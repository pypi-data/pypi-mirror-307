import pytest

from src.py_cdll import CDLL


def test___setitem___index_looping_over_and_replacing_all_success():
    # Setup
    data0: int = 37
    data1: int = 73
    cdll0: CDLL = CDLL(values=[data0, data1])

    # Execution
    for index, _ in enumerate(cdll0):
        cdll0[index] = index

    # Validation
    assert cdll0._head.value == 0
    assert cdll0._last.value == 1
    assert cdll0._head.next is cdll0._last
    assert cdll0._head.previous is cdll0._last


def test___setitem___index_in_range_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    cdll0: CDLL = CDLL(values=[data0])

    # Execution
    cdll0[0] = data1

    # Validation
    assert cdll0._head.value is data1
    assert cdll0._head.next is cdll0._head
    assert cdll0._head.previous is cdll0._head


def test___setitem___index_out_of_range_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    cdll0: CDLL = CDLL(values=[data0])

    # Validation
    with pytest.raises(IndexError):
        cdll0[1] = data1


def test___setitem___index_empty_list_out_of_range_failure():
    # Setup
    data0: str = "data0"
    cdll0: CDLL = CDLL()

    # Validation
    with pytest.raises(IndexError):
        cdll0[0] = data0


def test___setitem___index_negative_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    datas0: list[str] = [data0, data1]
    cdll0: CDLL = CDLL(values=datas0)

    # Verification
    assert cdll0._head.value is data0
    assert cdll0._last.value is data1
    assert cdll0._head.next is cdll0._last
    assert cdll0._head.previous is cdll0._last
    assert cdll0._last.next is cdll0._head
    assert cdll0._last.previous is cdll0._head

    # Execution
    cdll0[-1] = data2

    # Validation
    assert cdll0._head.value is data0
    assert cdll0._last.value is data2
    assert cdll0._head.next is cdll0._last
    assert cdll0._head.previous is cdll0._last
    assert cdll0._last.next is cdll0._head
    assert cdll0._last.previous is cdll0._head
