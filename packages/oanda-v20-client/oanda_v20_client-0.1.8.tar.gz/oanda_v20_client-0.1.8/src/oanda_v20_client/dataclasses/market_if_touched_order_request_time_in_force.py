from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
MARKET_IF_TOUCHED_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[
    MarketIfTouchedOrderRequestTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_market_if_touched_order_request_time_in_force(
    value: str,
) -> MarketIfTouchedOrderRequestTimeInForce:
    if value in MARKET_IF_TOUCHED_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(MarketIfTouchedOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
