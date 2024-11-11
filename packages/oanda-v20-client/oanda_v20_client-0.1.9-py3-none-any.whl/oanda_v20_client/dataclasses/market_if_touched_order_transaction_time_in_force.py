from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
MARKET_IF_TOUCHED_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    MarketIfTouchedOrderTransactionTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_market_if_touched_order_transaction_time_in_force(
    value: str,
) -> MarketIfTouchedOrderTransactionTimeInForce:
    if value in MARKET_IF_TOUCHED_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(MarketIfTouchedOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
