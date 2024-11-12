from typing import Literal, Set, cast

StopOrderTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

STOP_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    StopOrderTransactionTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_stop_order_transaction_trigger_condition(
    value: str,
) -> StopOrderTransactionTriggerCondition:
    if value in STOP_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(StopOrderTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
