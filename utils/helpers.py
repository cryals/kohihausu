import json
import os

def load_json(filename):
    filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}