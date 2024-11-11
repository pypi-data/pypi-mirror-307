from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_transaction_reason import OrderCancelTransactionReason
from .order_cancel_transaction_reason import check_order_cancel_transaction_reason
from .order_cancel_transaction_type import OrderCancelTransactionType
from .order_cancel_transaction_type import check_order_cancel_transaction_type
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="OrderCancelTransaction")


@dataclasses.dataclass
class OrderCancelTransaction:
    """An OrderCancelTransaction represents the cancellation of an Order in the client's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, OrderCancelTransactionType]): The Type of the Transaction. Always set to "ORDER_CANCEL" for
            an OrderCancelTransaction.
        order_id (Union[Unset, str]): The ID of the Order cancelled
        client_order_id (Union[Unset, str]): The client ID of the Order cancelled (only provided if the Order has a
            client Order ID).
        reason (Union[Unset, OrderCancelTransactionReason]): The reason that the Order was cancelled.
        replaced_by_order_id (Union[Unset, str]): The ID of the Order that replaced this Order (only provided if this
            Order was cancelled for replacement)."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[OrderCancelTransactionType]
    order_id: Optional[str]
    client_order_id: Optional[str]
    reason: Optional[OrderCancelTransactionReason]
    replaced_by_order_id: Optional[str]

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
        type: Optional[OrderCancelTransactionType]
        if _type is None:
            type = None
        else:
            type = check_order_cancel_transaction_type(_type)
        order_id = d.pop("orderID", None)
        client_order_id = d.pop("clientOrderID", None)
        _reason = d.pop("reason", None)
        reason: Optional[OrderCancelTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_order_cancel_transaction_reason(_reason)
        replaced_by_order_id = d.pop("replacedByOrderID", None)
        order_cancel_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            order_id=order_id,
            client_order_id=client_order_id,
            reason=reason,
            replaced_by_order_id=replaced_by_order_id,
        )
        order_cancel_transaction.additional_properties = d
        return order_cancel_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
