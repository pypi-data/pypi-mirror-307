from typing import Literal, Set, cast

AccountSummaryGuaranteedStopLossOrderMode = Literal["ALLOWED", "DISABLED", "REQUIRED"]

ACCOUNT_SUMMARY_GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES: Set[
    AccountSummaryGuaranteedStopLossOrderMode
] = {
    "ALLOWED",
    "DISABLED",
    "REQUIRED",
}


def check_account_summary_guaranteed_stop_loss_order_mode(
    value: str,
) -> AccountSummaryGuaranteedStopLossOrderMode:
    if value in ACCOUNT_SUMMARY_GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES:
        return cast(AccountSummaryGuaranteedStopLossOrderMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACCOUNT_SUMMARY_GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES!r}"
    )
