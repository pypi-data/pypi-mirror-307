from typing import Literal, Set, cast

FixedPriceOrderReason = Literal["PLATFORM_ACCOUNT_MIGRATION"]

FIXED_PRICE_ORDER_REASON_VALUES: Set[FixedPriceOrderReason] = {
    "PLATFORM_ACCOUNT_MIGRATION",
}


def check_fixed_price_order_reason(value: str) -> FixedPriceOrderReason:
    if value in FIXED_PRICE_ORDER_REASON_VALUES:
        return cast(FixedPriceOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FIXED_PRICE_ORDER_REASON_VALUES!r}"
    )
