from converters.opta import OptaConverter
from converters.statsbomb import StatsBombConverter
from converters.wyscout import WyscoutConverter

class SPADLConverter:
    def __init__(self):
        self.converters = {
            "opta": OptaConverter(),
            "statsbomb": StatsBombConverter(),
            "wyscout": WyscoutConverter()
        }

    def convert_event_to_spadl(self, event, provider):
        provider = provider.lower()
        if provider not in self.converters:
            raise ValueError(f"Proveedor no soportado: {provider}")
        return self.converters[provider].convert(event)