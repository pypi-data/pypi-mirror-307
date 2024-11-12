from src.py_cdll.node import Node, remove, nodes_from_values


def test_remove_first_in_two_node_sequence_success():
    # Setup
    head0: Node = nodes_from_values(values=["zero", "one"])
    node0: Node = head0
    node1: Node = head0.next

    # Execution
    removed0: Node = remove(target=node0)

    # Validation
    assert removed0 is node0
    assert node0.next is node0
    assert node0.previous is node0
    assert node1.next is node1
    assert node1.previous is node1


def test_remove_last_in_three_node_sequence_success():
    # Setup
    head0: Node = nodes_from_values(values=["zero", "one", "two"])
    node0: Node = head0
    node1: Node = head0.next
    node2: Node = head0.next.next

    # Execution
    removed0: Node = remove(target=node2)

    # Validation
    assert removed0 is node2
    assert node0.next is node1
    assert node0.previous is node1
    assert node1.next is node0
    assert node1.previous is node0
    assert node2.next is node2
    assert node2.previous is node2


def test_remove_middle_in_five_node_sequence_success():
    # Setup
    head0: Node = nodes_from_values(values=["zero", "one", "two", "three", "four"])
    node0: Node = head0
    node1: Node = head0.next
    node2: Node = head0.next.next
    node3: Node = head0.next.next.next
    node4: Node = head0.next.next.next.next

    # Execution
    removed0: Node = remove(target=node2)

    # Validation
    assert removed0 is node2
    assert node0.next is node1
    assert node0.previous is node4
    assert node1.next is node3
    assert node1.previous is node0
    assert node3.next is node4
    assert node3.previous is node1
    assert node4.next is node0
    assert node4.previous is node3
    assert node2.next is node2
    assert node2.previous is node2
