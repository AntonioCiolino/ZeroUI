from PIL import ImageFont
from .DrawableItem import DrawableItem

class Label(DrawableItem):
    def __init__(self, x, y, text, event_manager, font=None, text_color=(255, 255, 255), bg_color=None, z_order=0):
        super().__init__(z_order)  # Initialize the DrawableItem part
        self.x = x
        self.y = y
        self.text = text
        self.font = font if font else ImageFont.load_default()
        self.text_color = text_color
        self.bg_color = bg_color
        self.visible = True

        event_manager.register(self, z_order)

    def draw(self, draw_context):
        text_size = draw_context.textsize(self.text, font=self.font)
        if self.bg_color:
            rect = (self.x, self.y, self.x + text_size[0], self.y + text_size[1])
            draw_context.rectangle(rect, fill=self.bg_color)
            self.draw_3d_border(draw_context, rect, self.bg_color)

        draw_context.text((self.x, self.y), self.text, font=self.font, fill=self.text_color)

    def notify(self, event_type, **kwargs):
        # Labels don't need to respond to events
        return False
