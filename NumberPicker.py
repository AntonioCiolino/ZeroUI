from .DrawableItem import DrawableItem
from PIL import ImageDraw, ImageFont

class NumberPicker(DrawableItem):
    def __init__(self, x, y, w, h, min_value, max_value, event_manager, initial_value=None, font=None, bg_color=(200, 200, 200), text_color=(0, 0, 0), callback=None, visible = True, z_order=0):
        super().__init__(z_order)  # Initialize the DrawableItem part
        self.rect = (x, y, x + w, y + h)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value if initial_value is not None else min_value
        self.font = font if font else ImageFont.load_default()
        self.bg_color = bg_color
        self.text_color = text_color
        self.callback = callback
        self.visible = visible

        # Button size
        self.button_width = w // 3

        # Register the NumberPicker with the EventManager
        event_manager.register(self, self.z_order)

    def draw(self, draw_context):
        if self.visible == False:
            return

        # Draw background
        draw_context.rectangle(self.rect, fill=self.bg_color)

        # Draw decrement button
        dec_rect = (self.rect[0], self.rect[1], self.rect[0] + self.button_width, self.rect[3])
        draw_context.rectangle(dec_rect, fill=(150, 150, 150))
        draw_context.text((dec_rect[0] + 10, dec_rect[1] + 10), "-", font=self.font, fill=self.text_color)

        # Draw increment button
        inc_rect = (self.rect[2] - self.button_width, self.rect[1], self.rect[2], self.rect[3])
        draw_context.rectangle(inc_rect, fill=(150, 150, 150))
        draw_context.text((inc_rect[0] + 10, inc_rect[1] + 10), "+", font=self.font, fill=self.text_color)

        # Draw current value
        value_text = str(self.value)
        text_size = draw_context.textsize(value_text, font=self.font)
        text_x = self.rect[0] + (self.rect[2] - self.rect[0] - text_size[0]) // 2
        text_y = self.rect[1] + (self.rect[3] - self.rect[1] - text_size[1]) // 2
        draw_context.text((text_x, text_y), value_text, font=self.font, fill=self.text_color)

        # Draw 3D effect border
        self.draw_3d_border(draw_context, self.rect, self.bg_color)

    def notify(self, event_type, **kwargs):
        if self.visible == False:
            return False
        x, y = kwargs.get('x'), kwargs.get('y')
        if event_type == "touch_down":
            if self.is_pressed(x, y):
                if x < self.rect[0] + self.button_width:
                    self.decrement()
                elif x > self.rect[2] - self.button_width:
                    self.increment()
                return True
        return False

    def is_pressed(self, x, y):
        return self.rect[0] <= x <= self.rect[2] and self.rect[1] <= y <= self.rect[3]

    def increment(self):
        if self.value < self.max_value:
            self.value += 1
            if self.callback:
                self.callback(self.value)

    def decrement(self):
        if self.value > self.min_value:
            self.value -= 1
            if self.callback:
                self.callback(self.value)
