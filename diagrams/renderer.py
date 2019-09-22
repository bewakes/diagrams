from PIL import ImageDraw, ImageFont, Image

import shapes
from utils.geometry import add_points, rad_to_deg
from graph import Graph

RENDERFONT = 'Ubuntu-R'


def render_object(img, obj):
    draw = ImageDraw.Draw(img)

    if obj.type == 'rectangle':
        draw.rectangle((obj.top_left, obj.bottom_right))

    elif obj.type == 'text':
        draw.text(obj.position, obj.text, font=ImageFont.truetype(obj.font))

    elif obj.type == 'line':
        draw.line(obj.start + obj.end)

    elif obj.type == 'arc':
        x0, y0 = add_points(obj.center, (-obj.radius, -obj.radius))
        x1, y1 = add_points(obj.center, (obj.radius, obj.radius))
        start = rad_to_deg(-obj.end)
        end = rad_to_deg(-obj.start)
        draw.arc((x0, y0, x1, y1), start, end)

    else:
        [render_object(img, x) for x in obj.primitives]


class GraphRenderer:
    def __init__(self, graph: Graph, img_width: int, img_height: int):
        self.graph = graph
        self.rendered_nodes: dict = {}
        self.rendered_links: dict = {}
        self.width = img_width
        self.height = img_height
        self.img = None

    def render_chain(self, node):
        if node.id not in self.rendered_nodes:
            obj = get_render_shape(node)
            obj.center = (100, 50 + 100*len(self.rendered_nodes))
            render_object(self.img, obj)
            self.rendered_nodes[node.id] = obj
        obj = self.rendered_nodes[node.id]

        # Render linked nodes and links
        for adj in node.adjacents:
            if adj not in self.rendered_nodes:
                adjnode = self.graph.get_node(adj)
                adjobj = get_render_shape(adjnode)
                adjobj.center = (100, 50 + 100*len(self.rendered_nodes))
                render_object(self.img, adjobj)
                self.rendered_nodes[adj] = adjobj
            adjobj = self.rendered_nodes[adj]

            # Create link
            arr_start = obj.intersection_from(*adjobj.center)
            arr_end = adjobj.intersection_from(*obj.center)
            arrow = shapes.Arrow(arr_start, arr_end)
            render_object(self.img, arrow)

            # Update rendered links
            self.rendered_links[node.id] = {
                * self.rendered_links.get(node.id, set()),
                adj
            }

    def render(self):
        self.img = Image.new('RGB', (self.width, self.height))

        for node in self.graph.nodes:
            self.render_chain(node)

    def save_to(self, filename):
        self.img.save(filename)
        print(f'IMAGE SAVED TO {filename}')


def get_render_shape(node):
    node_center = (0, 0)
    padding = 20
    args = (RENDERFONT, node_center)

    if node.type == '/':
        return shapes.TextInParallelogram(node.value, *args, -15, padding)
    elif node.type == '[':
        return shapes.TextInRectangle(node.value, *args, padding)
    elif node.type == '(':
        return shapes.TextInRoundedRectangle(node.value, *args, radius=20, padding=padding)
    # DEFAULT Rectangle
    return shapes.TextInRectangle(node.value, *args, padding)


def main():
    from parser import parse
    with open('diagram.dsl') as f:
        graph = parse(f.read())
        w = 500
        h = 500
        filename = '/tmp/text.png'

        renderer = GraphRenderer(graph, w, h)
        renderer.render()
        renderer.save_to(filename)


if __name__ == '__main__':
    main()
