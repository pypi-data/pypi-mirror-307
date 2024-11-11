from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .transfer_funds_transaction_funding_reason import (
    TransferFundsTransactionFundingReason,
)
from .transfer_funds_transaction_type import TransferFundsTransactionType
from typing import TypeVar, Union

T = TypeVar("T", bound="TransferFundsTransaction")


@dataclasses.dataclass
class TransferFundsTransaction:
    """A TransferFundsTransaction represents the transfer of funds in/out of an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TransferFundsTransactionType]): The Type of the Transaction. Always set to "TRANSFER_FUNDS"
            in a TransferFundsTransaction.
        amount (Union[Unset, str]): The amount to deposit/withdraw from the Account in the Account's home currency. A
            positive value indicates a deposit, a negative value indicates a withdrawal.
        funding_reason (Union[Unset, TransferFundsTransactionFundingReason]): The reason that an Account is being
            funded.
        comment (Union[Unset, str]): An optional comment that may be attached to a fund transfer for audit purposes
        account_balance (Union[Unset, str]): The Account's balance after funds are transferred."""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, TransferFundsTransactionType] = UNSET
    amount: Union[Unset, str] = UNSET
    funding_reason: Union[Unset, TransferFundsTransactionFundingReason] = UNSET
    comment: Union[Unset, str] = UNSET
    account_balance: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransferFundsTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
