from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_reject_transaction_reject_reason import (
    OrderCancelRejectTransactionRejectReason,
)
from .order_cancel_reject_transaction_reject_reason import (
    check_order_cancel_reject_transaction_reject_reason,
)
from .order_cancel_reject_transaction_type import OrderCancelRejectTransactionType
from .order_cancel_reject_transaction_type import (
    check_order_cancel_reject_transaction_type,
)
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="OrderCancelRejectTransaction")


@dataclasses.dataclass
class OrderCancelRejectTransaction:
    """An OrderCancelRejectTransaction represents the rejection of the cancellation of an Order in the client's Account.

    Attributes:
        id (Optional[str]): The Transaction's Identifier.
        time (Optional[str]): The date/time when the Transaction was created.
        user_id (Optional[int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Optional[str]): The ID of the Account the Transaction was created for.
        batch_id (Optional[str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Optional[str]): The Request ID of the request which generated the transaction.
        type (Optional[OrderCancelRejectTransactionType]): The Type of the Transaction. Always set to
            "ORDER_CANCEL_REJECT" for an OrderCancelRejectTransaction.
        order_id (Optional[str]): The ID of the Order intended to be cancelled
        client_order_id (Optional[str]): The client ID of the Order intended to be cancelled (only provided if the
            Order has a client Order ID).
        reject_reason (Optional[OrderCancelRejectTransactionRejectReason]): The reason that the Reject Transaction
            was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[OrderCancelRejectTransactionType]
    order_id: Optional[str]
    client_order_id: Optional[str]
    reject_reason: Optional[OrderCancelRejectTransactionRejectReason]

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
        type: Optional[OrderCancelRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_order_cancel_reject_transaction_type(_type)
        order_id = d.pop("orderID", None)
        client_order_id = d.pop("clientOrderID", None)
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[OrderCancelRejectTransactionRejectReason]
        if _reject_reason is None:
            reject_reason = None
        else:
            reject_reason = check_order_cancel_reject_transaction_reject_reason(
                _reject_reason
            )
        order_cancel_reject_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            order_id=order_id,
            client_order_id=client_order_id,
            reject_reason=reject_reason,
        )
        order_cancel_reject_transaction.additional_properties = d
        return order_cancel_reject_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
