from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
TAKE_PROFIT_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    TakeProfitOrderTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_take_profit_order_transaction_trigger_condition(
    value: str,
) -> TakeProfitOrderTransactionTriggerCondition:
    if value in TAKE_PROFIT_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(TakeProfitOrderTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
