from typing import Literal, Set, cast

TrailingStopLossOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

TRAILING_STOP_LOSS_ORDER_REQUEST_TYPE_VALUES: Set[TrailingStopLossOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_trailing_stop_loss_order_request_type(
    value: str,
) -> TrailingStopLossOrderRequestType:
    if value in TRAILING_STOP_LOSS_ORDER_REQUEST_TYPE_VALUES:
        return cast(TrailingStopLossOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REQUEST_TYPE_VALUES!r}"
    )
