from converters.base import BaseProviderConverter

class StatsBombConverter(BaseProviderConverter):
    def convert(self, event):
        action = self.identify_action(event)
        if action is None:
            return None

        loc = event.get("location", [0, 0])
        end = event.get(event["type"]["name"].lower(), {}).get("end_location", loc)

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
            "Result": self.get_result(event, action),
            "Provider": "statsbomb"
        }

    def identify_action(self, event):
        eid = event["type"]["id"]

        if eid == 30:  # Pass
            p = event.get("pass", {})
            pname = p.get("type", {}).get("name", "")
            if p.get("cross"):
                if pname == "Corner":
                    return "corner_crossed"
                elif pname == "Free Kick":
                    return "freekick_crossed"
                else:
                    return "cross"
            elif pname == "Throw-in":
                return "throw_in"
            elif pname == "Corner":
                return "corner_short"
            elif pname == "Free Kick":
                return "freekick_short"
            else:
                return "pass"

        elif eid == 16:  # Shot
            s = event.get("shot", {})
            stype = s.get("type", {}).get("name", "")
            if stype == "Penalty":
                return "penalty_shot"
            elif stype == "Free Kick":
                return "freekick_shot"
            else:
                return "shot"

        elif eid == 22:
            return "foul"

        elif eid == 4:
            if event.get("duel", {}).get("type", {}).get("name") == "Tackle":
                return "tackle"

        elif eid == 10:
            return "interception"

        elif eid == 9:
            return "clearance"

        elif eid == 38:
            return "bad_touch"

        elif eid == 14:
            return "take_on"

        elif eid == 23:
            gk_type = event.get("goalkeeper", {}).get("type", {}).get("name", "")
            if gk_type in ["Shot Saved", "Shot Saved to Post"]:
                return "keeper_save"
            elif gk_type == "Claim":
                return "keeper_claim"
            elif gk_type == "Punch":
                return "keeper_punch"
            elif gk_type in ["Pick Up", "Collected"]:
                return "keeper_pick_up"

        return None

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

    def get_result(self, event, action):
        event_type = event["type"]["name"].lower()
        subtype = event.get(event_type, {})
        outcome = subtype.get("outcome", {}).get("name", "").lower()

        if action in {
            "bad_touch", "foul"
        }: return "fail"

        # SHOTS
        if action in {"shot", "freekick_shot", "penalty_shot"}:
            if outcome in {"goal", "saved", "saved to post"}:
                return "success"
            else:
                return "fail"

        # PASSES
        if action in {
            "pass", "cross", "freekick_short", "freekick_crossed",
            "corner_short", "corner_crossed", "throw_in"
        }:
            fail_outcomes = {
                "incomplete", "injury clearance", "out", "pass offside", "unknown"
            }
            return "fail" if outcome in fail_outcomes else "success"

        # FALTAS / TARJETAS
        if outcome == "offside":
            return "offside"
        if outcome == "own goal":
            return "own_goal"
        if outcome == "yellow card":
            return "yellow_card"
        if outcome == "red card":
            return "red_card"
        if outcome == "second yellow":
            return "second_yellow_card"

        # OTROS
        if outcome in {"success", "won", "complete"}:
            return "success"
        if outcome in {"fail", "lost", "incomplete"}:
            return "fail"

        return "success"
