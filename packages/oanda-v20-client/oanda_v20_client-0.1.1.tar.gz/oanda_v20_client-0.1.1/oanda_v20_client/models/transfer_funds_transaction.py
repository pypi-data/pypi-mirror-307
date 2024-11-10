from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transfer_funds_transaction_funding_reason import (
    check_transfer_funds_transaction_funding_reason,
)
from ..models.transfer_funds_transaction_funding_reason import (
    TransferFundsTransactionFundingReason,
)
from ..models.transfer_funds_transaction_type import (
    check_transfer_funds_transaction_type,
)
from ..models.transfer_funds_transaction_type import TransferFundsTransactionType
from typing import Union


T = TypeVar("T", bound="TransferFundsTransaction")


@_attrs_define
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
        account_balance (Union[Unset, str]): The Account's balance after funds are transferred.
    """

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        time = self.time

        user_id = self.user_id

        account_id = self.account_id

        batch_id = self.batch_id

        request_id = self.request_id

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        amount = self.amount

        funding_reason: Union[Unset, str] = UNSET
        if not isinstance(self.funding_reason, Unset):
            funding_reason = self.funding_reason

        comment = self.comment

        account_balance = self.account_balance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if time is not UNSET:
            field_dict["time"] = time
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if account_id is not UNSET:
            field_dict["accountID"] = account_id
        if batch_id is not UNSET:
            field_dict["batchID"] = batch_id
        if request_id is not UNSET:
            field_dict["requestID"] = request_id
        if type is not UNSET:
            field_dict["type"] = type
        if amount is not UNSET:
            field_dict["amount"] = amount
        if funding_reason is not UNSET:
            field_dict["fundingReason"] = funding_reason
        if comment is not UNSET:
            field_dict["comment"] = comment
        if account_balance is not UNSET:
            field_dict["accountBalance"] = account_balance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TransferFundsTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_transfer_funds_transaction_type(_type)

        amount = d.pop("amount", UNSET)

        _funding_reason = d.pop("fundingReason", UNSET)
        funding_reason: Union[Unset, TransferFundsTransactionFundingReason]
        if isinstance(_funding_reason, Unset):
            funding_reason = UNSET
        else:
            funding_reason = check_transfer_funds_transaction_funding_reason(
                _funding_reason
            )

        comment = d.pop("comment", UNSET)

        account_balance = d.pop("accountBalance", UNSET)

        transfer_funds_transaction = cls(
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
            account_balance=account_balance,
        )

        transfer_funds_transaction.additional_properties = d
        return transfer_funds_transaction

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
