from __future__ import annotations
from typing import Literal, Set, cast

StopLossOrderRejectTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
STOP_LOSS_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    StopLossOrderRejectTransactionTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_stop_loss_order_reject_transaction_time_in_force(
    value: str,
) -> StopLossOrderRejectTransactionTimeInForce:
    if value in STOP_LOSS_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(StopLossOrderRejectTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
