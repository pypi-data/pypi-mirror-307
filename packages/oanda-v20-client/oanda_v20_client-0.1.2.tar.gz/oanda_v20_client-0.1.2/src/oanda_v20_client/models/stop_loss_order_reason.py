from typing import Literal, Set, cast

StopLossOrderReason = Literal["CLIENT_ORDER", "ON_FILL", "REPLACEMENT"]

STOP_LOSS_ORDER_REASON_VALUES: Set[StopLossOrderReason] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_stop_loss_order_reason(value: str) -> StopLossOrderReason:
    if value in STOP_LOSS_ORDER_REASON_VALUES:
        return cast(StopLossOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REASON_VALUES!r}"
    )
