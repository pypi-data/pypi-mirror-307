from typing import Literal, Set, cast

StopLossOrderRejectTransactionReason = Literal["CLIENT_ORDER", "ON_FILL", "REPLACEMENT"]

STOP_LOSS_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[
    StopLossOrderRejectTransactionReason
] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_stop_loss_order_reject_transaction_reason(
    value: str,
) -> StopLossOrderRejectTransactionReason:
    if value in STOP_LOSS_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(StopLossOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
