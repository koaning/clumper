from clumper import Clumper


def test_left_join_base_example():
    """Base Example"""
    d1 = [{"a": 1, "b": 1, "d": 1}, {"a": 1, "b": 2, "d": 1}, {"a": 1, "b": 5, "d": 1}]
    d2 = [
        {"b": 1, "c": 1, "d": 2},
        {"b": 2, "c": 2, "d": 2},
        {"b": 2, "c": 20, "d": 20},
    ]
    joined = Clumper(d1).left_join(Clumper(d2), mapping={"b": "b"}).collect()
    expected = [
        {"a": 1, "b": 1, "d": 1, "c": 1, "d_joined": 2},
        {"a": 1, "b": 2, "d": 1, "c": 2, "d_joined": 2},
        {"a": 1, "b": 2, "d": 1, "c": 20, "d_joined": 20},
        {"a": 1, "b": 5, "d": 1},
    ]
    assert joined == expected


def test_left_join_suffix_missing_data():
    """
    Make sure that the left/right suffix appears in the name of the new property 
    when there is data missing.
    """
    d1 = [{"a": 1, "b": 1, "d": 1}, {"a": 1, "b": 2, "d": 1}, {"a": 1, "b": 5, "d": 1}]
    d2 = [
        {"b": 1, "c": 1, "d": 2},
        {"b": 2, "c": 2, "d": 2},
        {"b": 2, "c": 20, "d": 20},
    ]
    joined = (
        Clumper(d1)
        .left_join(Clumper(d2), mapping={"b": "b"}, lsuffix="left", rsuffix="right")
        .collect()
    )
    expected = [
        {"a": 1, "b": 1, "dleft": 1, "c": 1, "dright": 2},
        {"a": 1, "b": 2, "dleft": 1, "c": 2, "dright": 2},
        {"a": 1, "b": 2, "dleft": 1, "c": 20, "dright": 20},
        {"a": 1, "b": 5, "d": 1},
    ]
    assert joined == expected


def test_left_join_suffix_good_match():
    """
    Make sure that the left/right suffix appears in the name of the new property
    when there is no data missing in the join.
    """
    d1 = [{"a": 1, "b": 1, "d": 1}, {"a": 1, "b": 2, "d": 1}, {"a": 1, "b": 5, "d": 1}]
    d2 = [
        {"b": 1, "c": 1, "d": 1},
        {"b": 2, "c": 2, "d": 2},
        {"b": 2, "c": 20, "d": 20},
    ]
    joined = (
        Clumper(d1)
        .left_join(Clumper(d2), mapping={"d": "d"}, lsuffix="left", rsuffix="right")
        .collect()
    )
    expected = [
        {"a": 1, "bleft": 1, "d": 1, "bright": 1, "c": 1},
        {"a": 1, "bleft": 2, "d": 1, "bright": 1, "c": 1},
        {"a": 1, "bleft": 5, "d": 1, "bright": 1, "c": 1},
    ]
    assert joined == expected


def test_left_join_no_overlap():
    """
    When no data is join-able, we shouldn't loose data.
    """
    d1 = [{"a": 1, "b": 1, "d": 1}, {"a": 1, "b": 2, "d": 1}, {"a": 1, "b": 5, "d": 1}]
    d2 = [
        {"b": 1, "c": 1, "d": 100},
        {"b": 2, "c": 2, "d": 200},
        {"b": 2, "c": 20, "d": 200},
    ]
    joined = (
        Clumper(d1)
        .left_join(Clumper(d2), mapping={"d": "d"}, lsuffix="left", rsuffix="right")
        .collect()
    )
    assert joined == d1
