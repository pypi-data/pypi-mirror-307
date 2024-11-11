from __future__ import annotations
from typing import Literal, Set, cast

OrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]
ORDER_STATE_VALUES: Set[OrderState] = {"CANCELLED", "FILLED", "PENDING", "TRIGGERED"}


def check_order_state(value: str) -> OrderState:
    if value in ORDER_STATE_VALUES:
        return cast(OrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_STATE_VALUES!r}"
    )
