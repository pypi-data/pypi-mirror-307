from __future__ import annotations
from typing import Literal, Set, cast

MarketOrderRejectTransactionReason = Literal[
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
]
MARKET_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[
    MarketOrderRejectTransactionReason
] = {
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
}


def check_market_order_reject_transaction_reason(
    value: str,
) -> MarketOrderRejectTransactionReason:
    if value in MARKET_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(MarketOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
