from typing import TypeVar, Iterator, Sequence, Callable

from .exceptions import NotANodeError, NodesNotInSameListError, NoNewHeadError

_T = TypeVar("_T")


class Node:
    """Circular Doubly Linked Node"""

    def __init__(self, value: _T) -> None:
        self.head: Node = self
        self.next: Node = self
        self.previous: Node = self
        self.index: int = 0
        self.value: _T = value

    def __repr__(self) -> str:
        values: list = []

        current: Node = self
        while True:
            values.append(current.value)
            current = current.next
            if not isinstance(current, Node) or current is self:
                break

        string = f"Node{[self.value]}{values[1:]}"
        return string


def nodes_from_values(values: Sequence[_T]) -> Node | None:
    """Create circular doubly linked list of Nodes containing values."""
    values_iterator: Iterator[_T] = iter(values)

    try:
        head: Node | None = Node(value=next(values_iterator))
        current: Node | None = head
    except StopIteration:
        head, current = None, None

    for value in values_iterator:
        node: Node = Node(value=value)
        insert_between(before=current, after=head, insert=node)
        current = current.next

    return head


def nodes(head: Node, callback: Callable[[], Node] | None = None) -> Iterator[Node]:
    current: Node = head
    steps: int = 0

    while True:
        yield current
        current = current.next
        steps += 1

        # Current node no longer in original sequence
        is_node_in_list: bool = current.head is callback() if callback else current.head is head.head

        if not is_node_in_list:
            if callback:
                new_current: Node = callback()
            else:
                new_current: Node = head.head
            for _ in range(steps):
                new_current = new_current.next
            if new_current.index != steps:
                break
            current = new_current

        # Reaching end of sequence
        if current is head:
            break


def length_step(node: Node):
    """
    Count nodes in circular doubly linked sequence by stepping through a full round.
    Necessary in contexts where Node indices are not guaranteed to be correct.
    """

    current: Node = node
    amount: int = 0

    while True:
        amount += 1
        current = current.next
        if current is node:
            break

    return amount


def length(node: Node) -> int:
    """
    Calculates Node amount in circular doubly linked list by index of last Node.
    Assumes Node indices are correct.
    """

    try:
        node.next.previous.value
    except AttributeError as exception:
        raise NotANodeError(f"'{node}' is not a Node, but a '{type(node)}'.") from exception

    return node.head.previous.index + 1


def remove(target: Node) -> Node:
    """
    Requires a minimum length of 2 nodes
    Assumes that target node is in a fully circular doubly linked list.
    """

    head: Node | None = None

    if target is target.head:
        head = target.next

    removed: Node = insert_between(before=target.previous, after=target.next, insert=None, head=head)

    return removed


def equal(first: Node, second: Node) -> bool:
    """Compare nodes from head in two circular doubly linked sequences."""
    equality: bool = True

    first_head: Node = first
    second_head: Node = second

    first_current: Node = first_head
    second_current: Node = second_head

    while True:
        equality &= first_current.value is second_current.value or first_current.value == second_current.value
        equality &= first_current.index == second_current.index
        equality &= first_current.head is first_head and second_current.head is second_head

        if not equality:
            break
        elif first_current.next is first_head and second_current.next is second_head:
            break
        elif first_current.next is first_head and second_current.next is not second_head:
            equality &= False
            break
        elif first_current.next is not first_head and second_current.next is second_head:
            equality &= False
            break

        first_current = first_current.next
        second_current = second_current.next

    return equality


def reverse_order(head: Node) -> Node:
    if head.next is head:
        reversed_sequence: Node = head
    else:
        reversed_sequence: Node = head.previous
        previous_node: Node = head
        current_node: Node = head.previous

        while True:
            old_previous: Node = current_node.previous

            current_node.next = current_node.previous
            current_node.previous = previous_node

            previous_node = current_node
            current_node = old_previous

            if previous_node is head:
                break

    return reversed_sequence


def split_head_from_tail(node: Node) -> tuple[Node, Node | None]:
    first_head: Node = node

    if node.next is node:
        second_head: None = None
    else:
        second_head: Node = node.next
        split(first_head=first_head, second_head=second_head)

    return first_head, second_head


def middle_adjacent(head: Node) -> tuple[Node, Node]:
    """When node amount is uneven, preferentially adds one more node to before than after."""
    slow: Node = head
    fast: Node = head

    while fast.next is not head and fast.next.next is not head:
        slow = slow.next
        fast = fast.next.next

    before_last: Node = slow
    after_head: Node = slow.next

    return before_last, after_head


def stitch(head: Node, last: Node) -> None:
    """Stitch together head and last to make sequence circular."""
    head.previous, last.next = last, head


def split(first_head: Node, second_head: Node) -> None:
    """Split one circular doubly linked list into two."""

    if first_head.head is not second_head.head:
        raise NodesNotInSameListError(f"Nodes have different heads and are thus in different lists.")

    first_last: Node = second_head.previous
    second_last: Node = first_head.previous

    stitch(head=first_head, last=first_last), stitch(head=second_head, last=second_last)

    # TODO: refactor to extract repetitive code
    current: Node = first_head
    index: int = 0
    while True:
        current.head = first_head
        current.index = index

        current = current.next
        index += 1

        if current is first_head:
            break

    current: Node = second_head
    index: int = 0
    while True:
        current.head = second_head
        current.index = index

        current = current.next
        index += 1

        if current is second_head:
            break


