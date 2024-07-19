class Item:
    def __init__(self, command, data=None, delay=None):
        self.command = command
        self.data = data
        self.delay = delay

    def to_dict(self):
        item_dict = {"command": self.command}
        if self.data is not None:
            item_dict["data"] = self.data
        if self.delay is not None:
            item_dict["delay"] = self.delay
        return item_dict
