from src.py_cdll import CDLL
from src.py_cdll.node import Node


def test__node_replace_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    datas0: list[str] = [data0, data1, data2]
    new_node: Node = Node("new_data")
    cdll0: CDLL = CDLL(values=datas0)

    # Execution
    cdll0._node_replace(target=cdll0._head.next, replacement=new_node)

    # Validation
    assert cdll0._head.next is new_node
    assert cdll0._head.next.next.value == data2
    assert cdll0._head.next.previous.value == data0


def test__node_replace_reassign_head_on_overwrite_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    datas0: list[str] = [data0, data1, data2]
    new_node: Node = Node("new_data")
    cdll0: CDLL = CDLL(values=datas0)

    # Execution
    cdll0._node_replace(target=cdll0._head, replacement=new_node)

    # Validation
    assert cdll0._head is new_node
    assert cdll0._head.next.next.value == data2
    assert cdll0._head.previous.value == data2


