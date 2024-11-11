from typing import Literal, Set, cast

TakeProfitOrderRequestTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

TAKE_PROFIT_ORDER_REQUEST_TRIGGER_CONDITION_VALUES: Set[
    TakeProfitOrderRequestTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_take_profit_order_request_trigger_condition(
    value: str,
) -> TakeProfitOrderRequestTriggerCondition:
    if value in TAKE_PROFIT_ORDER_REQUEST_TRIGGER_CONDITION_VALUES:
        return cast(TakeProfitOrderRequestTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_REQUEST_TRIGGER_CONDITION_VALUES!r}"
    )
