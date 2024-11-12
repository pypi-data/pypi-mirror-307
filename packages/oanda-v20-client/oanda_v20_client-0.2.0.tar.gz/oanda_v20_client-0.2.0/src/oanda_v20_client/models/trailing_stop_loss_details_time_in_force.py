from typing import Literal, Set, cast

TrailingStopLossDetailsTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

TRAILING_STOP_LOSS_DETAILS_TIME_IN_FORCE_VALUES: Set[
    TrailingStopLossDetailsTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_trailing_stop_loss_details_time_in_force(
    value: str,
) -> TrailingStopLossDetailsTimeInForce:
    if value in TRAILING_STOP_LOSS_DETAILS_TIME_IN_FORCE_VALUES:
        return cast(TrailingStopLossDetailsTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_DETAILS_TIME_IN_FORCE_VALUES!r}"
    )
