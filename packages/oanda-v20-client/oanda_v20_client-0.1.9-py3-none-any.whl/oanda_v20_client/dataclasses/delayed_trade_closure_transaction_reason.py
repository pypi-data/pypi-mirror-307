from __future__ import annotations
from typing import Literal, Set, cast

DelayedTradeClosureTransactionReason = Literal[
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
]
DELAYED_TRADE_CLOSURE_TRANSACTION_REASON_VALUES: Set[
    DelayedTradeClosureTransactionReason
] = {
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
}


def check_delayed_trade_closure_transaction_reason(
    value: str,
) -> DelayedTradeClosureTransactionReason:
    if value in DELAYED_TRADE_CLOSURE_TRANSACTION_REASON_VALUES:
        return cast(DelayedTradeClosureTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DELAYED_TRADE_CLOSURE_TRANSACTION_REASON_VALUES!r}"
    )
