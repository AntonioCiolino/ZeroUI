from .DrawableItem import DrawableItem
from PIL import ImageDraw, ImageFont

class ColorPicker(DrawableItem):
    def __init__(self, x, y, w, h, colors, event_manager, bg_color=(128,12,128), font=None, callback=None, visible=True, z_order=0):
        super().__init__(z_order)  # Initialize the DrawableItem part
        self.rect = (x, y, x + w, y + h)
        self.colors = colors
        self.font = font if font else ImageFont.load_default()
        self.callback = callback
        self.selected_color = None
        self.bg_color = bg_color
        self.visible = visible

        # Calculate the size of each color box
        self.box_size = min(w // len(colors[0]), h // len(colors))

        # Register the ColorPicker with the EventManager
        event_manager.register(self, self.z_order)

    def draw(self, draw_context):
        if not self.visible:
            return

        # Draw the color boxes
        for row_index, row in enumerate(self.colors):
            for col_index, color in enumerate(row):
                box_x = self.rect[0] + col_index * self.box_size
                box_y = self.rect[1] + row_index * self.box_size
                box_rect = (box_x, box_y, box_x + self.box_size, box_y + self.box_size)
                draw_context.rectangle(box_rect, fill=color)

                # Draw 3D effect border for each box
                self.draw_3d_border(draw_context, box_rect, self.bg_color)

                # Draw a border if this color is selected
                if self.selected_color == color:
                    draw_context.rectangle(box_rect, outline=(255, 255, 255), width=3)

    def notify(self, event_type, **kwargs):
        if not self.visible:
            return False
        x, y = kwargs.get('x'), kwargs.get('y')
        if event_type == "touch_down" and self.is_pressed(x, y):
            col_index = (x - self.rect[0]) // self.box_size
            row_index = (y - self.rect[1]) // self.box_size
            if 0 <= row_index < len(self.colors) and 0 <= col_index < len(self.colors[0]):
                self.selected_color = self.colors[row_index][col_index]
                if self.callback:
                    self.callback(self.selected_color)
                return True
        return False

    def is_pressed(self, x, y):
        return self.rect[0] <= x <= self.rect[2] and self.rect[1] <= y <= self.rect[3]
