from typing import Literal, Set, cast

TakeProfitOrderTransactionReason = Literal["CLIENT_ORDER", "ON_FILL", "REPLACEMENT"]

TAKE_PROFIT_ORDER_TRANSACTION_REASON_VALUES: Set[TakeProfitOrderTransactionReason] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_take_profit_order_transaction_reason(
    value: str,
) -> TakeProfitOrderTransactionReason:
    if value in TAKE_PROFIT_ORDER_TRANSACTION_REASON_VALUES:
        return cast(TakeProfitOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
