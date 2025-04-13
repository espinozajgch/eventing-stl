import json
import xml.etree.ElementTree as ET
from pathlib import Path
from utils import util

def load_wyscout_mappings(teams_path: Path, players_path: Path):
    with open(teams_path, 'r', encoding='utf-8') as f:
        teams_data = json.load(f)
    with open(players_path, 'r', encoding='utf-8') as f:
        players_data = json.load(f)

    team_map = {
        str(team["wyId"]): util.clean_unicode(team["name"])
        for team in teams_data
    }
    player_map = {
        str(player["wyId"]): util.clean_unicode(player["shortName"])
        for player in players_data
    }

    return team_map, player_map
    
import xml.etree.ElementTree as ET

def load_opta_mappings(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    team_map = {}
    player_map = {}

    for team in root.findall(".//Team"):
        team_id = team.attrib.get("uID", "").replace("t", "")
        team_name = team.find("Name").text
        team_map[team_id] = team_name

        for player in team.findall(".//Player"):
            player_id = player.attrib.get("uID", "").replace("p", "")
            full_name = player.attrib.get("Name", None)  # PRIORIDAD 1: atributo Name

            # Si no hay atributo Name, buscar en los Stat
            if not full_name or not full_name.strip():
                first_name = None
                last_name = None
                known_name = None

                for stat in player.findall("Stat"):
                    stat_type = stat.attrib.get("Type", "")
                    if stat_type == "first_name":
                        first_name = stat.text
                    elif stat_type == "last_name":
                        last_name = stat.text
                    elif stat_type == "known_name":
                        known_name = stat.text

                if known_name:
                    full_name = known_name.strip()
                elif first_name or last_name:
                    full_name = f"{first_name or ''} {last_name or ''}".strip()
                else:
                    full_name = f"Player_{player_id}"

            player_map[player_id] = full_name

    return team_map, player_map

