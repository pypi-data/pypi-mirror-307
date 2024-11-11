from typing import Literal, Set, cast

MarketOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

MARKET_ORDER_STATE_VALUES: Set[MarketOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_market_order_state(value: str) -> MarketOrderState:
    if value in MARKET_ORDER_STATE_VALUES:
        return cast(MarketOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_STATE_VALUES!r}"
    )
