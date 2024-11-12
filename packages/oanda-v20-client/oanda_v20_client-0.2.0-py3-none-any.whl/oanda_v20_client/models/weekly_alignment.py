from typing import Literal, Set, cast

WeeklyAlignment = Literal[
    "Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"
]

WEEKLY_ALIGNMENT_VALUES: Set[WeeklyAlignment] = {
    "Friday",
    "Monday",
    "Saturday",
    "Sunday",
    "Thursday",
    "Tuesday",
    "Wednesday",
}


def check_weekly_alignment(value: str) -> WeeklyAlignment:
    if value in WEEKLY_ALIGNMENT_VALUES:
        return cast(WeeklyAlignment, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {WEEKLY_ALIGNMENT_VALUES!r}"
    )
