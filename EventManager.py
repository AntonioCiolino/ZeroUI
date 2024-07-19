from .TouchscreenHandler import TouchscreenHandler

class EventManager:
    def __init__(self):
        self.listeners = []

    def register(self, listener, z_order=0):
        self.listeners.append((listener, z_order))
        self.listeners.sort(key=lambda x: x[1], reverse=True)
        #self.debug_listeners()  # Print the listeners for debugging

    def dispatch(self, event_type, **kwargs):
        for listener, _ in self.listeners:
            if listener.notify(event_type, **kwargs):
                break  # Stop dispatching if the event was handled

    def get_visible_listeners(self):
        return [listener for listener, _ in self.listeners if getattr(listener, 'visible', True)]


    def debug_listeners(self):
        print("Current listeners in order of z_order:")
        for listener, z_order in self.listeners:
            print(f"Listener: {listener.__class__.__name__}, z_order: {z_order}, ID: {id(listener)}")
        print("\n")
