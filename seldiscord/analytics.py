import time
import random

class AnalyticsEvent:
    type: str
    properties: dict

    def __init__(self, type: str, **properties):
        self.type = type
        self.properties = properties

    def __repr__(self) -> str:
        return f"<AnalyticsEvent [{self.type}]>"
    
    def to_dict(self, client_uuid: str) -> dict:
        _properties = self.properties.copy()
        _properties.update({
            "client_send_timestamp": int(time.time()*1000) \
                + random.randint(100,300),
            "client_track_timestamp": int(time.time()*1000),
            "client_uuid": client_uuid
        })
        return {"type": self.type, "properties": _properties}