from typing import Literal, Set, cast

TrailingStopLossOrderRequestTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

TRAILING_STOP_LOSS_ORDER_REQUEST_TRIGGER_CONDITION_VALUES: Set[
    TrailingStopLossOrderRequestTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_trailing_stop_loss_order_request_trigger_condition(
    value: str,
) -> TrailingStopLossOrderRequestTriggerCondition:
    if value in TRAILING_STOP_LOSS_ORDER_REQUEST_TRIGGER_CONDITION_VALUES:
        return cast(TrailingStopLossOrderRequestTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REQUEST_TRIGGER_CONDITION_VALUES!r}"
    )
