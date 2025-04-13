import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any

def load_statsbomb_events(filepath: Path) -> List[Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_wyscout_events(filepath: Path) -> List[Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_opta_events(filepath: Path) -> List[Dict[str, Any]]:
    tree = ET.parse(filepath)
    root = tree.getroot()
    events = []
    for event in root.findall(".//Event"):
        ev_dict = dict(event.attrib)
        qualifiers = [
            {"qualifier_id": q.get("qualifier_id"), "value": q.get("value")}
            for q in event.findall("Q")
        ]
        ev_dict["qualifiers"] = qualifiers
        events.append(ev_dict)
    return events

