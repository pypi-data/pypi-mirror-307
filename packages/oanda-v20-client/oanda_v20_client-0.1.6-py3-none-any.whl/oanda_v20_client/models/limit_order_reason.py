from typing import Literal, Set, cast

LimitOrderReason = Literal["CLIENT_ORDER", "REPLACEMENT"]

LIMIT_ORDER_REASON_VALUES: Set[LimitOrderReason] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_limit_order_reason(value: str) -> LimitOrderReason:
    if value in LIMIT_ORDER_REASON_VALUES:
        return cast(LimitOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REASON_VALUES!r}"
    )
