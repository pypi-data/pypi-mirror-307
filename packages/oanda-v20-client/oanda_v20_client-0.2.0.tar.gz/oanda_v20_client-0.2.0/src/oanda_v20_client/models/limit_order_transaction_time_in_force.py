from typing import Literal, Set, cast

LimitOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

LIMIT_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[LimitOrderTransactionTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_limit_order_transaction_time_in_force(
    value: str,
) -> LimitOrderTransactionTimeInForce:
    if value in LIMIT_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(LimitOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
