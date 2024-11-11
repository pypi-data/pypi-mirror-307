from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
TRAILING_STOP_LOSS_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    TrailingStopLossOrderTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_trailing_stop_loss_order_transaction_trigger_condition(
    value: str,
) -> TrailingStopLossOrderTransactionTriggerCondition:
    if value in TRAILING_STOP_LOSS_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(TrailingStopLossOrderTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
