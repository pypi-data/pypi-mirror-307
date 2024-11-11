from __future__ import annotations
from typing import Literal, Set, cast

MarketOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
MARKET_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[MarketOrderRequestTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_market_order_request_time_in_force(
    value: str,
) -> MarketOrderRequestTimeInForce:
    if value in MARKET_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(MarketOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
