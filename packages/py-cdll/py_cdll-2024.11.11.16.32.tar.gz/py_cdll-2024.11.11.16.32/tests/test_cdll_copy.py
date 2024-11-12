from src.py_cdll import CDLL


def test_copy_empty_success():
    # Setup
    cdll0: CDLL = CDLL()

    # Execution
    cdll1: CDLL = cdll0.copy()

    # Validation
    assert cdll0 is not cdll1
    assert cdll0 == cdll1


def test_copy_single_value_success():
    # Setup
    data0: str = "data0"
    datas0: list[str] = [data0]
    cdll0: CDLL = CDLL(values=datas0)

    # Execution
    cdll1: CDLL = cdll0.copy()

    # Validation
    assert cdll0 is not cdll1
    assert cdll0 == cdll1


def test_copy_multiple_values_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data3: str = "data3"
    data4: str = "data4"
    datas0: list[str] = [data0, data1, data2, data3, data4]
    cdll0: CDLL = CDLL(values=datas0)

    # Execution
    cdll1: CDLL = cdll0.copy()

    # Validation
    assert cdll0 is not cdll1
    assert cdll0 == cdll1
