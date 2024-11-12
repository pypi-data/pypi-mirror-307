from typing import Literal, Set, cast

MarketOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

MARKET_ORDER_TIME_IN_FORCE_VALUES: Set[MarketOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_market_order_time_in_force(value: str) -> MarketOrderTimeInForce:
    if value in MARKET_ORDER_TIME_IN_FORCE_VALUES:
        return cast(MarketOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
