import pytest

from src.py_cdll import CDLL
from src.py_cdll.exceptions import CDLLAlreadyPopulatedError, UnableToPopulateWithNoValuesError


def test__populate_non_empty_cdll_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    datas0: list[str] = [data0]
    datas1: list[str] = [data1]
    cdll0: CDLL = CDLL(values=datas0)

    # Validation
    with pytest.raises(CDLLAlreadyPopulatedError):
        cdll0._populate(values=datas1)


def test__populate_empty_cdll_with_no_values_failure():
    # Setup
    datas0: list[str] = []
    datas1: list[str] = []
    cdll0: CDLL = CDLL(values=datas0)

    # Validation
    with pytest.raises(UnableToPopulateWithNoValuesError):
        cdll0._populate(values=datas1)


def test__populate_empty_cdll_success():
    # Setup
    data0: str = "data0"
    datas0: list[str] = [data0]
    cdll0: CDLL = CDLL()

    # Execution
    cdll0._populate(values=datas0)

    # Validation
    assert cdll0.head == data0
    assert cdll0._head == cdll0._head.next
    assert cdll0._head == cdll0._head.previous
    assert len(cdll0) == 1
