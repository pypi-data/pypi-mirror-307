from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .transaction import Transaction
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="CreateOrderResponse404")


@dataclasses.dataclass
class CreateOrderResponse404:
    """Attributes:
    order_reject_transaction (Optional[Transaction]): The base Transaction specification. Specifies properties
        that are common between all Transaction.
    related_transaction_i_ds (Optional[List[str]]): The IDs of all Transactions that were created while
        satisfying the request. Only present if the Account exists.
    last_transaction_id (Optional[str]): The ID of the most recent Transaction created for the Account. Only
        present if the Account exists.
    error_code (Optional[str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Optional[str]): The human-readable description of the error that has occurred."""

    order_reject_transaction: Optional["Transaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .transaction import Transaction

        d = src_dict.copy()
        _order_reject_transaction = d.pop("orderRejectTransaction", None)
        order_reject_transaction: Optional[Transaction]
        if _order_reject_transaction is None:
            order_reject_transaction = None
        else:
            order_reject_transaction = Transaction.from_dict(_order_reject_transaction)
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        create_order_response_404 = cls(
            order_reject_transaction=order_reject_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
            error_code=error_code,
            error_message=error_message,
        )
        return create_order_response_404

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
