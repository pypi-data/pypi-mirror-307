from typing import Literal, Set, cast

LimitOrderRequestPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]

LIMIT_ORDER_REQUEST_POSITION_FILL_VALUES: Set[LimitOrderRequestPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_limit_order_request_position_fill(
    value: str,
) -> LimitOrderRequestPositionFill:
    if value in LIMIT_ORDER_REQUEST_POSITION_FILL_VALUES:
        return cast(LimitOrderRequestPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REQUEST_POSITION_FILL_VALUES!r}"
    )
