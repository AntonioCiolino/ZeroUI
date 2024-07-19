from .DrawableItem import DrawableItem
from PIL import Image, ImageDraw, ImageFont

class ListComponent(DrawableItem):
    def __init__(self, x, y, w, h, items, event_manager, font=None, item_height=30, bg_color=(200, 200, 200), text_color=(0, 0, 0), selected_color=(150, 150, 150), callback=None, z_order=0):
        super().__init__(z_order)  # Initialize the DrawableItem part
        self.rect = (x, y, x + w, y + h)
        self.items = items
        self.font = font if font else ImageFont.load_default()
        self.item_height = item_height
        self.bg_color = bg_color
        self.text_color = text_color
        self.selected_color = selected_color
        self.callback = callback
        self.selected_index = -1
        self.scroll_offset = 0
        self.last_touch_y = None

        event_manager.register(self, self.z_order)

    def draw(self, draw_context):
        # Draw the component background
        draw_context.rectangle(self.rect, fill=self.bg_color)
        
        # Draw 3D effect border
        self.draw_3d_border(draw_context, self.rect, self.bg_color)

        # Draw the items within the visible area
        x, y = self.rect[0], self.rect[1]
        for index, item in enumerate(self.items):
            item_y = y + index * self.item_height - self.scroll_offset
            item_rect = (x, item_y, self.rect[2], item_y + self.item_height)
            
            if item_rect[1] < self.rect[1] or item_rect[3] > self.rect[3]:
                continue  # Skip drawing outside the bounds
            
            if self.is_selected(index):
                draw_context.rectangle(item_rect, fill=self.selected_color)
            draw_context.text((x + 5, item_y + (self.item_height - self.font.getsize(item)[1]) // 2), item, font=self.font, fill=self.text_color)

    def notify(self, event_type, **kwargs):
        x, y = kwargs.get('x'), kwargs.get('y')
        if event_type == "touch_down":
            if self.is_pressed(x, y):
                self.last_touch_y = y
                self.selected_index = self.get_item_index(y)
                if self.selected_index is None or self.selected_index >= len(self.items):
                    return False
                if self.callback: 
                    self.callback(self.selected_index, self.items[self.selected_index])
                return True
        elif event_type == "drag":
            if self.last_touch_y is not None:
                dy = y - self.last_touch_y
                self.scroll_offset -= dy
                self.scroll_offset = max(0, min(self.scroll_offset, max(0, len(self.items) * self.item_height - (self.rect[3] - self.rect[1]))))
                self.last_touch_y = y
                return True
        elif event_type == "touch_up":
            self.last_touch_y = None
        return False

    def is_pressed(self, x, y):
        return self.rect[0] <= x <= self.rect[2] and self.rect[1] <= y <= self.rect[3]

    def is_selected(self, index):
        return index == self.selected_index

    def get_item_index(self, y):
        relative_y = y - self.rect[1] + self.scroll_offset
        return relative_y // self.item_height

    def clear(self):
        self.items = []
        self.selected_index = -1
        self.scroll_offset = 0

    def add_item(self, item):
        self.items.append(item)
