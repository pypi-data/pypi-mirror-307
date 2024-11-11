from typing import Literal, Set, cast

MarketOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

MARKET_ORDER_TYPE_VALUES: Set[MarketOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_market_order_type(value: str) -> MarketOrderType:
    if value in MARKET_ORDER_TYPE_VALUES:
        return cast(MarketOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_TYPE_VALUES!r}"
    )
