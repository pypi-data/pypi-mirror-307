from src.py_cdll import CDLL


def test__length_empty_success():
    # Setup
    cdll0: CDLL = CDLL()

    # Validation
    assert cdll0._length == 0


def test__length_three_items_success():
    # Setup
    data0: int = 0
    data1: int = 1
    data2: int = 2
    datas0: list[int] = [data0, data1, data2]
    cdll0: CDLL = CDLL(values=datas0)

    # Validation
    assert cdll0._length == 3
