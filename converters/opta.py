from converters.base import BaseProviderConverter

class OptaConverter(BaseProviderConverter):
    def __init__(self, team_map=None, player_map=None):
        super().__init__()
        self.team_map = team_map or {}
        self.player_map = player_map or {}

    def convert(self, event):
        type_id = int(event.get("type_id", -1))

        qualifiers_list = event.get("qualifiers", [])
        qualifiers_dict = {str(q.get("qualifier_id")): q.get("value") for q in qualifiers_list}
        #[str(q.get("qualifier_id")) for q in qualifiers_list]

        action = None
        if type_id == 1:
            if "2" in qualifiers_dict:
                action = "cross"
            elif "107" in qualifiers_dict:
                action = "throw_in"
            elif "24" in qualifiers_dict:
                action = "freekick_crossed"
            elif "5" in qualifiers_dict:
                action = "freekick_short"
            elif "6" in qualifiers_dict:
                action = "corner_crossed" if "2" in qualifiers_dict else "corner_short"
            else:
                action = "pass"
        elif type_id in [13, 14, 15, 16]:
            if "9" in qualifiers_dict:
                action = "penalty_shot"
            elif "26" in qualifiers_dict:
                action = "freekick_shot"
            else:
                action = "shot"
        elif type_id == 4:
            foul_qualifiers = {"12","13"}
            if foul_qualifiers & qualifiers_dict.keys():
                action = "foul"

        else:
            action = {
                3: "take_on",
                7: "tackle",
                8: "interception",
                12: "clearance",
                61: "bad_touch",
                10: "keeper_save",
                11: "keeper_claim",
                41: "keeper_punch",
                52: "keeper_pick_up"
            }.get(type_id, None)

        if action is None:
            return None

        # Coordenadas
        start_x = event.get("x", 0)
        start_y = event.get("y", 0)
        end_x = qualifiers_dict.get("140", start_x)
        end_y = qualifiers_dict.get("141", start_y)

        time = float(event.get("min", 0)) * 60 + float(event.get("sec", 0))
        player_id = event.get("player_id")
        team_id = event.get("team_id")

        return {
            "StartTime": round(time, 2),
            "EndTime": round(time + 1.0, 2),
            "StartLoc": (round(float(start_x), 2), round(float(start_y), 2)),
            "EndLoc": (round(float(end_x), 2), round(float(end_y), 2)),
            "Player": self.player_map.get(player_id, player_id),
            "Team": self.team_map.get(team_id, team_id),
            "ActionType": action,
            "BodyPart": self.get_bodypart(qualifiers_dict),
            "Result": self.get_result(event, action, qualifiers_dict),
            "Provider": "opta"
        }

    def get_bodypart(self, qualifiers):
        if "15" in qualifiers:
            return "head"
        elif "72" in qualifiers:
            return "left_foot"
        elif "20" in qualifiers:
            return "right_foot"
        elif "21" in qualifiers:
            return "other"
        return "other"

    def get_result(self, event, action, qualifiers):
        """
        Determina el resultado de una acción con lógica específica para disparos.
        """
        outcome = str(event.get("outcome", "0"))
        type_id = int(event.get("type_id", -1))

        # -- TIROS --
        if action in {"shot", "freekick_shot", "penalty_shot"}:
            if type_id in [13, 14]:  # Miss o Post
                return "fail"
            if "82" in qualifiers:
                return "fail"
            if "28" in qualifiers:  # Own goal
                return "own_goal"
            return "success" if outcome == "1" else "fail"

        # -- PASES --
        elif action in {
            "pass", "cross", "freekick_short", "freekick_crossed",
            "corner_short", "corner_crossed", "throw_in"
        }:
            return "success" if outcome == "1" else "fail"

        # -- FALTAS Y TARJETAS --
        elif action == "foul":
            if "31" in qualifiers:
                return "yellow_card"
            elif "32" in qualifiers:
                return "second_yellow_card"
            elif "33" in qualifiers:
                return "red_card"
            return "fail"
        
        elif action == "bad_touch":
           return "fail"

        # -- DEMÁS ACCIONES --
        else:
            return "success" if outcome == "1" else "fail"

