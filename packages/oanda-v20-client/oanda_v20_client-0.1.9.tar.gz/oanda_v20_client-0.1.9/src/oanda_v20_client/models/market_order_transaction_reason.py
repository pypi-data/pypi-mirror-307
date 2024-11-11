from typing import Literal, Set, cast

MarketOrderTransactionReason = Literal[
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
]

MARKET_ORDER_TRANSACTION_REASON_VALUES: Set[MarketOrderTransactionReason] = {
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
}


def check_market_order_transaction_reason(value: str) -> MarketOrderTransactionReason:
    if value in MARKET_ORDER_TRANSACTION_REASON_VALUES:
        return cast(MarketOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
