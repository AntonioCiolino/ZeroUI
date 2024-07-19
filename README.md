# ZeroUI

ZeroUI is a Python-based user interface library for Raspberry Pi Zero. It provides a set of basic UI components such as buttons, labels, dropdowns, and color pickers to create simple touchscreen applications. This project is designed to work with the limited resources of the Raspberry Pi Zero and aims to offer a straightforward solution for touchscreen interactions.

## Background

This project began as an attempt to get a simple touchscreen and button interface working on a Raspberry Pi Zero. Initially, we experimented with various methods, including PyGame, but encountered several issues:

- **PyGame 1.9.6**: It sort of worked but was not a future-proof solution.
- **PyGame 2**: It offered more than needed and didn't perform well under Raspberry Pi OS Bullseye and Bookworm on the Pi Zero.

The goal was to develop a lightweight and efficient solution to get the screen running without the overhead of PyGame 2. As the project progressed, additional components were added to enhance functionality.

## Project Status

This is not a rock-solid implementation; it is a starting point to get things running. More error handling and optimizations are needed to improve stability and performance.

## Features

- **Buttons**: Simple clickable buttons with 3D effects.
- **Labels**: Text labels with optional background colors and 3D effects.
- **Dropdowns**: Selectable lists with touch scrolling and 3D effects.
- **Color Picker**: Modal color picker for selecting colors.
- **Event Manager**: Handles touch events and dispatches them to the UI components.
- **MQTT Integration**: Publish and subscribe to MQTT topics.

## Installation

### Prerequisites

- Python 3.x
- Virtual Environment (optional but recommended)
- Dependencies: `Pillow`, `paho-mqtt`, `evdev`

### Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/ZeroUI.git
   cd ZeroUI
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt```


### Configuration

	1.	Configure the Touchscreen Device Path
Update the device_path in TouchscreenHandler class to match your device.
	2.	Run the Application

python app.py

### Usage

Creating UI Components

Here’s a simple example of creating and displaying a button and label:

```
from PIL import ImageFont
from my_ui_package import EventManager, App, Button, Label

def button_callback(button):
    print(f"Button {button.text} pressed")

# Create an event manager
event_manager = EventManager()

# Create the app
app = App(320, 240, event_manager)

# Create a label with background color and 3D effect
label = Label(10, 10, "Hello, World!", event_manager, font=ImageFont.load_default(), text_color=(255, 255, 255), bg_color=(0, 0, 255), z_order=1)

# Create a button with a higher z_order
button = Button(10, 50, 100, 50, event_manager, text="Press me", z_order=2, callback=button_callback)

# Draw the controls
app.draw_items()
app.update_display()

# Simulate touch events
event_manager.dispatch('touch_down', x=20, y=60)
event_manager.dispatch('touch_up', x=20, y=60)

# Redraw after selection to reflect the hidden state
app.draw_items()
app.update_display()
``` 

### Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss your ideas.

### License

This project is licensed under the MIT License.

### Future Work

- Implement more robust error handling with try/except blocks.
- Optimize performance for the Raspberry Pi Zero.
- Add more UI components and enhance existing ones.
- Improve documentation and examples.

### Acknowledgments

- Special thanks to the open-source community for providing the libraries and tools used in this project.
- Inspiration from various tutorials and projects on Raspberry Pi and touchscreens.

