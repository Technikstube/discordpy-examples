import json

config = "external-permission-system\configuration.json"

class Config:
    def __init__(self):
        pass
    
    def get(self) -> dict:
        with open(config, "r") as cf:
            data = json.load(cf)
        return data

    def save(self, conf: dict) -> None:
        with open(config, "w") as cf:
            json.dump(conf, cf, indent=4)