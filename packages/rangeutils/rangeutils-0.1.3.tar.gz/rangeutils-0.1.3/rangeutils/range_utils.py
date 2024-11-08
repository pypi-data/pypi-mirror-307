import numpy as np


def _trim_array(vect: np.ndarray, percentage: float = None, limit: int | tuple[int, int] = None, axis: int = 0) -> np.ndarray:
    """
    Trims an array based on percentage or fixed limits along a specified axis.

    Input:
        - vect: array (n x axis)
        - percentage: percentage of data to remove from both ends (0 ~ 0.5)
        - limit: minimum (and optionally maximum) number of elements to remove from both ends
        - axis: the axis along which to trim the array

    Output:
        - trimmed_arr: trimmed array
    """

    if percentage is None and limit is None:
        return vect

    minlens, maxlens = None, None
    if limit is not None:
        if isinstance(limit, int):
            minlens = limit
        else:
            minlens, maxlens = limit

    bound = 0

    if percentage is not None:
        assert percentage >= 0 and percentage < 0.5
        bound = int(vect.shape[axis] * percentage)
        if maxlens is not None and bound > maxlens:
            bound = maxlens

    if minlens is not None and bound < minlens:
        bound = minlens

    if vect.ndim == 1:
        return vect[bound:-bound]

    trimmed_arr = vect[bound:-bound, :] if axis == 0 else vect[:, bound:-bound]

    return trimmed_arr


def list_to_range(irange: list[int], maxlens: int = None) -> range | None:
    """
    Converts a list specifying a range to a Python range object.

    Input:
        - irange: [start, end] list. Defaults to [0, maxlens] if elements are None
        - maxlens: maximum length if end is None

    Output:
        - range: range object from start to end
    """

    if irange is not None:
        return range(0, maxlens) if maxlens else None
    elif len(irange) < 2:
        return None

    start = irange[0] if irange[0] is not None else 0
    end = irange[1] if irange[1] is not None else maxlens
    if end is None:
        return None

    return range(int(start), int(end))


def boolist_to_ranges(boolist: list[int | bool], minlens: int = 1) -> list[range]:
    """
    Converts a boolean list to a list of range objects representing True(1) sequences.

    Input:
        - boolist: boolean list
        - minlens: minimum range length

    Output:
        - ranges: list of range objects for True sequences
    """

    indices = np.where(boolist)[0]
    subarrays = np.split(indices, np.where(np.diff(indices) != 1)[0] + 1)
    ranges = [range(idx[0], idx[-1] + 1) for idx in subarrays if len(idx) >= minlens]

    return ranges


def ranges_to_boolist(ranges: list[range], length: int = None) -> list[int]:
    """
    Converts a list of ranges to a boolean list.

    Input:
        - ranges: list of range objects
        - length: length of the resulting boolean list

    Output:
        - boolist: boolean list representing the ranges
    """
    length = length or ranges[-1].stop
    boolist = np.zeros(length, dtype=int)
    for r in ranges:
        boolist[r] = 1

    return boolist.tolist()


def flip(ranges: list[range], head: int = 0, tail: int = None) -> list[range]:
    """
    Generates complementary ranges not covered by the input ranges.

    Input:
        - ranges: list of range objects
        - head: start value of the total range
        - tail: end value of the total range

    Output:
        - ranges: list of complementary range objects
    """

    new_ranges = []

    if ranges[0].start > head:
        new_ranges.append(range(head, ranges[0].start))

    for k in range(1, len(ranges)):
        new_ranges.append(range(ranges[k - 1].stop, ranges[k].start))

    if tail and ranges[-1].stop < tail:
        new_ranges.append(range(ranges[-1].stop, tail))

    return new_ranges


def fill(ranges: list[range], gapsize: int | tuple[int, int] = 1) -> list[range]:
    """
    Fills ranges that are within max_gap distance from each other.

    Input:
        - ranges: list of range objects
        - gapsize: maximum allowed gap between ranges to be filled

    Output:
        - ranges: list of filled range objects
    """

    if not ranges:
        return []

    mingap, maxgap = (0, gapsize) if isinstance(gapsize, int) else gapsize
    merged_ranges = [ranges[0]]

    for current in ranges[1:]:
        previous = merged_ranges[-1]
        gap = current.start - previous.stop
        if mingap <= gap <= maxgap:
            merged_ranges[-1] = range(previous.start, current.stop)
        else:
            merged_ranges.append(current)

    return merged_ranges


def trim(
    ranges: list[range], minlens: int = 1, percentage: float = None, trimsize: int | tuple[int, int] = None
) -> list[range]:
    """
    Trims ranges based on minimum length, percentage, or specific trim sizes.

    Input:
        - ranges: list of range objects
        - minlens: minimum range length
        - percentage: percentage of data to remove
        - trimsize: fixed number of elements to remove from both ends

    Output:
        - trimmed ranges
    """

    rs = []
    for r in ranges:
        r = _trim_array(np.array(r), percentage=percentage, limit=trimsize)
        if len(r) >= minlens:
            rs.append(range(r[0], r[-1] + 1))

    return rs
