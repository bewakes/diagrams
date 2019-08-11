import math

from PIL import ImageDraw, ImageFont, Image

from utils import (
    negate,
    add_points,
    strip_horizontal_line,
    strip_vertical_line,
)


class Line:
    type = 'line'

    def __init(self, start, end, width=1, fill=None):
        self.start = start
        self.end = end
        self.fill = fill
        self.width = width


class Arc:
    type = 'arc'

    def __init__(self, center, start, end, fill=None, border=None):
        self.center = center
        self.start = start
        self.end = end
        self.fill = None,
        self.border = None


class Rectangle:
    type = 'rectangle'

    def __init__(self, top_left, bottom_right, fill=None, border=None):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.fill = None
        self.border_width, self.border_color = border


class Text:
    type = 'text'

    def __init__(self, position, size, color='black'):
        self.position = position
        self.color = color
        self.width, self.height = size


class RoundedRectangle:
    type = 'rounded_rectangle'

    def __init__(self, top_left, bottom_right, radius, fill=None, border=None):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.radius = radius
        self.fill = None
        self.border_width, self.border_color = border

        self.width = self.bottom_right[0] - self.top_left[0]
        self.height = self.bottom_right[1] - self.top_left[1]

    def get_primitives(self):
        if hasattr(self, 'primitives'):
            return self.primitives
        # Calculate Primitives
        if self.fill is not None:
            return self._get_filled_primitives()

        self.primitives = self._get_wired_primitives()
        return self.primitives

    def _get_filled_primitives(self):
        raise Exception('NOT IMPLEMENTED')

    def _get_wired_primitives(self):
        """The wired primitives consists of 4 90degree arcs at four corners,
        and four lines"""
        x1, y1 = self.top_left
        x2, y2 = self.bottom_right
        w, h, r = self.width, self.height, self.radius

        lines = [
            # Horizontal lines
            (add_points((x1, y1), (r, 0)), add_points((x2, y1), (-r, 0))),
            (add_points((x1, y2), (r, 0)), add_points((x2, y2), (-r, 0))),
            # Vertical lines
            (add_points((x1, y1), (0, r)), add_points((x1, y2), (0, -r))),
            (add_points((x2, y1), (0, r)), add_points((x2, y2), (0, -r))),
        ]

        # First calculate lines without border radius
        top_line = self.top_left, (x1, y2)
        bottom_line = tuple(add_points(x, (0, h)) for x in top_line)

        left_line = self.top_left, (y1, x2)
        right_line = tuple(add_points(x, (w, 0)) for x in left_line)

        lines = [
            strip_horizontal_line(top_line, r),
            strip_horizontal_line(bottom_line, r),
            strip_vertical_line(left_line, r),
            strip_vertical_line(right_line, r),
        ]

        radius = (r, r)
        # Now get the four arcs
        top_left_center = add_points(self.top_left, radius)
        top_left_angles = (math.PI/2, math.PI)

        top_right_center = add_points(top_left_center, (w - r * 2, 0))
        top_right_angles = (0, math.PI/2)

        bottom_left_center = add_points(top_left_center, (0, h - r * 2))
        bottom_left_angles = (math.PI, 3*math.PI/2)

        bottom_right_center = add_points(self.bottom_right, negate(radius))
        bottom_right_angles = (3*math.PI/2, 2*math.PI)

        arcs = [
            Arc(*args, fill=self.fill, border=self.border) for args in
            [
                (top_left_center, *top_left_angles),
                (top_right_center, *top_right_angles),
                (bottom_left_center, *bottom_left_angles),
                (bottom_right_center, *bottom_right_angles),
            ]
        ]

        return [*lines, *arcs]


def get_text_position(rect_top_left, rect_bottom_right, text_size):
    x1, y1 = rect_top_left
    x2, y2 = rect_bottom_right
    w, h = text_size
    return (x2 - x1 - w) / 2, (y2 - y1 - h) / 2


def draw_rounded_rectangle(top_left, bottom_right, radius, fill=None):
    pass


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
