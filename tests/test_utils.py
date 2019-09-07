from diagrams.utils import intersection_of_lines, cramers_rule


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
