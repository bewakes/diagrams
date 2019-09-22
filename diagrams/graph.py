from typing import List, Dict


class Node:
    __slots__ = 'id', 'varname', 'value', 'type', 'adjacents'
    count = 0

    def __init__(self, varname: str, value: str, type: str):
        self.id = Node.count
        Node.count += 1
        self.varname = varname
        self.value = value
        self.type = type
        self.adjacents: List[int] = []

    def __str__(self):
        return f'{self.id}: {self.varname} -> {self.value}, {self.type}'


class Graph:
    __slots__ = 'nodes', 'id_nodes'

    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.id_nodes: Dict[int, Node] = {x.id: x for x in nodes}

    def __str__(self) -> str:
        node_info = 'NODES\n'
        links_info = ''
        for node in self.nodes:
            node_info += str(node) + '\n'
            links_info += f'{node.id} -> {node.adjacents}\n'
        return f'{node_info}\nLINKS\n{links_info}'

    def node_chain(self, node_id: int) -> List[Node]:
        """Return chain of nodes from given node"""
        pass

    def get_node(self, node_id: int) -> Node:
        return self.id_nodes[node_id]
