from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .order_client_extensions_modify_reject_transaction_reject_reason import (
    OrderClientExtensionsModifyRejectTransactionRejectReason,
)
from .order_client_extensions_modify_reject_transaction_reject_reason import (
    check_order_client_extensions_modify_reject_transaction_reject_reason,
)
from .order_client_extensions_modify_reject_transaction_type import (
    OrderClientExtensionsModifyRejectTransactionType,
)
from .order_client_extensions_modify_reject_transaction_type import (
    check_order_client_extensions_modify_reject_transaction_type,
)
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="OrderClientExtensionsModifyRejectTransaction")


@dataclasses.dataclass
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
                Reject Transaction was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[OrderClientExtensionsModifyRejectTransactionType]
    order_id: Optional[str]
    client_order_id: Optional[str]
    client_extensions_modify: Optional["ClientExtensions"]
    trade_client_extensions_modify: Optional["ClientExtensions"]
    reject_reason: Optional[OrderClientExtensionsModifyRejectTransactionRejectReason]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[OrderClientExtensionsModifyRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_order_client_extensions_modify_reject_transaction_type(_type)
        order_id = d.pop("orderID", None)
        client_order_id = d.pop("clientOrderID", None)
        _client_extensions_modify = d.pop("clientExtensionsModify", None)
        client_extensions_modify: Optional[ClientExtensions]
        if isinstance(_client_extensions_modify, Unset):
            client_extensions_modify = None
        else:
            client_extensions_modify = ClientExtensions.from_dict(
                _client_extensions_modify
            )
        _trade_client_extensions_modify = d.pop("tradeClientExtensionsModify", None)
        trade_client_extensions_modify: Optional[ClientExtensions]
        if isinstance(_trade_client_extensions_modify, Unset):
            trade_client_extensions_modify = None
        else:
            trade_client_extensions_modify = ClientExtensions.from_dict(
                _trade_client_extensions_modify
            )
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[
            OrderClientExtensionsModifyRejectTransactionRejectReason
        ]
        if isinstance(_reject_reason, Unset):
            reject_reason = None
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
