from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderTransactionReason = Literal["CLIENT_ORDER", "REPLACEMENT"]
MARKET_IF_TOUCHED_ORDER_TRANSACTION_REASON_VALUES: Set[
    MarketIfTouchedOrderTransactionReason
] = {"CLIENT_ORDER", "REPLACEMENT"}


def check_market_if_touched_order_transaction_reason(
    value: str,
) -> MarketIfTouchedOrderTransactionReason:
    if value in MARKET_IF_TOUCHED_ORDER_TRANSACTION_REASON_VALUES:
        return cast(MarketIfTouchedOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
