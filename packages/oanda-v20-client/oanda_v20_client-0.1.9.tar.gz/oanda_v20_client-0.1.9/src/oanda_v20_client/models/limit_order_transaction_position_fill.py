from typing import Literal, Set, cast

LimitOrderTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]

LIMIT_ORDER_TRANSACTION_POSITION_FILL_VALUES: Set[LimitOrderTransactionPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_limit_order_transaction_position_fill(
    value: str,
) -> LimitOrderTransactionPositionFill:
    if value in LIMIT_ORDER_TRANSACTION_POSITION_FILL_VALUES:
        return cast(LimitOrderTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
