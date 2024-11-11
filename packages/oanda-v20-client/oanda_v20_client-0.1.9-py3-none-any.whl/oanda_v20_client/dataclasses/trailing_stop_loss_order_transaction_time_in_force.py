from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
TRAILING_STOP_LOSS_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    TrailingStopLossOrderTransactionTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_trailing_stop_loss_order_transaction_time_in_force(
    value: str,
) -> TrailingStopLossOrderTransactionTimeInForce:
    if value in TRAILING_STOP_LOSS_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(TrailingStopLossOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
