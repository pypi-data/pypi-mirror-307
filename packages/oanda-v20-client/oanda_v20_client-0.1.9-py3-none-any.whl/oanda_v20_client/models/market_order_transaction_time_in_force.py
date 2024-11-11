from typing import Literal, Set, cast

MarketOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

MARKET_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    MarketOrderTransactionTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_market_order_transaction_time_in_force(
    value: str,
) -> MarketOrderTransactionTimeInForce:
    if value in MARKET_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(MarketOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
