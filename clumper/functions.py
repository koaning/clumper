from datetime import datetime, timedelta

SUPPORTED_FREQUENCIES = ["seconds", "minutes", "hours", "days", "months"]


def get_datetime_component(dt: datetime, component: str):
    if component == "seconds":
        return dt.second

    if component == "minutes":
        return dt.minute

    if component == "hours":
        return dt.hour

    if component == "days":
        return dt.day - 1

    if component == "months":
        return dt


def round_dt_str(
    dt_str: str,
    frequency: str,
    dt_format: str = "%Y-%m-%d %H:%M:%S.%f",
):
    """Rounds datetime to the nearest frequency. The default format is assumed to be ISO 8601 datetime format.
    You can specify your own format as well. For simplicity, the timezone is not taken into consideration.

    Args:
        dt_str (str): The datetime in string.
        frequency(str): The frequency to round the datetime.
        dt_format (str, optional): The datetime format. Defaults to ISO 8601 datetime format.


    Raises:
        TypeError: If the given frequency is not suppored

    Returns:
        str: The rounded datetime
    """

    if frequency not in SUPPORTED_FREQUENCIES:
        raise TypeError(
            f"given frequency {frequency} is not supported, please select one from {SUPPORTED_FREQUENCIES}"
        )

    dt = datetime.strptime(dt_str, dt_format)

    frequencies_to_update = {
        SUPPORTED_FREQUENCIES[i]: get_datetime_component(dt, SUPPORTED_FREQUENCIES[i])
        for i in range(SUPPORTED_FREQUENCIES.index(frequency))
    }

    new_dt = dt - timedelta(microseconds=dt.microsecond, **frequencies_to_update)

    return new_dt.strftime(dt_format)
