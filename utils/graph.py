from graph import Graph, Node

from typing import List


def get_node_longest_chain(graph: Graph, node: Node, chain: List[int]) -> List[int]:  # noqa
    longest_chain: List[int] = []

    for adjacant in node.adjacents:
        adj_chain: List[int] = []

        if adjacant in chain:
            continue

        adj_node = graph.get_node(adjacant)
        new_chain = chain + [node.id, adjacant]
        adj_chain = get_node_longest_chain(graph, adj_node, chain + new_chain)

        if len(adj_chain) > len(longest_chain):
            longest_chain = [*adj_chain]

    return [node.id, *longest_chain]
