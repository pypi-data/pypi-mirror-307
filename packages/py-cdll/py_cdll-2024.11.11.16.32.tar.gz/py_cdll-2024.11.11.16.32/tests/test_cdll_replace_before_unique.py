import pytest

from src.py_cdll import CDLL, NoAdjacentValueError


def test_replace_before_unique_overwrite_success():
    # Setup
    data: str = "data"
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0.replace_before_unique(value=data0, replacement=data)

    # Validation
    assert list0.before_unique(data0) is data


def test_replace_before_unique_single_entry_list_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    list0: CDLL = CDLL()
    list0.append(data0)

    # Validation
    with pytest.raises(NoAdjacentValueError):
        list0.replace_before_unique(value=data0, replacement=data1)
