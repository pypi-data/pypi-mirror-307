from typing import Literal, Set, cast

Direction = Literal["LONG", "SHORT"]

DIRECTION_VALUES: Set[Direction] = {
    "LONG",
    "SHORT",
}


def check_direction(value: str) -> Direction:
    if value in DIRECTION_VALUES:
        return cast(Direction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTION_VALUES!r}")
