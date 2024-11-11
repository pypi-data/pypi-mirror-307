from typing import Literal, Set, cast

MarketIfTouchedOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

MARKET_IF_TOUCHED_ORDER_TYPE_VALUES: Set[MarketIfTouchedOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_market_if_touched_order_type(value: str) -> MarketIfTouchedOrderType:
    if value in MARKET_IF_TOUCHED_ORDER_TYPE_VALUES:
        return cast(MarketIfTouchedOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TYPE_VALUES!r}"
    )
