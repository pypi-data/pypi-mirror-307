from typing import Literal, Set, cast

TrailingStopLossOrderRejectTransactionReason = Literal[
    "CLIENT_ORDER", "ON_FILL", "REPLACEMENT"
]

TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[
    TrailingStopLossOrderRejectTransactionReason
] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_trailing_stop_loss_order_reject_transaction_reason(
    value: str,
) -> TrailingStopLossOrderRejectTransactionReason:
    if value in TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(TrailingStopLossOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
