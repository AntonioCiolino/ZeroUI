import evdev
from evdev import InputDevice, categorize, ecodes
import select

class TouchscreenHandler:
    def __init__(self, device_path, event_manager):
        self.device = InputDevice(device_path)
        self.device.grab()  # Grab the device for exclusive access
        self.event_manager = event_manager
        self.touching = False  # Track the state of the touch
        self.current_x = None  # Store the current x coordinate
        self.current_y = None  # Store the current y coordinate

    def poll(self):
        # Use select to check for available events without blocking
        r, w, e = select.select([self.device], [], [], 0.01)
        if r:
            for event in self.device.read():
                if event.type == ecodes.EV_ABS:
                    abs_event = categorize(event)
                    if abs_event.event.code == ecodes.ABS_MT_POSITION_X:
                        self.current_x = abs_event.event.value
                    elif abs_event.event.code == ecodes.ABS_MT_POSITION_Y:
                        self.current_y = abs_event.event.value

                    if self.touching and self.current_x is not None and self.current_y is not None:
                        self.event_manager.dispatch('drag', x=self.current_x, y=self.current_y)
                elif event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH:
                    if event.value == 1 and not self.touching:
                        # Touch down event
                        self.touching = True
                        if self.current_x is not None and self.current_y is not None:
                            self.event_manager.dispatch('touch_down', x=self.current_x, y=self.current_y)
                    elif event.value == 0 and self.touching:
                        # Touch up event
                        self.touching = False
                        if self.current_x is not None and self.current_y is not None:
                            self.event_manager.dispatch('touch_up', x=self.current_x, y=self.current_y)

    def cleanup(self):
        self.device.ungrab()
