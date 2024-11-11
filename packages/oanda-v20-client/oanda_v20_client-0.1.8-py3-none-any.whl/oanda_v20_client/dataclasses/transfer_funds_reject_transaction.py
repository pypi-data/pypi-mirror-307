from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .transfer_funds_reject_transaction_funding_reason import (
    TransferFundsRejectTransactionFundingReason,
)
from .transfer_funds_reject_transaction_funding_reason import (
    check_transfer_funds_reject_transaction_funding_reason,
)
from .transfer_funds_reject_transaction_reject_reason import (
    TransferFundsRejectTransactionRejectReason,
)
from .transfer_funds_reject_transaction_reject_reason import (
    check_transfer_funds_reject_transaction_reject_reason,
)
from .transfer_funds_reject_transaction_type import TransferFundsRejectTransactionType
from .transfer_funds_reject_transaction_type import (
    check_transfer_funds_reject_transaction_type,
)
from types import Unset
from typing import Optional, Type, TypeVar

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

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[TransferFundsRejectTransactionType]
    amount: Optional[str]
    funding_reason: Optional[TransferFundsRejectTransactionFundingReason]
    comment: Optional[str]
    reject_reason: Optional[TransferFundsRejectTransactionRejectReason]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[TransferFundsRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_transfer_funds_reject_transaction_type(_type)
        amount = d.pop("amount", None)
        _funding_reason = d.pop("fundingReason", None)
        funding_reason: Optional[TransferFundsRejectTransactionFundingReason]
        if isinstance(_funding_reason, Unset):
            funding_reason = None
        else:
            funding_reason = check_transfer_funds_reject_transaction_funding_reason(
                _funding_reason
            )
        comment = d.pop("comment", None)
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[TransferFundsRejectTransactionRejectReason]
        if isinstance(_reject_reason, Unset):
            reject_reason = None
        else:
            reject_reason = check_transfer_funds_reject_transaction_reject_reason(
                _reject_reason
            )
        transfer_funds_reject_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            amount=amount,
            funding_reason=funding_reason,
            comment=comment,
            reject_reason=reject_reason,
        )
        transfer_funds_reject_transaction.additional_properties = d
        return transfer_funds_reject_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
