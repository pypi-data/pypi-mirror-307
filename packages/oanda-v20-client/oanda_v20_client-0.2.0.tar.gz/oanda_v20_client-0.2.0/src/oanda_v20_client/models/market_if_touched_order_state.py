from typing import Literal, Set, cast

MarketIfTouchedOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

MARKET_IF_TOUCHED_ORDER_STATE_VALUES: Set[MarketIfTouchedOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_market_if_touched_order_state(value: str) -> MarketIfTouchedOrderState:
    if value in MARKET_IF_TOUCHED_ORDER_STATE_VALUES:
        return cast(MarketIfTouchedOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_STATE_VALUES!r}"
    )
