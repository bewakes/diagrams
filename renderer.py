from PIL import ImageDraw, ImageFont, Image

import shapes
import utils


def render(img, obj):
    draw = ImageDraw.Draw(img)

    if obj.type == 'rectangle':
        draw.rectangle((obj.top_left, obj.bottom_right))

    elif obj.type == 'text':
        draw.text(obj.position, obj.text, font=ImageFont.truetype(obj.font))

    elif obj.type == 'line':
        draw.line(obj.start + obj.end)

    elif obj.type == 'arc':
        x0, y0 = utils.add_points(obj.center, (-obj.radius, -obj.radius))
        x1, y1 = utils.add_points(obj.center, (obj.radius, obj.radius))
        start = utils.rad_to_deg(-obj.end)
        end = utils.rad_to_deg(-obj.start)
        draw.arc((x0, y0, x1, y1), start, end)

    else:
        [render(img, x) for x in obj.primitives]


def render_shapes():
    font = 'Ubuntu-R'
    image_size = (500, 500)
    img = Image.new('RGB', image_size)

    rectangle = shapes.Rectangle((0, 0), (100, 100))
    text = shapes.Text('bibek', (50, 50), font)
    arc = shapes.Arc((300, 20), 50, 0, -3.14/3)

    arrow = shapes.Arrow((400, 400), (450, 150))

    textrect = shapes.TextInRectangle('Pandey', font, (100, 100), padding=20)
    textrrect = shapes.TextInRoundedRectangle('round', font, (200, 380), radius=20, padding=20)
    roundedrect = shapes.RoundedRectangle((150, 150), (300, 340), 10)

    parallelogram = shapes.ParalleloGram((40, 40), (100, 100), slide=-10)
    textinparall = shapes.TextInParallelogram('textpara', font, (300, 400), -15, padding=10)

    render(img, rectangle)
    render(img, text)
    render(img, arc)
    render(img, arrow)
    render(img, textrect)
    render(img, textrrect)
    render(img, roundedrect)
    render(img, parallelogram)
    render(img, textinparall)

    img.save('text.png')


def render_blocks_and_arrows():
    font = 'Ubuntu-R'
    image_size = (500, 500)
    img = Image.new('RGB', image_size)

    par_text = shapes.TextInParallelogram('Side Project', font, (100, 100), 15, padding=10)
    rect_text = shapes.TextInRectangle('Is Fun', font, (300, 100), padding=10)
    round_text = shapes.TextInRoundedRectangle('Life', font, (450, 200), 7)

    arrow1 = shapes.Arrow(par_text.center, rect_text.center)
    arrow2 = shapes.Arrow(round_text.center, rect_text.center)

    [render(img, x) for x in [par_text, rect_text, round_text, arrow1, arrow2]]
    img.save('text.png')


if __name__ == '__main__':
    render_blocks_and_arrows()