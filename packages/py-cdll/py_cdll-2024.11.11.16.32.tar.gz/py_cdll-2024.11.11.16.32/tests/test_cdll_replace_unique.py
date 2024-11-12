import pytest

from src.py_cdll import CDLL, ValueNotFoundError, MultipleValuesFoundError


def test_replace_unique_present_success():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data_new: str = "data_new"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Execution
    list0.replace_unique(value=data1, replacement=data_new)

    # Validation
    assert list0[1] is data_new


def test_replace_unique_not_present_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data_find: str = "data_find"
    data_new: str = "data_new"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(ValueNotFoundError):
        list0.replace_unique(value=data_find, replacement=data_new)


def test_replace_unique_multiple_options_failure():
    # Setup
    data0: str = "data0"
    data1: str = "data1"
    data2: str = "data2"
    data_new: str = "data_new"
    list0: CDLL = CDLL()
    list0.append(data0)
    list0.append(data1)
    list0.append(data1)
    list0.append(data2)

    # Validation
    with pytest.raises(MultipleValuesFoundError):
        list0.replace_unique(value=data1, replacement=data_new)
