import pytest

from src.py_cdll import NoNewHeadError
from src.py_cdll.node import Node, insert_between, nodes_from_values, equal


def test_insert_between_first_zero_second_one_success():
    # Setup
    head0: Node = nodes_from_values(values=[0])
    head1: Node = nodes_from_values(values=[1])
    head2: Node = nodes_from_values(values=[0, 1])
    before0: Node = head0
    after0: Node = head0.next
    insert0: Node = head1
    remove0: None = None

    # Execution
    removed0: None = insert_between(before=before0, after=after0, insert=insert0)

    # Validation
    assert removed0 is remove0
    assert equal(first=head0, second=head2)


def test_insert_between_first_seven_second_none_success():
    # Setup
    head0: Node = nodes_from_values(values=[7])
    head1: None = None
    head2: Node = nodes_from_values(values=[7])
    before0: Node = head0
    after0: Node = head0.next
    insert0: None = head1

    # Execution
    inserted0: Node = insert_between(before=before0, after=after0, insert=insert0)

    # Validation
    assert inserted0 is insert0
    assert equal(first=head0, second=head2)


def test_insert_between_first_zero_two_second_one_success():
    # Setup
    head0: Node = nodes_from_values(values=[0, 2])
    head1: Node = nodes_from_values(values=[1])
    head2: Node = nodes_from_values(values=[0, 1, 2])
    before0: Node = head0
    after0: Node = head0.next
    insert0: Node = head1
    remove0: None = None

    # Execution
    removed0: None = insert_between(before=before0, after=after0, insert=insert0)

    # Validation
    assert removed0 is remove0
    assert equal(first=head0, second=head2)


def test_insert_between_first_three_nine_second_none_success():
    # Setup
    head0: Node = nodes_from_values(values=[3, 9])
    head1: None = None
    head2: Node = nodes_from_values(values=[3, 9])
    before0: Node = head0
    after0: Node = head0.next
    insert0: None = head1

    # Execution
    inserted0: Node = insert_between(before=before0, after=after0, insert=insert0)

    # Validation
    assert inserted0 is insert0
    assert equal(first=head0, second=head2)


def test_insert_between_first_three_nine_second_none_remove_success():
    # Setup
    head0: Node = nodes_from_values(values=[3, 9])
    head1: None = None
    head2: Node = nodes_from_values(values=[3])
    before0: Node = head0
    after0: Node = head0
    insert0: None = head1
    remove0: Node = head0.next

    # Execution
    removed0: Node = insert_between(before=before0, after=after0, insert=insert0)

    # Validation
    assert removed0 is removed0
    assert equal(first=removed0, second=remove0)
    assert equal(first=head0, second=head2)


def test_insert_between_first_five_twelve_second_two_success():
    # Setup
    head0: Node = nodes_from_values(values=[5, 12])
    head1: Node = nodes_from_values(values=[2])
    head2: Node = nodes_from_values(values=[2, 5, 12])
    before0: Node = head0.previous
    after0: Node = head0
    insert0: Node = head1
    remove0: None = None

    # Execution
    removed0: None = insert_between(before=before0, after=after0, insert=insert0, head=insert0)

    # Validation
    assert removed0 is remove0
    assert equal(first=head1, second=head2)


def test_insert_between_first_five_twelve_second_two_four_success():
    # Setup
    head0: Node = nodes_from_values(values=[5, 12])
    head1: Node = nodes_from_values(values=[2, 4])
    head2: Node = nodes_from_values(values=[2, 4, 5, 12])
    before0: Node = head0.previous
    after0: Node = head0
    insert0: Node = head1
    remove0: None = None

    # Execution
    removed0: None = insert_between(before=before0, after=after0, insert=insert0, head=insert0)

    # Validation
    assert removed0 is remove0
    assert equal(first=head1, second=head2)


def test_insert_between_first_five_twelve_sixteen_twenty_second_none_success():
    # Setup
    head0: Node = nodes_from_values(values=[5, 12, 16, 20])
    head1: None = None
    head2: Node = nodes_from_values(values=[5, 20])
    before0: Node = head0
    after0: Node = head0.previous
    insert0: None = head1
    removed0: Node = nodes_from_values(values=[12, 16])

    # Execution
    inserted0: Node = insert_between(before=before0, after=after0, insert=insert0)

    # Validation
    assert equal(first=inserted0, second=removed0)
    assert equal(first=head0, second=head2)


def test_insert_between_first_three_seven_nine_fifteen_nineteen_second_ten_twelve_two_five_without_head_failure():
    # Setup
    head0: Node = nodes_from_values(values=[3, 7, 9, 15, 19])
    head1: Node = nodes_from_values(values=[10, 12, 2, 5])
    before0: Node = head0.next.next
    after0: Node = before0
    insert0: Node = head1

    # Validation
    with pytest.raises(NoNewHeadError):
        _: Node = insert_between(before=before0, after=after0, insert=insert0)


def test_insert_between_first_three_seven_nine_fifteen_nineteen_second_ten_twelve_two_five_with_head_success():
    # Setup
    head0: Node = nodes_from_values(values=[3, 7, 9, 15, 19])
    head1: Node = nodes_from_values(values=[10, 12, 2, 5])
    head2: Node = nodes_from_values(values=[2, 5, 9, 10, 12])
    head3: Node = head1.previous.previous
    before0: Node = head0.next.next
    after0: Node = before0
    insert0: Node = head1
    removed0: Node = nodes_from_values(values=[15, 19, 3, 7])

    # Execution
    inserted0: Node = insert_between(before=before0, after=after0, insert=insert0, head=head3)

    # Validation
    assert equal(first=inserted0, second=removed0)
    assert equal(first=head3, second=head2)
