from __future__ import annotations
from typing import Literal, Set, cast

AcceptDatetimeFormat = Literal["RFC3339", "UNIX"]
ACCEPT_DATETIME_FORMAT_VALUES: Set[AcceptDatetimeFormat] = {"RFC3339", "UNIX"}


def check_accept_datetime_format(value: str) -> AcceptDatetimeFormat:
    if value in ACCEPT_DATETIME_FORMAT_VALUES:
        return cast(AcceptDatetimeFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACCEPT_DATETIME_FORMAT_VALUES!r}"
    )
