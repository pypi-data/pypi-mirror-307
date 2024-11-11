from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
LIMIT_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    LimitOrderTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_limit_order_transaction_trigger_condition(
    value: str,
) -> LimitOrderTransactionTriggerCondition:
    if value in LIMIT_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(LimitOrderTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
