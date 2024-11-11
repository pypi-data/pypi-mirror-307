from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]
TAKE_PROFIT_ORDER_STATE_VALUES: Set[TakeProfitOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_take_profit_order_state(value: str) -> TakeProfitOrderState:
    if value in TAKE_PROFIT_ORDER_STATE_VALUES:
        return cast(TakeProfitOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_STATE_VALUES!r}"
    )
