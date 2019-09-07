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


def point_on_line(p, line):
    start, end = line

    # Translate end point and the given point to origin by start
    (ex, ey) = add_points(end, negate(start))
    (px, py) = add_points(p, negate(start))

    if px < 0 or px > ex:
        return False

    if py < 0 or py > ey:
        return False

    return px * ey - ex * py == 0


def intersection_of_lines(line1, line2):
    p1l1, p2l1 = line1
    p1l2, p2l2 = line2

    # Translate l1 to origin by it's first point, and also l2
    np1l1 = negate(p1l1)
    tp2l1 = add_points(p2l1, np1l1)

    tp1l2 = add_points(p1l2, np1l1)
    tp2l2 = add_points(p2l2, np1l1)

    # Check if endpoints touch the line
    if point_on_line(tp1l2, ((0, 0), tp2l1)):
        return p1l2
    if point_on_line(tp2l2, ((0, 0), tp2l1)):
        return p2l2

    # Eqn of translated line1 is p2.y*x - p2.x*y = 0 where p2 is translated second point
    def l1_eqn(x, y):
        return tp2l1[1] * x - tp2l1[0] * y

    # Check if both points of line2 line on same side of line1 (both translated points)
    # If so, there is no intersection
    if l1_eqn(*tp1l2) * l1_eqn(*tp2l2) >= 0:
        return None

    dy_l2 = tp2l2[1] - tp1l2[1]
    dx_l2 = tp2l2[0] - tp1l2[0]
    dy_x1 = dy_l2 * tp1l2[0]
    dx_y1 = dx_l2 * tp1l2[1]

    # Check conditions when line1 is vertical or horizontal
    if tp2l1[0] == 0:  # means vertical
        if dx_l2 == 0:  # means line is also vertical and there are many intersection points
            # Return the line's initial point
            return p1l2 if abs(tp1l2[1]) < abs(tp2l1[1]) else p2l2

        # return intersection when x is zero
        y = (dx_y1 - dy_x1) / dx_l2

        if y * (y - tp2l1[1]) > 0:
            return None
        return add_points((0, y), p1l1)

    if tp2l1[1] == 0:  # means horizontal
        if dy_l2 == 0:  # means line is also vertical and there are many intersection points
            # Return the line's initial point
            return p1l2 if abs(tp1l2[0]) < (tp2l1[0]) else p2l2

        # return intersection when y is zero
        x = (dy_x1 - dx_y1) / dy_l2
        if x * (x - tp2l1[0]) > 0:
            return None
        return add_points((x, 0), p1l1)

    # Final Case when first line is neither horizontal nor vertical
    # Find linear eqn parameters for first line and second line and solve by cramers rule
    params1 = (tp2l1[1], - tp2l1[0], 0)
    params2 = (dy_l2, -dx_l2, dy_x1 - dx_y1)
    x, y = cramers_rule(params1, params2)

    # BOUNDING BOX CHECK
    if x * (x - tp2l1[0]) > 0 or y * (y - tp2l1[1]) > 0:
        return None

    return add_points((x, y), p1l1)


def cramers_rule(params1, params2):
    # works only when determinant is non zero
    a1, b1, c1 = params1
    a2, b2, c2 = params2
    x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
    y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)
    return (x, y)
