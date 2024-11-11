from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
TAKE_PROFIT_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    TakeProfitOrderTransactionTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_take_profit_order_transaction_time_in_force(
    value: str,
) -> TakeProfitOrderTransactionTimeInForce:
    if value in TAKE_PROFIT_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(TakeProfitOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
