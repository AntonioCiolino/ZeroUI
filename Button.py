from PIL import ImageDraw, ImageFont
from .DrawableItem  import DrawableItem

class Button(DrawableItem):
    def __init__(self, x, y, w, h, event_manager, text="Button", color=(0, 128, 255), text_color=(255, 255, 255), font=None, callback=None, z_order=0):
        super().__init__(z_order)  # Initialize the DrawableItem part
        self.rect = (x, y, x + w, y + h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font
        self.pressed = False
        self.callback = callback
        self.visible=True

        event_manager.register(self, self.z_order)

    def draw(self, draw_context):
        # Draw the button with a 3D effect
        top_shade_color = self._lighten_color(self.color, 1.5)
        bottom_shade_color = self._darken_color(self.color, 0.6)

        if self.pressed:
            draw_context.rectangle(self.rect, fill=bottom_shade_color)
        else:
            draw_context.rectangle(self.rect, fill=self.color)
            # Draw top shade
            draw_context.line([self.rect[0], self.rect[1], self.rect[2], self.rect[1]], fill=top_shade_color, width=3)
            draw_context.line([self.rect[0], self.rect[1], self.rect[0], self.rect[3]], fill=top_shade_color, width=3)
            # Draw bottom shade
            draw_context.line([self.rect[0], self.rect[3], self.rect[2], self.rect[3]], fill=bottom_shade_color, width=3)
            draw_context.line([self.rect[2], self.rect[1], self.rect[2], self.rect[3]], fill=bottom_shade_color, width=3)

        # Draw the button text
        if self.font:
            text_size = draw_context.textsize(self.text, font=self.font)
            text_x = self.rect[0] + (self.rect[2] - self.rect[0] - text_size[0]) // 2
            text_y = self.rect[1] + (self.rect[3] - self.rect[1] - text_size[1]) // 2  
            draw_context.text((text_x, text_y), self.text, font=self.font, fill=self.text_color)
        else:
            draw_context.text((self.rect[0] + 10, self.rect[1] + 10), self.text, fill=self.text_color)

    def notify(self, event_type, **kwargs):
        x, y = kwargs.get('x'), kwargs.get('y')
        if event_type == "touch_down":
            if self.is_pressed(x, y):
                self.pressed = True
                return True
        elif event_type == "drag":
            if self.pressed and self.is_pressed(x, y):
                # Handle dragging if needed
                return True
        elif event_type == "touch_up":
            if self.pressed:
                self.pressed = False
                if self.is_pressed(x, y) and self.callback:
                    self.callback(self)  # Call the callback on touch up
                return True
        return False

    def is_pressed(self, x, y):
        return self.rect[0] <= x <= self.rect[2] and self.rect[1] <= y <= self.rect[3]

    def _lighten_color(self, color, factor):
        return tuple(min(int(c * factor), 255) for c in color)

    def _darken_color(self, color, factor):
        return tuple(max(int(c * factor), 0) for c in color)
