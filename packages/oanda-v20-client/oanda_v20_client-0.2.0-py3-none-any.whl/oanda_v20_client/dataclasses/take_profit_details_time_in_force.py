from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitDetailsTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
TAKE_PROFIT_DETAILS_TIME_IN_FORCE_VALUES: Set[TakeProfitDetailsTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_take_profit_details_time_in_force(value: str) -> TakeProfitDetailsTimeInForce:
    if value in TAKE_PROFIT_DETAILS_TIME_IN_FORCE_VALUES:
        return cast(TakeProfitDetailsTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_DETAILS_TIME_IN_FORCE_VALUES!r}"
    )
