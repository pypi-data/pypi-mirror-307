import json

from .deck import Deck

def custom_serializer(self):
    if isinstance(self, ViewerData):
        return {"name": self.name, "height": self.height, "decks": [custom_serializer(deck) for deck in self.decks] }
        # return {"name": self.name, "height": self.height }
    elif isinstance(self, Deck):
        return {"id": self.id, "name": self.name, "image_id": self.image_id}
    raise TypeError(f"Type {type(self)} is not serializable")

class ViewerData:
    def __init__(self, name, height, deck_image_id):
        self.name = name
        self.height = height
        self.deck_image_id = deck_image_id
        self.decks = []
                
    def add_deck(self, deck: Deck):
        self.decks.append(deck)
        
    def to_json(self):
        # return json.dumps(self.__dict__)    
        return custom_serializer(self)
    
    # def __str__(self):
    #     decks_str = "\n".join(str(deck) for deck in self.decks)
    #     beacons_str = "\n".join(str(beacon) for beacon in self.decks.beacons)
    #     cameras_str = "\n".join(str(camera) for camera in self.decks.cameras)
    #     return f"{self.name}, beacons: {beacons_str}, cameras: {cameras_str}"
        