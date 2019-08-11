def negate(p):
    return -p[0], -p[1]


def add_points(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


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
