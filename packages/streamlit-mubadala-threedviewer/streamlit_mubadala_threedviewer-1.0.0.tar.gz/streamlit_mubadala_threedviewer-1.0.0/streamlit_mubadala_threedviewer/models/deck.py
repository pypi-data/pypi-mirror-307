import json

from .beacon import Beacon
from .camera import Camera

class Deck:
    
    def __init__(self, id, name, image_id) -> None:
        self.id = id
        self.name = name
        self.image_id = image_id
        
        self.beacons = []
        self.cameras = []
                
    def add_beacon(self, beacon: Beacon):
        self.beacons.append(beacon)
        
    def add_camera(self, camera: Camera):
        self.cameras.append(camera)
        
    def to_json(self):
        return json.dumps(self.__dict__)
        
    
        
    