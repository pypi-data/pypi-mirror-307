from typing import Literal, Set, cast

StopOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

STOP_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[StopOrderRequestTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_order_request_time_in_force(value: str) -> StopOrderRequestTimeInForce:
    if value in STOP_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(StopOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
