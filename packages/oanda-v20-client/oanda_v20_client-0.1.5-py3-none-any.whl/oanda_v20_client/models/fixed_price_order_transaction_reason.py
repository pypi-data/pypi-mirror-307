from typing import Literal, Set, cast

FixedPriceOrderTransactionReason = Literal["PLATFORM_ACCOUNT_MIGRATION"]

FIXED_PRICE_ORDER_TRANSACTION_REASON_VALUES: Set[FixedPriceOrderTransactionReason] = {
    "PLATFORM_ACCOUNT_MIGRATION",
}


def check_fixed_price_order_transaction_reason(
    value: str,
) -> FixedPriceOrderTransactionReason:
    if value in FIXED_PRICE_ORDER_TRANSACTION_REASON_VALUES:
        return cast(FixedPriceOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FIXED_PRICE_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