def insert_between(before: Node, after: Node, insert: Node | None, head: Node | None = None) -> Node | None:
    """
    Requires a minimum length of 1 node
    When working with 1 node it is always going to assume that it should operate "between itself" and not on itself.
    Allows that insert can have multiple connected nodes.
    Assumes that each input node is in a fully circular doubly linked list.
    """

    if after.index - before.index == 0 and before.index != 0 and head is None:
        # When head is removed or overwritten and no new head has been defined, it is exception time!
        raise NoNewHeadError(f"Expected new head, but none was provided.")

    try:
        if insert is None:
            insert_head: Node = after
            insert_last: Node = before

            if length(node=before.head) == 1 or after.index - before.index == 1:
                processed_sequence_start: None = None
                processed_sequence_end: None = None
            else:
                processed_sequence_start: Node = before.next
                processed_sequence_end: Node = after.previous
        else:
            insert_head: Node = insert
            insert_last: Node = insert.previous

            if (after.index - before.index == 0 or after.index - before.index > 1) and length(node=before) > 1:
                processed_sequence_start: Node = before.next
                processed_sequence_end: Node = after.previous
            else:
                processed_sequence_start: None = None
                processed_sequence_end: None = None
    except AttributeError as exception:
        raise NotANodeError(f"'{insert}' is not a Node, but a '{type(insert)}'.") from exception

    if insert and processed_sequence_start and processed_sequence_end:
        stitch(head=insert_head, last=before), \
            stitch(head=after, last=insert_last), \
            stitch(head=processed_sequence_start, last=processed_sequence_end)
    elif not insert and processed_sequence_start and processed_sequence_end:
        stitch(head=insert_head, last=before), \
            stitch(head=processed_sequence_start, last=processed_sequence_end)
    elif insert:
        stitch(head=insert_head, last=before), \
            stitch(head=after, last=insert_last)
    elif not insert:
        pass
    else:
        raise ValueError(f"Unclear how Node sequences should be re-stitched...")

    # Update head and index in inserted nodes
    if head:
        # Update all nodes
        current: Node = head
        index: int = 0
        while True:
            current.head = head
            current.index = index
            if current.next is head:
                break
            current = current.next
            index += 1
    elif insert or processed_sequence_start:
        # Update only inserted nodes
        current: Node = insert_head
        if length_step(before) == 1:
            current_head: Node = current
        else:
            current_head: Node = current.previous.head

        if current is current_head:
            index: int = 0
        else:
            index: int = current.previous.index + 1

        while True:
            current.head = current_head
            current.index = index
            current = current.next
            if current is before.head:
                break
            index += 1

    if processed_sequence_start and processed_sequence_end:
        # Update removed nodes

        current_index = 0
        current_head = processed_sequence_start
        current: Node = processed_sequence_start
        while True:
            current.head = current_head
            current.index = current_index

            current = current.next

            if current is processed_sequence_start:
                break

            current_index += 1

    return processed_sequence_start


def update_head(node: Node) -> None:
    """Update all Nodes with new head."""
    if node is node.head:
        return

    current: Node = node
    index: int = 0

    while True:
        current.head = node
        current.index = index

        current = current.next
        index += 1

        if current is node:
            break


def before_target(current: Node, head: Node, target: Node) -> Node:
    """
    When last node value is still smaller than target value, then the last node is "before target".
    Assuming pre-sorted sub-lists.
    Assuming first head value is lower than or equal to insert head value.
    """

    while current.next.value <= target.value and current.next is not head:
        current = current.next

    return current


def split_in_middle(head: Node) -> tuple[Node, Node]:
    before_head: Node = head
    _, after_head = middle_adjacent(head=head)

    split(first_head=before_head, second_head=after_head)

    return before_head, after_head


def merge(first: Node, second: Node) -> Node:
    """
    Merge pre-sorted circular doubly linked nodes.
    Moving nodes from second into sorted positions in first.
    Assuming pre-sorted sub-lists.
    """

    if first.value > second.value:
        first, second = second, first

    before_insert: Node = first

    while second is not None:
        insert, second = split_head_from_tail(node=second)
        before_insert = before_target(current=before_insert, head=first, target=insert)
        insert_between(before=before_insert, after=before_insert.next, insert=insert)

    return first


def merge_sort(head: Node) -> Node:
    """Merge-sort implementation for circular doubly linked nodes."""

    if head.next is head:
        # When there is only one value, there is nothing to sort.
        merged_sorted: Node = head
    else:
        first, second = split_in_middle(head=head)
        first_sorted, second_sorted = merge_sort(head=first), merge_sort(head=second)
        merged_sorted: Node = merge(first=first_sorted, second=second_sorted)

    return merged_sorted
