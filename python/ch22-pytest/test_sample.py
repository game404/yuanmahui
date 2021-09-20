import time

import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


@pytest.mark.slow
def test_mark():
    print("test mark")
    time.sleep(10)
    assert 5 == 5
