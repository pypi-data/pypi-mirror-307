from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
MARKET_IF_TOUCHED_ORDER_TIME_IN_FORCE_VALUES: Set[MarketIfTouchedOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_market_if_touched_order_time_in_force(
    value: str,
) -> MarketIfTouchedOrderTimeInForce:
    if value in MARKET_IF_TOUCHED_ORDER_TIME_IN_FORCE_VALUES:
        return cast(MarketIfTouchedOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
