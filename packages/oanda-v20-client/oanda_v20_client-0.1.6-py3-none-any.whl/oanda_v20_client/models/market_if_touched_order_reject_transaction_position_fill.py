from typing import Literal, Set, cast

MarketIfTouchedOrderRejectTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]

MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES: Set[
    MarketIfTouchedOrderRejectTransactionPositionFill
] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_market_if_touched_order_reject_transaction_position_fill(
    value: str,
) -> MarketIfTouchedOrderRejectTransactionPositionFill:
    if value in MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES:
        return cast(MarketIfTouchedOrderRejectTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
