from typing import Literal, Set, cast

StopLossOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

STOP_LOSS_ORDER_STATE_VALUES: Set[StopLossOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_stop_loss_order_state(value: str) -> StopLossOrderState:
    if value in STOP_LOSS_ORDER_STATE_VALUES:
        return cast(StopLossOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_STATE_VALUES!r}"
    )
