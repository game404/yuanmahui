import pytest


def test_eval():
    assert eval("3+5") == 8
    assert eval("'2'+'4'") == "24"
    assert eval("6*9") == 54


@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("'2'+'4'", "24"),
    ("6*9", 54)
])
def test_eval_1(test_input, expected):
    assert eval(test_input) == expected
