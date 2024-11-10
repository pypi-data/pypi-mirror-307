from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.order_client_extensions_modify_reject_transaction_reject_reason import (
    check_order_client_extensions_modify_reject_transaction_reject_reason,
)
from ..models.order_client_extensions_modify_reject_transaction_reject_reason import (
    OrderClientExtensionsModifyRejectTransactionRejectReason,
)
from ..models.order_client_extensions_modify_reject_transaction_type import (
    check_order_client_extensions_modify_reject_transaction_type,
)
from ..models.order_client_extensions_modify_reject_transaction_type import (
    OrderClientExtensionsModifyRejectTransactionType,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="OrderClientExtensionsModifyRejectTransaction")


@_attrs_define
class OrderClientExtensionsModifyRejectTransaction:
    """A OrderClientExtensionsModifyRejectTransaction represents the rejection of the modification of an Order's Client
    Extensions.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, OrderClientExtensionsModifyRejectTransactionType]): The Type of the Transaction. Always set
                to "ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT" for a OrderClientExtensionsModifyRejectTransaction.
            order_id (Union[Unset, str]): The ID of the Order who's client extensions are to be modified.
            client_order_id (Union[Unset, str]): The original Client ID of the Order who's client extensions are to be
                modified.
            client_extensions_modify (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            trade_client_extensions_modify (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to
                attach a clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this
                field if your account is associated with MT4.
            reject_reason (Union[Unset, OrderClientExtensionsModifyRejectTransactionRejectReason]): The reason that the
                Reject Transaction was created
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, OrderClientExtensionsModifyRejectTransactionType] = UNSET
    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    client_extensions_modify: Union[Unset, "ClientExtensions"] = UNSET
    trade_client_extensions_modify: Union[Unset, "ClientExtensions"] = UNSET
    reject_reason: Union[
        Unset, OrderClientExtensionsModifyRejectTransactionRejectReason
    ] = UNSET
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

        order_id = self.order_id

        client_order_id = self.client_order_id

        client_extensions_modify: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions_modify, Unset):
            client_extensions_modify = self.client_extensions_modify.to_dict()

        trade_client_extensions_modify: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_client_extensions_modify, Unset):
            trade_client_extensions_modify = (
                self.trade_client_extensions_modify.to_dict()
            )

        reject_reason: Union[Unset, str] = UNSET
        if not isinstance(self.reject_reason, Unset):
            reject_reason = self.reject_reason

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
        if order_id is not UNSET:
            field_dict["orderID"] = order_id
        if client_order_id is not UNSET:
            field_dict["clientOrderID"] = client_order_id
        if client_extensions_modify is not UNSET:
            field_dict["clientExtensionsModify"] = client_extensions_modify
        if trade_client_extensions_modify is not UNSET:
            field_dict["tradeClientExtensionsModify"] = trade_client_extensions_modify
        if reject_reason is not UNSET:
            field_dict["rejectReason"] = reject_reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, OrderClientExtensionsModifyRejectTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_order_client_extensions_modify_reject_transaction_type(_type)

        order_id = d.pop("orderID", UNSET)

        client_order_id = d.pop("clientOrderID", UNSET)

        _client_extensions_modify = d.pop("clientExtensionsModify", UNSET)
        client_extensions_modify: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions_modify, Unset):
            client_extensions_modify = UNSET
        else:
            client_extensions_modify = ClientExtensions.from_dict(
                _client_extensions_modify
            )

        _trade_client_extensions_modify = d.pop("tradeClientExtensionsModify", UNSET)
        trade_client_extensions_modify: Union[Unset, ClientExtensions]
        if isinstance(_trade_client_extensions_modify, Unset):
            trade_client_extensions_modify = UNSET
        else:
            trade_client_extensions_modify = ClientExtensions.from_dict(
                _trade_client_extensions_modify
            )

        _reject_reason = d.pop("rejectReason", UNSET)
        reject_reason: Union[
            Unset, OrderClientExtensionsModifyRejectTransactionRejectReason
        ]
        if isinstance(_reject_reason, Unset):
            reject_reason = UNSET
        else:
            reject_reason = (
                check_order_client_extensions_modify_reject_transaction_reject_reason(
                    _reject_reason
                )
            )

        order_client_extensions_modify_reject_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            order_id=order_id,
            client_order_id=client_order_id,
            client_extensions_modify=client_extensions_modify,
            trade_client_extensions_modify=trade_client_extensions_modify,
            reject_reason=reject_reason,
        )

        order_client_extensions_modify_reject_transaction.additional_properties = d
        return order_client_extensions_modify_reject_transaction

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
