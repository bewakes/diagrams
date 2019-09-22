from diagrams.utils.geometry import intersection_of_lines, cramers_rule
from diagrams.graph import Graph, Node

from diagrams.utils.graph import get_node_longest_chain


def test_cramers_rule():
    params1 = 4, -3, 11
    params2 = 6, 5, 7
    soln = (2, -1)
    assert cramers_rule(params1, params2) == soln

    params1 = 3, 5, -7
    params2 = 1, 4, -14
    soln = (6, -5)
    assert cramers_rule(params1, params2) == soln


def test_intersection_of_lines():
    # NOTE: this is not complete
    line1 = ((50, 100), (100, 25))
    line2 = ((75, 50), (100, 50))
    expected = (83.33, 50)
    observed = intersection_of_lines(line1, line2)

    assert expected[0] == round(observed[0], 2)
    assert expected[1] == round(observed[1], 2)


class TestGraphChains:
    def test_node_longest_chain1(self):
        n1 = Node('A', 'valueA', '(')
        n2 = Node('B', 'valueB', '(')
        n3 = Node('C', 'valueC', '(')
        n4 = Node('D', 'valueD', '(')
        n5 = Node('E', 'valueE', '(')
        n6 = Node('F', 'valueF', '(')

        n1.adjacents = [n2.id, n3.id]
        n2.adjacents = [n3.id]
        n3.adjacents = [n4.id, n5.id]
        n4.adjacents = [n5.id]
        n5.adjacents = [n6.id]
        n6.adjacents = [n1.id]  # This introduces cycle

        graph = Graph([n1, n2, n3, n4, n5, n6])
        chain = get_node_longest_chain(graph, n1, [])
        assert isinstance(chain, list)
        expected_chain = [n1.id, n2.id, n3.id, n4.id, n5.id, n6.id]
        assert chain == expected_chain

    def test_node_longest_chain2(self):
        n1 = Node('A', 'valueA', '(')
        n2 = Node('B', 'valueB', '(')
        n3 = Node('C', 'valueC', '(')
        n4 = Node('D', 'valueD', '(')
        n5 = Node('E', 'valueE', '(')
        n6 = Node('F', 'valueF', '(')

        n1.adjacents = [n2.id, n3.id]
        n2.adjacents = [n5.id]
        n3.adjacents = [n4.id]
        n4.adjacents = [n2.id, n6.id]
        n5.adjacents = [n4.id]
        n6.adjacents = []

        graph = Graph([n1, n2, n3, n4, n5, n6])
        chain1 = get_node_longest_chain(graph, n1, [])
        chain2 = get_node_longest_chain(graph, n2, [])
        chain3 = get_node_longest_chain(graph, n3, [])
        chain4 = get_node_longest_chain(graph, n4, [])
        chain5 = get_node_longest_chain(graph, n5, [])
        chain6 = get_node_longest_chain(graph, n6, [])

        assert chain1 == [n1.id, n2.id, n5.id, n4.id, n6.id]
        assert chain2 == [n2.id, n5.id, n4.id, n6.id]
        assert chain3 == [n3.id, n4.id, n2.id, n5.id]
        assert chain4 == [n4.id, n2.id, n5.id]
        assert chain5 == [n5.id, n4.id, n2.id]
        assert chain6 == [n6.id]
