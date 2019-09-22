import math

from PIL import ImageFont

from utils.geometry import (
    add_points, scale_point,
    negate, rotate_point, distance,
    intersection_of_lines,
)


class Line:
    type = 'line'

    def __init__(self, start, end, width=1, fill=None):
        self.start = start
        self.end = end
        self.fill = fill
        self.width = width

    @property
    def center(self):
        return scale_point(add_points(self.start, self.end), 0.5)


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


class Arrow:
    type = 'arrow'

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def center(self):
        return scale_point(add_points(self.start, self.end), 0.5)

    @property
    def primitives(self):
        if hasattr(self, '_primitives'):
            return self._primitives

        arrow_head_length = 7
        line_dist = distance(self.start, self.end)
        factor = arrow_head_length / line_dist
        # Calculate arrow head lines:
        # - Take a line from end to start, rotate it 30 deg, and clip it
        # - Take a line from end to start, rotate it -30 deg, and clip it
        origin_shifted = add_points(self.start, negate(self.end))
        pos_rotated = rotate_point(origin_shifted, math.pi / 6)
        neg_rotated = rotate_point(origin_shifted, -math.pi / 6)

        p1 = pos_rotated[0] * factor, pos_rotated[1] * factor
        p2 = neg_rotated[0] * factor, neg_rotated[1] * factor
        head1 = add_points(self.end, p1)
        head2 = add_points(self.end, p2)

        return [
            Line(self.start, self.end),  # the main line
            Line(self.end, head1),
            Line(self.end, head2),
        ]


class Rectangle:
    type = 'rectangle'

    def __init__(self, top_left, bottom_right, fill=None, border=(None, None)):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.fill = None
        self.border_width, self.border_color = border

    @property
    def center(self):
        return scale_point(add_points(self.top_left, self.bottom_right), 0.5)


class ParalleloGram:
    type = 'parallelogram'

    def __init__(self, bound_top_left, bound_bottom_right, slide=0, fill=None):
        self.bound_top_left = bound_top_left
        self.bound_bottom_right = bound_bottom_right
        self.slide = slide
        self.fill = fill

    @property
    def center(self):
        return scale_point(
            add_points(self.bound_top_left, self.bound_bottom_right),
            0.5
        )

    @property
    def primitives(self):
        if hasattr(self, '_primitives'):
            return self._primitives

        # calculate primitives
        x1, y1 = self.bound_top_left
        x2, y2 = self.bound_bottom_right
        # TODO: return a polygon instead of lines
        if self.slide < 0:  # slide is towards left
            # bound top_left and bound bottom_right remain the same
            return [
                Line((x1, y1), (x2 + self.slide, y1)),  # Top
                Line((x1 - self.slide, y2), (x2, y2)),  # Bottom
                Line((x1, y1), (x1 - self.slide, y2)),  # Left
                Line((x2 + self.slide, y1), (x2, y2)),  # Right
            ]
        else:  # slide is towards right
            return [
                Line((x1 + self.slide, y1), (x2, y1)),  # Top
                Line((x1, y2), (x2 - self.slide, y2)),  # Bottom
                Line((x1 + self.slide, y1), (x1, y2)),  # Left
                Line((x2, y1), (x2-self.slide, y2)),  # Right
            ]


class Text:
    type = 'text'

    def __init__(self, text, position, font, color='black'):
        self.text = text
        self.position = position
        self.color = color
        self.font = font  # STRING
        self.center = None  # TODO: calculate this


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
    def center(self):
        return scale_point(add_points(self.top_left, self.bottom_right), 0.5)

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

        # TODO: check for case of circle or ellipse

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

    def intersection_from(self, x, y):
        """Calculate border interesection point from given point to center"""
        centers_line = ((x, y), self.center)
        [_, rect] = self.primitives
        (a, b) = rect.top_left
        (c, d) = rect.bottom_right
        # Check with top line
        intersection = intersection_with_polygon(
            [(a, b), (c, b), (c, d), (a, d)],
            centers_line
        )
        # If not intersections, return center
        return intersection or self.center


class TextInRoundedRectangle(TextInRectangle):
    def __init__(self, text, font, center, padding=0, radius=5, wrap=None):
        self.text = text
        self.center = center
        self.radius = radius
        self.font = font
        self.padding = padding  # padding with rect
        self.wrap = None if wrap == 0 else wrap  # width of the wrap

    @property
    def primitives(self):
        if hasattr(self, '_primitives'):
            return self._primitives

        # Get primitives from suepr and modify rectangle to rounded rect
        self._primitives = [
            x if x.type != 'rectangle' else RoundedRectangle(
                x.top_left, x.bottom_right, self.radius)
            for x in super().primitives
        ]
        return self._primitives


def intersection_with_polygon(points, line):
    for side in zip(points, points[1:] + [points[0]]):
        intersection = intersection_of_lines(line, side)
        if intersection:
            return intersection
    return None


class TextInParallelogram:
    type = 'text_in_parallelogram'

    def __init__(self, text, font, center, slide=0, padding=0, wrap=None):
        self.text = text
        self.center = center
        self.font = font
        self.slide = slide
        self.padding = padding
        self.wrap = None if wrap == 0 else wrap

    @property
    def primitives(self):
        if hasattr(self, '_primitives'):
            return self._primitives
        # No wrap, simple Logic

        # Calculate text size
        font = ImageFont.truetype(self.font)
        text_size = font.getsize(self.text)  # equivalent to text's top left at origin  # noqa
        half_text_size = scale_point(text_size, 0.5)
        text_position = add_points(self.center, negate(half_text_size))

        padding = self.padding
        left = text_position[0] - padding - abs(self.slide)
        right = text_position[0] + text_size[0] + padding + abs(self.slide)

        rect_top_left = (left, text_position[1] - padding)
        rect_bottom_right = (right, text_position[1] + text_size[1] + padding)

        self._primitives = [
            Text(self.text, text_position, self.font),
            ParalleloGram(rect_top_left, rect_bottom_right, self.slide)
        ]
        return self._primitives
