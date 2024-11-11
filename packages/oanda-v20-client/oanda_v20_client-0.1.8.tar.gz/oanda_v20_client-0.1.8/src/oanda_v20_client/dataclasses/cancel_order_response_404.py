from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_cancel_reject_transaction import OrderCancelRejectTransaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="CancelOrderResponse404")


@dataclasses.dataclass
class CancelOrderResponse404:
    """Attributes:
    order_cancel_reject_transaction (Union[Unset, OrderCancelRejectTransaction]): An OrderCancelRejectTransaction
        represents the rejection of the cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request. Only present if the Account exists.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account. Only
        present if the Account exists.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    order_cancel_reject_transaction: Optional["OrderCancelRejectTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_cancel_reject_transaction import OrderCancelRejectTransaction

        d = src_dict.copy()
        _order_cancel_reject_transaction = d.pop("orderCancelRejectTransaction", None)
        order_cancel_reject_transaction: Optional[OrderCancelRejectTransaction]
        if isinstance(_order_cancel_reject_transaction, Unset):
            order_cancel_reject_transaction = None
        else:
            order_cancel_reject_transaction = OrderCancelRejectTransaction.from_dict(
                _order_cancel_reject_transaction
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        cancel_order_response_404 = cls(
            order_cancel_reject_transaction=order_cancel_reject_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
            error_code=error_code,
            error_message=error_message,
        )
        cancel_order_response_404.additional_properties = d
        return cancel_order_response_404

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
