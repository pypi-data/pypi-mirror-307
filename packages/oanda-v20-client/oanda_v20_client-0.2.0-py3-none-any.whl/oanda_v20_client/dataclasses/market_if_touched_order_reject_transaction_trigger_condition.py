from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderRejectTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    MarketIfTouchedOrderRejectTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_market_if_touched_order_reject_transaction_trigger_condition(
    value: str,
) -> MarketIfTouchedOrderRejectTransactionTriggerCondition:
    if value in MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(MarketIfTouchedOrderRejectTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
