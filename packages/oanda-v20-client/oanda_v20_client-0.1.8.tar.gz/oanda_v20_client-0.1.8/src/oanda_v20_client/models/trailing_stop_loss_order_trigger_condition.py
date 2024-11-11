from typing import Literal, Set, cast

TrailingStopLossOrderTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

TRAILING_STOP_LOSS_ORDER_TRIGGER_CONDITION_VALUES: Set[
    TrailingStopLossOrderTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_trailing_stop_loss_order_trigger_condition(
    value: str,
) -> TrailingStopLossOrderTriggerCondition:
    if value in TRAILING_STOP_LOSS_ORDER_TRIGGER_CONDITION_VALUES:
        return cast(TrailingStopLossOrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
