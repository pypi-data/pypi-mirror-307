from typing import Literal, Set, cast

DailyFinancingTransactionAccountFinancingMode = Literal[
    "DAILY", "NO_FINANCING", "SECOND_BY_SECOND"
]

DAILY_FINANCING_TRANSACTION_ACCOUNT_FINANCING_MODE_VALUES: Set[
    DailyFinancingTransactionAccountFinancingMode
] = {
    "DAILY",
    "NO_FINANCING",
    "SECOND_BY_SECOND",
}


def check_daily_financing_transaction_account_financing_mode(
    value: str,
) -> DailyFinancingTransactionAccountFinancingMode:
    if value in DAILY_FINANCING_TRANSACTION_ACCOUNT_FINANCING_MODE_VALUES:
        return cast(DailyFinancingTransactionAccountFinancingMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DAILY_FINANCING_TRANSACTION_ACCOUNT_FINANCING_MODE_VALUES!r}"
    )
