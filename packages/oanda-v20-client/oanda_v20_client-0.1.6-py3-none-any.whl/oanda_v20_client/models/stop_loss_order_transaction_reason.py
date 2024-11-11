from typing import Literal, Set, cast

StopLossOrderTransactionReason = Literal["CLIENT_ORDER", "ON_FILL", "REPLACEMENT"]

STOP_LOSS_ORDER_TRANSACTION_REASON_VALUES: Set[StopLossOrderTransactionReason] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_stop_loss_order_transaction_reason(
    value: str,
) -> StopLossOrderTransactionReason:
    if value in STOP_LOSS_ORDER_TRANSACTION_REASON_VALUES:
        return cast(StopLossOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
