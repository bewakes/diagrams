import math

from PIL import ImageDraw, ImageFont, Image

from utils import add_points, scale_point, negate


class Line:
    type = 'line'

    def __init__(self, start, end, width=1, fill=None):
        self.start = start
        self.end = end
        self.fill = fill
        self.width = width


class Arc:
    type = 'arc'

    def __init__(self, center, radius, start, end, fill=None, border=None):
        self.center = center
        self.start, self.end = (start, end) if start < end else (end, start)
        self.start = self.start + math.pi * 2
        self.end = self.end + math.pi * 2
        self.radius = radius
        self.fill = None,
        self.border = None


class Rectangle:
    type = 'rectangle'

    def __init__(self, top_left, bottom_right, fill=None, border=(None, None)):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.fill = None
        self.border_width, self.border_color = border


class Text:
    type = 'text'

    def __init__(self, text, position, font, color='black'):
        self.text = text
        self.position = position
        self.color = color
        self.font = font  # STRING


class RoundedRectangle:
    type = 'rounded_rectangle'

    def __init__(self, top_left, bottom_right, radius, fill=None, border=(None, None)):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.radius = radius
        self.fill = None
        self.border_width, self.border_color = border

        self.width = self.bottom_right[0] - self.top_left[0]
        self.height = self.bottom_right[1] - self.top_left[1]

    @property
    def primitives(self):
        if hasattr(self, '_primitives'):
            return self._primitives
        # Calculate Primitives
        if self.fill is not None:
            return self._get_filled_primitives()

        self._primitives = self._get_wired_primitives()
        return self._primitives

    def _get_filled_primitives(self):
        raise Exception('NOT IMPLEMENTED')

    def _get_wired_primitives(self):
        """The wired primitives consists of 4 90degree arcs at four corners,
        and four lines"""
        x1, y1 = self.top_left
        x2, y2 = self.bottom_right
        r = self.radius

        lines = [
            # Horizontal lines
            Line(add_points((x1, y1), (r, 0)), add_points((x2, y1), (-r, 0))),
            Line(add_points((x1, y2), (r, 0)), add_points((x2, y2), (-r, 0))),
            # Vertical lines
            Line(add_points((x1, y1), (0, r)), add_points((x1, y2), (0, -r))),
            Line(add_points((x2, y1), (0, r)), add_points((x2, y2), (0, -r))),
        ]

        # anti clockwise points starting from top right point
        anticw_points_from_top_right = [(x2, y1), (x1, y1), (x1, y2), (x2, y2)]
        # Their differences from center: add them to get corresponding centers
        center_diffs = [(-r, r), (r, r), (r, -r), (-r, -r)]

        # Zipped to add them in loop
        zipped = zip(anticw_points_from_top_right, center_diffs)

        arcs = [
            Arc(
                add_points(x, y),
                r,
                i*math.pi/2, (i+1)*math.pi/2,
                self.fill
            )
            for i, (x, y) in enumerate(zipped)
        ]
        return [*lines, *arcs]


class TextInRectangle:
    type = 'text_in_rectangle'

    # TODO: add other params like fill and border, etc
    def __init__(self, text, font, center, padding=0, wrap=None):
        self.text = text
        self.center = center
        self.font = font
        self.padding = padding  # padding with rect
        self.wrap = None if wrap == 0 else wrap  # width of the wrap

    @property
    def primitives(self):
        if hasattr(self, '_primitives'):
            return self._primitives

        # Calculate rectangle and text size
        font = ImageFont.truetype(self.font)
        text_size = font.getsize(self.text)

        if self.wrap is not None and text_size[0] > self.wrap:
            # TODO: insert the logic here
            pass
        # No wrap, simple logic
        text_size = font.getsize(self.text)  # equivalent to text's top left at origin  # noqa
        half_text_size = scale_point(text_size, 0.5)
        text_position = add_points(self.center, negate(half_text_size))

        pad = self.padding, self.padding
        rect_size = add_points(text_size, pad)

        rect_top_left = add_points(text_position, negate(pad))
        # add padding to bottom point as well
        rect_bottom_right = add_points(
            rect_top_left, (add_points(rect_size, pad))
        )

        self._primitives = [
            Text(self.text, text_position, self.font),
            Rectangle(rect_top_left, rect_bottom_right)
        ]
        return self._primitives


class TextInRoundedRectangle(TextInRectangle):
    def __init__(self, text, font, center, padding=0, radius=5, wrap=None):
        pass


def get_text_position(rect_top_left, rect_bottom_right, text_size):
    x1, y1 = rect_top_left
    x2, y2 = rect_bottom_right
    w, h = text_size
    return (x2 - x1 - w) / 2, (y2 - y1 - h) / 2


def draw_text_inside_rectangle(text, padding=20):
    image_size = (500, 500)
    img = Image.new('RGB', image_size)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype('Ubuntu-R')
    text_size = font.getsize(text)
    rect_size = tuple(x+padding for x in text_size)

    rect_top_left = (0, 0)
    rect_bottom_right = add_points(rect_top_left, rect_size)

    text_pos = get_text_position(rect_top_left, rect_bottom_right, text_size)

    draw.rectangle((rect_top_left, rect_bottom_right))
    draw.text(
        text_pos,
        text,
        font=font
    )

    img.save('text.png')


if __name__ == '__main__':
    draw_text_inside_rectangle('bibek')
