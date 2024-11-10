from typing import Literal, Set, cast

LimitOrderRequestTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]

LIMIT_ORDER_REQUEST_TRIGGER_CONDITION_VALUES: Set[LimitOrderRequestTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_limit_order_request_trigger_condition(
    value: str,
) -> LimitOrderRequestTriggerCondition:
    if value in LIMIT_ORDER_REQUEST_TRIGGER_CONDITION_VALUES:
        return cast(LimitOrderRequestTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REQUEST_TRIGGER_CONDITION_VALUES!r}"
    )
