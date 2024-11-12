import pytest

from src.py_cdll import CDLL
from src.py_cdll.node import split_in_middle, Node


def test_split_in_middle_wrong_type_failure():
    # Setup
    node: str = "not a node"

    # Validation
    with pytest.raises(AttributeError):
        # noinspection PyTypeChecker
        split_in_middle(head=node)


def test_split_in_middle_cdll_one_node_success():
    # Setup
    datas0: list[int] = [0]
    cdll0: CDLL = CDLL(values=datas0)
    head0: Node = cdll0._head

    # Execution
    new_head, new_middle = split_in_middle(head=head0)

    # Validation
    assert new_head is head0
    assert new_head.next is head0
    assert new_head.previous is head0
    assert new_middle is head0
    assert new_middle.next is head0
    assert new_middle.previous is head0


def test_split_in_middle_cdll_two_nodes_success():
    # Setup
    datas0: list[int] = [0, 1]
    cdll0: CDLL = CDLL(values=datas0)
    head0: Node = cdll0._head
    last0: Node = head0.next

    # Execution
    new_head, new_middle = split_in_middle(head=head0)

    # Validation
    assert new_head is head0
    assert new_head.next is head0
    assert new_head.previous is head0
    assert new_middle is last0
    assert new_middle.next is last0
    assert new_middle.previous is last0


def test_split_in_middle_cdll_three_nodes_success():
    # Setup
    datas0: list[int] = [0, 1, 2]
    cdll0: CDLL = CDLL(values=datas0)
    head0: Node = cdll0._head
    middle0: Node = head0.next
    last0: Node = head0.previous

    # Execution
    new_head, new_middle = split_in_middle(head=head0)

    # Validation
    assert new_head is head0
    assert new_head.next is middle0
    assert new_head.previous is middle0
    assert new_middle is last0
    assert new_middle.next is last0
    assert new_middle.previous is last0


def test_split_in_middle_cdll_four_nodes_success():
    # Setup
    datas0: list[int] = [0, 1, 2, 3]
    cdll0: CDLL = CDLL(values=datas0)
    head0: Node = cdll0._head
    second0: Node = head0.next
    third0: Node = second0.next
    last0: Node = third0.next

    # Execution
    new_head, new_middle = split_in_middle(head=head0)

    # Validation
    assert new_head is head0
    assert new_head.next is second0
    assert new_head.previous is second0
    assert new_middle is third0
    assert new_middle.next is last0
    assert new_middle.previous is last0


def test_split_in_middle_cdll_seven_nodes_success():
    # Setup
    datas0: list[int] = [0, 1, 2, 3, 4, 5, 6]
    cdll0: CDLL = CDLL(values=datas0)
    head0: Node = cdll0._head
    second0: Node = head0.next
    third0: Node = second0.next
    fourth0: Node = third0.next
    fifth0: Node = fourth0.next
    sixth0: Node = fifth0.next
    last0: Node = sixth0.next

    # Execution
    new_head, new_middle = split_in_middle(head=head0)

    # Validation
    assert new_head is head0
    assert new_head.next is second0
    assert new_head.previous is fourth0
    assert new_middle is fifth0
    assert new_middle.next is sixth0
    assert new_middle.previous is last0
