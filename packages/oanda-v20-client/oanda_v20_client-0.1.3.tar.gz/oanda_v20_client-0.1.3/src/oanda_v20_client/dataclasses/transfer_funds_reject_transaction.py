from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .transfer_funds_reject_transaction_funding_reason import (
    TransferFundsRejectTransactionFundingReason,
)
from .transfer_funds_reject_transaction_reject_reason import (
    TransferFundsRejectTransactionRejectReason,
)
from .transfer_funds_reject_transaction_type import TransferFundsRejectTransactionType
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="TransferFundsRejectTransaction")


@dataclasses.dataclass
class TransferFundsRejectTransaction:
    """A TransferFundsRejectTransaction represents the rejection of the transfer of funds in/out of an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TransferFundsRejectTransactionType]): The Type of the Transaction. Always set to
            "TRANSFER_FUNDS_REJECT" in a TransferFundsRejectTransaction.
        amount (Union[Unset, str]): The amount to deposit/withdraw from the Account in the Account's home currency. A
            positive value indicates a deposit, a negative value indicates a withdrawal.
        funding_reason (Union[Unset, TransferFundsRejectTransactionFundingReason]): The reason that an Account is being
            funded.
        comment (Union[Unset, str]): An optional comment that may be attached to a fund transfer for audit purposes
        reject_reason (Union[Unset, TransferFundsRejectTransactionRejectReason]): The reason that the Reject Transaction
            was created"""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, TransferFundsRejectTransactionType] = UNSET
    amount: Union[Unset, str] = UNSET
    funding_reason: Union[Unset, TransferFundsRejectTransactionFundingReason] = UNSET
    comment: Union[Unset, str] = UNSET
    reject_reason: Union[Unset, TransferFundsRejectTransactionRejectReason] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransferFundsRejectTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
