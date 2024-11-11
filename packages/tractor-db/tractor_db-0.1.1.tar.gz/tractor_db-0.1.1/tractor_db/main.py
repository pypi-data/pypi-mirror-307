# tractor_data/main.py
import json
import random
import os

class TractorData:
    def __init__(self):
        self.tractors = self._load_data()

    def _load_data(self):
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'db.json')
            with open(db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return [
                {"name": "L3901", "brand": "Kubota"},
                {"name": "1025R", "brand": "John Deere"}
            ]

    def get_tractor(self):
        return random.choice(self.tractors)

    def get_tractor_name(self):
        tractor = self.get_tractor()
        return f"{tractor['brand']} {tractor['name']}"

# Create single instance
_tractor_data = TractorData()

# Public API functions
def get_tractor():
    return _tractor_data.get_tractor()

def get_tractor_name():
    return _tractor_data.get_tractor_name()