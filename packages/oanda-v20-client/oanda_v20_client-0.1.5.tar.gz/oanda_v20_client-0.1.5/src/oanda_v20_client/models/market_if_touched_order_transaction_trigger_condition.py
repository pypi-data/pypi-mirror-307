from typing import Literal, Set, cast

MarketIfTouchedOrderTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

MARKET_IF_TOUCHED_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    MarketIfTouchedOrderTransactionTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_market_if_touched_order_transaction_trigger_condition(
    value: str,
) -> MarketIfTouchedOrderTransactionTriggerCondition:
    if value in MARKET_IF_TOUCHED_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(MarketIfTouchedOrderTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
