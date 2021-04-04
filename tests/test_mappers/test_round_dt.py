import pytest
from clumper import round_dt_str


def test_invalid_format_dt_round_str():
    """Checks that invalid datetime format raises error"""
    with pytest.raises(ValueError):
        round_dt_str("2019-01-01 01:01:59", "minute", "%m/%d/%Y, %H:%M:%S")


@pytest.mark.parametrize(
    "non_rounded_datetime, frequency,rounded_datetime",
    [
        ("2021-04-03 12:20:32.805052", "second", "2021-04-03 12:20:32.000000"),
        ("2021-04-03 12:20:32.805052", "minute", "2021-04-03 12:20:00.000000"),
        ("2021-04-03 12:20:36.805052", "hour", "2021-04-03 12:00:00.000000"),
        ("2021-04-03 12:20:36.805052", "day", "2021-04-03 00:00:00.000000"),
        ("2021-04-03 12:20:36.805052", "month", "2021-03-31 00:00:00.000000"),
    ],
)
def test_round_iso_8601_datetime(non_rounded_datetime, frequency, rounded_datetime):
    assert (
        round_dt_str(non_rounded_datetime, frequency) == rounded_datetime
    ), "Rounded datetime is not correct"
