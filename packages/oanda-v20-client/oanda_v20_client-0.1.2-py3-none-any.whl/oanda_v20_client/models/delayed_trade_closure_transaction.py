from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.delayed_trade_closure_transaction_reason import (
    check_delayed_trade_closure_transaction_reason,
)
from ..models.delayed_trade_closure_transaction_reason import (
    DelayedTradeClosureTransactionReason,
)
from ..models.delayed_trade_closure_transaction_type import (
    check_delayed_trade_closure_transaction_type,
)
from ..models.delayed_trade_closure_transaction_type import (
    DelayedTradeClosureTransactionType,
)
from typing import Union


T = TypeVar("T", bound="DelayedTradeClosureTransaction")


@_attrs_define
class DelayedTradeClosureTransaction:
    """A DelayedTradeClosure Transaction is created administratively to indicate open trades that should have been closed
    but weren't because the open trades' instruments were untradeable at the time. Open trades listed in this
    transaction will be closed once their respective instruments become tradeable.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, DelayedTradeClosureTransactionType]): The Type of the Transaction. Always set to
                "DELAYED_TRADE_CLOSURE" for an DelayedTradeClosureTransaction.
            reason (Union[Unset, DelayedTradeClosureTransactionReason]): The reason for the delayed trade closure
            trade_i_ds (Union[Unset, str]): List of Trade ID's identifying the open trades that will be closed when their
                respective instruments become tradeable
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, DelayedTradeClosureTransactionType] = UNSET
    reason: Union[Unset, DelayedTradeClosureTransactionReason] = UNSET
    trade_i_ds: Union[Unset, str] = UNSET
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

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason

        trade_i_ds = self.trade_i_ds

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
        if reason is not UNSET:
            field_dict["reason"] = reason
        if trade_i_ds is not UNSET:
            field_dict["tradeIDs"] = trade_i_ds

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
        type: Union[Unset, DelayedTradeClosureTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_delayed_trade_closure_transaction_type(_type)

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, DelayedTradeClosureTransactionReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = check_delayed_trade_closure_transaction_reason(_reason)

        trade_i_ds = d.pop("tradeIDs", UNSET)

        delayed_trade_closure_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            reason=reason,
            trade_i_ds=trade_i_ds,
        )

        delayed_trade_closure_transaction.additional_properties = d
        return delayed_trade_closure_transaction

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
