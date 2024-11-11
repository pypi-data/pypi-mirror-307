from typing import Literal, Set, cast

StopOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

STOP_ORDER_STATE_VALUES: Set[StopOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_stop_order_state(value: str) -> StopOrderState:
    if value in STOP_ORDER_STATE_VALUES:
        return cast(StopOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_STATE_VALUES!r}"
    )
