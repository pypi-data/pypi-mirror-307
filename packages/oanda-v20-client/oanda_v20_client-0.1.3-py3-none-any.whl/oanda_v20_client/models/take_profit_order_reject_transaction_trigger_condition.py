from typing import Literal, Set, cast

TakeProfitOrderRejectTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

TAKE_PROFIT_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    TakeProfitOrderRejectTransactionTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_take_profit_order_reject_transaction_trigger_condition(
    value: str,
) -> TakeProfitOrderRejectTransactionTriggerCondition:
    if value in TAKE_PROFIT_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(TakeProfitOrderRejectTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
