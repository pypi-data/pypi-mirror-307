from src.py_cdll.node import Node, stitch


def test_stitch_single_node_list_success():
    # Setup
    node0: Node = Node(value=None)
    node0.next = None
    node0.previous = None

    # Verification
    assert node0.next is None
    assert node0.previous is None

    # Execution
    stitch(head=node0, last=node0)

    # Validation
    assert node0.next is node0
    assert node0.previous is node0


def test_stitch_double_node_list_success():
    # Setup
    node0: Node = Node(value=None)
    node1: Node = Node(value=None)
    node0.next = node1
    node0.previous = None
    node1.next = None
    node1.previous = node0

    # Verification
    assert node0.next is node1
    assert node0.previous is None
    assert node1.next is None
    assert node1.previous is node0

    # Execution
    stitch(head=node0, last=node1)

    # Validation
    assert node0.next is node1
    assert node0.previous is node1
    assert node1.next is node0
    assert node1.previous is node0
