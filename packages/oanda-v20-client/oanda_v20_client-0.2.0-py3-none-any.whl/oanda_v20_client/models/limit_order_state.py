from typing import Literal, Set, cast

LimitOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

LIMIT_ORDER_STATE_VALUES: Set[LimitOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_limit_order_state(value: str) -> LimitOrderState:
    if value in LIMIT_ORDER_STATE_VALUES:
        return cast(LimitOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_STATE_VALUES!r}"
    )
