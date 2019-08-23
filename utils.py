import math

cos = math.cos
sin = math.sin


def negate(p):
    return -p[0], -p[1]


def distance(p1, p2):
    a, b = p1
    c, d = p2
    return ((c - a) ** 2 + (d - b) ** 2) ** 0.5


def add_points(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def rotate_point(p, angle):
    x, y = p
    return x * cos(angle) - y * sin(angle), y * cos(angle) + x * sin(angle)


def scale_point(p, f):
    return p[0] * f, p[1] * f


def strip_horizontal_line(line, strip_width):
    """Strips a horizontal line both sides"""
    start, end = line
    strip = (strip_width, 0)

    if start[0] >= end[0]:
        # Line is right to left
        # So, subtract strip from start's x and add strip to end's x
        return add_points(start, negate(strip)), add_points(end, strip)
    else:
        return add_points(start, strip), add_points(end, negate(strip))


def strip_vertical_line(line, strip_width):
    """Strips a vertical line both sides"""
    # NOTE: y increases from top to bottom unlike normal math graphs
    start, end = line
    strip = (0, strip_width)

    if start[1] >= end[1]:
        # Line is bottom to up
        # So, subtract strip from start's y and add strip to end's y
        return add_points(start, negate(strip)), add_points(end, strip)
    else:
        return add_points(start, strip), add_points(end, negate(strip))


def rad_to_deg(rad):
    return 180 * rad / math.pi


def string_hash(string):
    prime = 307  # this is arbritrary prime
    m = 87178291199  # also arbitrary
    s = 0
    for i, chr in enumerate(string):
        val = ord(chr)
        s += val * (prime ** i)
    return s % m
