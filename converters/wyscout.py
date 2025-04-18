from converters.base import BaseProviderConverter

class WyscoutConverter(BaseProviderConverter):
    def __init__(self, team_map=None, player_map=None):
        super().__init__()
        self.team_map = team_map or {}
        self.player_map = player_map or {}

    def convert(self, event):
        eid = event.get("eventId")
        sub = event.get("subEventName", "").lower()
        tags = [tag["id"] for tag in event.get("tags", [])]

        action = None
        
        # Detectar intercepción por tag 1401 antes de cualquier otra lógica
        if 1401 in tags:
            action = "interception"

        if action is None:
            if eid == 8:  # Pass
                if sub == "cross":
                    action = "cross"
                elif sub == "simple pass":
                    action = "bad_touch" if 1802 in tags else "pass"
                else:
                    action = "pass"
            elif eid == 3:
                if sub == "penalty":
                    action = "penalty_shot"
                elif sub == "throw in":
                    action = "throw_in"
                elif sub == "free kick":
                    action = "freekick_short"
                elif sub == "corner":
                    action = "corner_crossed" if 302 in tags else "corner_short"
                elif sub == "free kick shot":
                    action = "freekick_shot"
                elif sub == "free kick cross":
                    action = "freekick_crossed"
                else:
                    action = "freekick_short"
            elif eid == 10:
                action = "shot"
            elif eid == 2:
                action = "foul"
            elif eid == 7:
                action = "clearance"
            elif eid == 9:
                action = "keeper_save"
            elif eid == 1:
                if sub == "ground attacking duel" and any(t in tags for t in [503, 504]):
                    action = "take_on"
                elif sub == "ground defending duel" and 1601 in tags:
                    action = "tackle"

        if action is None:
            return None

        pos = event.get("positions", [])
        loc = [pos[0]["x"], pos[0]["y"]] if len(pos) > 0 else [0, 0]
        end = [pos[1]["x"], pos[1]["y"]] if len(pos) > 1 else loc
        start_x, start_y = loc[0], loc[1]
        end_x, end_y = end[0], end[1]
        raw_time = event.get("eventSec", 0)
        period = event.get("matchPeriod", "1H")
        
        # Mapeo de períodos a segundos de offset
        period_offsets = {
            "1H": 0,
            "2H": 45 * 60,
            "E1": 90 * 60,
            "E2": 105 * 60,
            "P": 120 * 60
        }

        offset = period_offsets.get(period, 0)
        time = round(raw_time + offset, 2)

        player_id = str(event.get("playerId"))
        team_id = str(event.get("teamId"))

        return {
            "StartTime": round(time, 2),
            "EndTime": round(time + 1.0, 2),
            "StartLoc": (round(start_x, 2), round(start_y, 2)),
            "EndLoc": (round(end_x, 2), round(end_y, 2)),
            "Player": self.player_map.get(player_id, player_id),
            "Team": self.team_map.get(team_id, team_id),
            "ActionType": action,
            "BodyPart": self.get_bodypart(event),
            "Result": self.get_result(event, action),
            "Provider": "wyscout"
        }

    def get_bodypart(self, event):
        tag_ids = [tag["id"] for tag in event.get("tags", [])]
        if 401 in tag_ids:
            return "left_foot"
        elif 402 in tag_ids:
            return "right_foot"
        elif 403 in tag_ids:
            return "head"
        return "other"

    def get_result(self, event, action):
        tag_ids = [tag["id"] for tag in event.get("tags", [])]

        if 1701 in tag_ids:
            return "red_card"
        elif 1702 in tag_ids:
            return "yellow_card"
        elif 1703 in tag_ids:
            return "second_yellow_card"
        elif 101 in tag_ids:
            return "goal"
        elif 102 in tag_ids:
            return "own_goal"

        if action in ["pass", "cross", "freekick_short", "freekick_crossed", "corner_short", "corner_crossed"]:
            if 1801 in tag_ids:
                return "success"
            elif 1802 in tag_ids:
                return "fail"
        elif action in ["shot", "freekick_shot", "penalty_shot"]:
            if 1801 in tag_ids:
                return "success"
            elif 1802 in tag_ids:
                return "fail"
            elif 2101 in tag_ids:
                return "blocked"
        elif action == "tackle":
            if 703 in tag_ids:
                return "success"
            elif 701 in tag_ids:
                return "fail"
        elif action == "interception":
            if 1401 in tag_ids:
                return "success"
        elif action == "clearance":
            if 1501 in tag_ids:
                return "success"
        elif action == "keeper_save":
            if 2000 in tag_ids:
                return "success"

        return "unknown"
