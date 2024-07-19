from .DrawableItem import DrawableItem
from PIL import Image, ImageDraw, ImageFont

class Dropdown(DrawableItem):
    def __init__(self, x, y, w, h, items, event_manager, font=None, bg_color=(200, 200, 200), text_color=(0, 0, 0), selected_color=(150, 150, 150), callback=None, z_order=0):
        super().__init__(z_order)  # Initialize the DrawableItem part
        self.rect = (x, y, x + w, y + h)
        self.items = items
        self.font = font if font else ImageFont.load_default()
        self.bg_color = bg_color
        self.text_color = text_color
        self.selected_color = selected_color
        self.callback = callback
        self.selected_index = -1
        self.expanded = False
        self.item_height = h
        self.scroll_offset = 0
        self.last_touch_y = None

        # Register the Dropdown with the EventManager
        event_manager.register(self, self.z_order)

    def draw(self, draw_context):
        # Draw the main button
        draw_context.rectangle(self.rect, fill=self.bg_color)

        # Draw the button with a 3D effect
        top_shade_color = self._lighten_color(self.bg_color, 1.5)
        bottom_shade_color = self._darken_color(self.bg_color, 0.6)

        # Draw top shade
        draw_context.line([self.rect[0], self.rect[1], self.rect[2], self.rect[1]], fill=top_shade_color, width=3)
        draw_context.line([self.rect[0], self.rect[1], self.rect[0], self.rect[3]], fill=top_shade_color, width=3)
        # Draw bottom shade
        draw_context.line([self.rect[0], self.rect[3], self.rect[2], self.rect[3]], fill=bottom_shade_color, width=3)
        draw_context.line([self.rect[2], self.rect[1], self.rect[2], self.rect[3]], fill=bottom_shade_color, width=3)

        main_text = self.items[self.selected_index] if self.selected_index >= 0 else "Select"
        text_size = draw_context.textsize(main_text, font=self.font)
        text_x = self.rect[0] + (self.rect[2] - self.rect[0] - text_size[0]) // 2
        text_y = self.rect[1] + (self.rect[3] - self.rect[1] - text_size[1]) // 2
        draw_context.text((text_x, text_y), main_text, font=self.font, fill=self.text_color)

        # Draw the dropdown arrow
        arrow_x = self.rect[2] - 10 
        arrow_y = self.rect[1] + (self.rect[3] - self.rect[1]) // 2
        arrow_size = 10
        arrow_points = [(arrow_x - arrow_size // 2, arrow_y - arrow_size // 2), 
                        (arrow_x + arrow_size // 2, arrow_y - arrow_size // 2), 
                        (arrow_x, arrow_y + arrow_size // 2)]
        draw_context.polygon(arrow_points, fill=self.text_color)

        # Draw the dropdown items if expanded
        if self.expanded:
            for index, item in enumerate(self.items):
                item_y = self.rect[3] + index * self.item_height - self.scroll_offset
                item_rect = [self.rect[0], item_y, self.rect[2], item_y + self.item_height]
                
                if item_rect[1] < self.rect[3] or item_rect[3] > self.rect[3] + self.item_height * len(self.items):
                    continue  # Skip drawing outside the bounds

                draw_context.rectangle(item_rect, fill=self.selected_color if self.selected_index == index else self.bg_color)
                item_text_size = draw_context.textsize(item, font=self.font)
                item_text_x = self.rect[0] + (self.rect[2] - self.rect[0] - item_text_size[0]) // 2
                item_text_y = item_y + (self.item_height - item_text_size[1]) // 2
                draw_context.text((item_text_x, item_text_y), item, font=self.font, fill=self.text_color)

    def notify(self, event_type, **kwargs):
        x, y = kwargs.get('x'), kwargs.get('y')
        if event_type == "touch_down":
            if self.is_pressed(x, y):
                if self.expanded:
                    self.last_touch_y = y
                    # Highlight the item on touch down
                    self.highlighted_index = self.get_item_index(y)
                return True
        elif event_type == "touch_up":
            self.last_touch_y = None
            if self.is_pressed(x, y):
                if self.expanded and self.highlighted_index >= 0:
                    # Select the item on touch up
                    self.selected_index = self.highlighted_index
                    if self.callback:
                        self.callback(self.selected_index, self.items[self.selected_index])
                self.expanded = not self.expanded
                self.highlighted_index = -1
                return True
            else:
                # Collapse if click is outside
                self.expanded = False
        elif event_type == "drag":
            if self.expanded and self.last_touch_y is not None:
                dy = y - self.last_touch_y
                self.scroll_offset -= dy
                self.scroll_offset = max(0, min(self.scroll_offset, max(0, len(self.items) * self.item_height - (self.rect[3] - self.rect[1]))))
                self.last_touch_y = y
                # Highlight the item on drag
                self.highlighted_index = self.get_item_index(y)
                return True
        return False

    def is_pressed(self, x, y):
        return (self.rect[0] <= x <= self.rect[2] and self.rect[1] <= y <= (self.rect[3] if not self.expanded else self.rect[3] + len(self.items) * self.item_height))

    def get_item_index(self, y):
        if self.rect[3] <= y <= self.rect[3] + len(self.items) * self.item_height:
            return (y - self.rect[3] + self.scroll_offset) // self.item_height
        return -1

    def get_text(self):
        return self.items[self.selected_index] if self.selected_index >= 0 else "Select"
