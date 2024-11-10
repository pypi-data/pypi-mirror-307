from typing import Literal, Set, cast

TakeProfitOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

TAKE_PROFIT_ORDER_TIME_IN_FORCE_VALUES: Set[TakeProfitOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_take_profit_order_time_in_force(value: str) -> TakeProfitOrderTimeInForce:
    if value in TAKE_PROFIT_ORDER_TIME_IN_FORCE_VALUES:
        return cast(TakeProfitOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
