import json
from .Item import Item

class ListFormatter:
    def __init__(self, items):
        self.items = items

    def format_to_json(self):
        items_list = [item.to_dict() for item in self.items]
        return json.dumps(items_list, indent=4)
