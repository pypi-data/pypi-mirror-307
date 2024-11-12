from src.py_cdll import CDLL
from src.py_cdll.node import Node


def test__node_remove_from_single_success():
    # Setup
    list0: list[int] = [0]
    cdll0: CDLL = CDLL(values=list0)
    node0: Node = cdll0._head

    # Execution
    cdll0._node_remove(target=node0)

    # Validation
    assert len(cdll0) == 0


def test__node_remove_head_from_triple_success():
    # Bug: _node_remove had no check for whether head was being removed, which would invalidate pointer in CDLL
    # and cause infinite loops when trying to find head after that.

    # Setup
    list0: list[int] = [0, 1, 2]
    cdll0: CDLL = CDLL(values=list0)
    node0: Node = cdll0._head

    # Execution
    cdll0._node_remove(target=node0)

    # Validation
    assert len(cdll0) == 2


def test__node_remove_from_multiple_success():
    # Setup
    list0: list[int] = [0, 1, 2, 3, 4]
    cdll0: CDLL = CDLL(values=list0)
    node0: Node = cdll0._head.previous.previous

    # Execution
    cdll0._node_remove(target=node0)

    # Validation
    assert node0 not in cdll0._nodes()
    assert len(cdll0) == 4
