class Node:
    count = 0

    def __init__(self, varname, value, type):
        self.id = Node.count
        Node.count += 1
        self.varname = varname
        self.value = value
        self.type = type
        self.adjacents = []

    def __str__(self):
        return f'{self.id}: {self.varname} -> {self.value}, {self.type}'


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.id_nodes = {x.id: x for x in nodes.values()}

    def __str__(self):
        node_info = 'NODES\n'
        links_info = ''
        for id, node in self.nodes.items():
            node_info += str(node) + '\n'
            links_info += f'{id} -> {node.adjacents}\n'
        return f'{node_info}\nLINKS\n{links_info}'

    def get_node(self, node_id):
        return self.id_nodes[node_id]
