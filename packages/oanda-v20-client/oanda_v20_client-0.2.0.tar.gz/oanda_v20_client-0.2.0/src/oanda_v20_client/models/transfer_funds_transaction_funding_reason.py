from typing import Literal, Set, cast

TransferFundsTransactionFundingReason = Literal[
    "ACCOUNT_TRANSFER",
    "ADJUSTMENT",
    "CLIENT_FUNDING",
    "DIVISION_MIGRATION",
    "SITE_MIGRATION",
]

TRANSFER_FUNDS_TRANSACTION_FUNDING_REASON_VALUES: Set[
    TransferFundsTransactionFundingReason
] = {
    "ACCOUNT_TRANSFER",
    "ADJUSTMENT",
    "CLIENT_FUNDING",
    "DIVISION_MIGRATION",
    "SITE_MIGRATION",
}


def check_transfer_funds_transaction_funding_reason(
    value: str,
) -> TransferFundsTransactionFundingReason:
    if value in TRANSFER_FUNDS_TRANSACTION_FUNDING_REASON_VALUES:
        return cast(TransferFundsTransactionFundingReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRANSFER_FUNDS_TRANSACTION_FUNDING_REASON_VALUES!r}"
    )
