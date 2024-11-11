from __future__ import annotations
from typing import Literal, Set, cast

StopLossOrderRejectTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
STOP_LOSS_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    StopLossOrderRejectTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_stop_loss_order_reject_transaction_trigger_condition(
    value: str,
) -> StopLossOrderRejectTransactionTriggerCondition:
    if value in STOP_LOSS_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(StopLossOrderRejectTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
