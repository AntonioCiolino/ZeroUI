from PIL import ImageDraw

class DrawableItem:
    def __init__(self, z_order=0):
        self.z_order = z_order

    def draw(self, draw_context):
        raise NotImplementedError("Subclasses should implement this!")

    def notify(self, event_type, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    def draw_3d_border(self, draw_context, rect, bg_color, width=3):
        top_shade_color = self._lighten_color(bg_color, 1.5)
        bottom_shade_color = self._darken_color(bg_color, 0.6)

        # Draw top shade
        draw_context.line([rect[0], rect[1], rect[2], rect[1]], fill=top_shade_color, width=width)
        draw_context.line([rect[0], rect[1], rect[0], rect[3]], fill=top_shade_color, width=width)
        # Draw bottom shade
        draw_context.line([rect[0], rect[3], rect[2], rect[3]], fill=bottom_shade_color, width=width)
        draw_context.line([rect[2], rect[1], rect[2], rect[3]], fill=bottom_shade_color, width=width)

    def _lighten_color(self, color, factor):
        return tuple(min(int(c * factor), 255) for c in color)

    def _darken_color(self, color, factor):
        return tuple(max(int(c * factor), 0) for c in color)
