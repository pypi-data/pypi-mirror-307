from typing import Literal, Set, cast

StopOrderRejectTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

STOP_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    StopOrderRejectTransactionTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_stop_order_reject_transaction_trigger_condition(
    value: str,
) -> StopOrderRejectTransactionTriggerCondition:
    if value in STOP_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(StopOrderRejectTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
