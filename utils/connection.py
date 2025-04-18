import pandas as pd

from pathlib import Path
from converters.spadl import SPADLConverter
from converters.opta import OptaConverter
from converters.wyscout import WyscoutConverter
from utils.loaders import load_opta_events
from utils.loaders import load_statsbomb_events
from utils.loaders import load_wyscout_events
from utils import mappers

def get_df():
    # # Barcelona - Real Madrid, 2 - 2 - May 6, 2018 Temporada 17/18
    # Rutas a los archivos
    statsbomb_path = Path("data/statsbomb/9924.json")
    wyscout_path = Path("data/wyscout/2565907.json")
    opta_path = Path("data/opta/f24-23-2017-943158-eventdetails.xml")

    # Crear convertidor
    converter = SPADLConverter()

    # Leer mappings
    f40_path = Path("data/opta/srml-23-2017-squads.xml")
    team_map, player_map = mappers.load_opta_mappings(f40_path)

    teams_path = Path("data/wyscout/teams.json")
    players_path = Path("data/wyscout/players.json")
    team_map_ws, player_map_ws = mappers.load_wyscout_mappings(teams_path, players_path)

    # Asignar el nuevo convertidor en el wrapper SPADLConverter
    converter.converters["wyscout"] = WyscoutConverter(team_map=team_map_ws, player_map=player_map_ws)

    # Instanciar convertidor personalizado
    converter.converters["opta"] = OptaConverter(team_map=team_map, player_map=player_map)

    sb_events = load_statsbomb_events(statsbomb_path)
    ws_events = load_wyscout_events(wyscout_path)
    op_events = load_opta_events(opta_path)

    spadl_sb = [converter.convert_event_to_spadl(e, "statsbomb") for e in sb_events if converter.convert_event_to_spadl(e, "statsbomb")]
    spadl_ws = [converter.convert_event_to_spadl(e, "wyscout") for e in ws_events if converter.convert_event_to_spadl(e, "wyscout")]
    spadl_op = [converter.convert_event_to_spadl(e, "opta") for e in op_events if converter.convert_event_to_spadl(e, "opta")]

    df_sb = pd.DataFrame(spadl_sb)
    df_ws = pd.DataFrame(spadl_ws)
    df_ws = df_ws[df_ws['Player'] != '0']
    df_op = pd.DataFrame(spadl_op)

    return df_sb, df_op, df_ws
