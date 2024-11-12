from src.py_cdll.node import Node, reverse_order


def test_reverse_order_one_node_success():
    # Setup
    node0: Node = Node(value=None)
    node0.next = node0
    node0.previous = node0

    # Execution
    reversed0: Node = reverse_order(head=node0)

    # Validation
    assert reversed0 is node0
    assert reversed0.next is node0
    assert reversed0.previous is node0


def test_reverse_order_five_nodes_success():
    # Setup
    node0: Node = Node(value=None)
    node1: Node = Node(value=None)
    node2: Node = Node(value=None)
    node3: Node = Node(value=None)
    node4: Node = Node(value=None)
    node0.next = node1
    node1.previous = node0
    node1.next = node2
    node2.previous = node1
    node2.next = node3
    node3.previous = node2
    node3.next = node4
    node4.previous = node3
    node4.next = node0
    node0.previous = node4

    # Execution
    reversed0: Node = reverse_order(head=node0)

    # Validation
    assert reversed0 is node4
    assert reversed0.next is node3
    assert reversed0.next.next is node2
    assert reversed0.next.next.next is node1
    assert reversed0.next.next.next.next is node0
    assert reversed0.next.next.next.next.next is node4
    assert reversed0.previous is node0
    assert reversed0.previous.previous is node1
    assert reversed0.previous.previous.previous is node2
    assert reversed0.previous.previous.previous.previous is node3
    assert reversed0.previous.previous.previous.previous.previous is node4
