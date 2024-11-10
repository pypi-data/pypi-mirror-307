from typing import Literal, Set, cast

StopOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

STOP_ORDER_TIME_IN_FORCE_VALUES: Set[StopOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_order_time_in_force(value: str) -> StopOrderTimeInForce:
    if value in STOP_ORDER_TIME_IN_FORCE_VALUES:
        return cast(StopOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
