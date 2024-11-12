from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderReason = Literal["CLIENT_ORDER", "ON_FILL", "REPLACEMENT"]
TAKE_PROFIT_ORDER_REASON_VALUES: Set[TakeProfitOrderReason] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_take_profit_order_reason(value: str) -> TakeProfitOrderReason:
    if value in TAKE_PROFIT_ORDER_REASON_VALUES:
        return cast(TakeProfitOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_REASON_VALUES!r}"
    )
