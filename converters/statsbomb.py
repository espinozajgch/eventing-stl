from converters.base import BaseProviderConverter

class StatsBombConverter(BaseProviderConverter):
    def convert(self, event):
        eid = event["type"]["id"]
        action = None

        if eid == 30:  # Pass
            p = event.get("pass", {})
            pname = p.get("type", {}).get("name", "")
            if p.get("cross"):
                if pname == "Corner":
                    action = "corner_crossed"
                elif pname == "Free Kick":
                    action = "freekick_crossed"
                else:
                    action = "cross"
            elif pname == "Throw-in":
                action = "throw_in"
            elif pname == "Corner":
                action = "corner_short"
            elif pname == "Free Kick":
                action = "freekick_short"
            else:
                action = "pass"

        elif eid == 16:  # Shot
            s = event.get("shot", {})
            stype = s.get("type", {}).get("name", "")
            if stype == "Penalty":
                action = "penalty_shot"
            elif stype == "Free Kick":
                action = "freekick_shot"
            elif stype == "Open Play":
                action = "shot"

        elif eid == 22:  # Foul
            action = "foul"

        elif eid == 4:  # Duel
            if event.get("duel", {}).get("type", {}).get("name") == "Tackle":
                action = "tackle"

        elif eid == 10:
            action = "interception"

        elif eid == 9:
            action = "clearance"

        elif eid == 38:
            action = "bad_touch"

        elif eid == 14:
            action = "take_on"  # SPADL does not distinguish take_on vs dribble separately

        elif eid == 23:  # Goalkeeper actions
            gk_type = event.get("goalkeeper", {}).get("type", {}).get("name", "")
            if gk_type in ["Shot Saved", "Shot Saved to Post"]:
                action = "keeper_save"
            elif gk_type == "Claim":
                action = "keeper_claim"
            elif gk_type == "Punch":
                action = "keeper_punch"
            elif gk_type in ["Pick Up", "Collected"]:
                action = "keeper_pick_up"

        if action is None:
            return None

        loc = event.get("location", [0, 0])
        end = event.get(event["type"]["name"].lower(), {}).get("end_location", loc)
        
        #start_x, start_y = self.normalize_coords(loc[0], loc[1], 120, 80)
        #end_x, end_y = self.normalize_coords(end[0], end[1], 120, 80)

        #start_x, start_y = self.normalize_coords(loc[0], loc[1], provider="statsbomb")
        #end_x, end_y = self.normalize_coords(end[0], end[1], provider="statsbomb")

        start_x, start_y = loc[0], loc[1]
        end_x, end_y = end[0], end[1]
        
        time = event.get("minute", 0) * 60 + event.get("second", 0)

        return {
            "StartTime": round(time, 2),
            "EndTime": round(time + 1.0, 2),
            "StartLoc": (round(start_x, 2), round(start_y, 2)),
            "EndLoc": (round(end_x, 2), round(end_y, 2)),
            "Player": event.get("player", {}).get("name"),
            "Team": event.get("team", {}).get("name"),
            "ActionType": action,
            "BodyPart": self.get_bodypart(event),
            "Result": self.get_result(event),
            "Provider": "statsbomb"
        }

    def get_bodypart(self, event):
        bp = event.get("pass", {}).get("body_part", {}).get("name") \
            or event.get("shot", {}).get("body_part", {}).get("name") or ""
        bp = bp.lower()
        if "left" in bp:
            return "left_foot"
        elif "right" in bp:
            return "right_foot"
        elif "head" in bp:
            return "head"
        return "other"

    def get_result(self, event):
        outcome = event.get(event["type"]["name"].lower(), {}).get("outcome", {}).get("name", "").lower()
        if "goal" in outcome:
            return "success"
        elif any(word in outcome for word in ["off t", "incomplete", "lost"]):
            return "fail"
        elif "own goal" in outcome:
            return "own_goal"
        return "success"
