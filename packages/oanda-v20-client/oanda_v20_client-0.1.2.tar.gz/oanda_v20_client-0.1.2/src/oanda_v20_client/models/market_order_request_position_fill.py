from typing import Literal, Set, cast

MarketOrderRequestPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]

MARKET_ORDER_REQUEST_POSITION_FILL_VALUES: Set[MarketOrderRequestPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_market_order_request_position_fill(
    value: str,
) -> MarketOrderRequestPositionFill:
    if value in MARKET_ORDER_REQUEST_POSITION_FILL_VALUES:
        return cast(MarketOrderRequestPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REQUEST_POSITION_FILL_VALUES!r}"
    )
