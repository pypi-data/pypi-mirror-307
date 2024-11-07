from typing import Any
from inline_snapshot import snapshot 

def test_L2():
    assert 1 == snapshot(1)
    assert 1 == snapshot(1+0)

