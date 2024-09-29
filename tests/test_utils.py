
from osmpkg.utils import first_util


def test_my_function():
    """Tests the first_util function.

    This test verifies that the first_util function correctly computes the sum of two integers.
    It checks a specific case where both integers are 2, expecting the result to be 4.

    """
    assert first_util(2, 2) == 4
