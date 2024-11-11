from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .transaction import Transaction
from typing import List, TypeVar, Union

T = TypeVar("T", bound="ReplaceOrderResponse404")


@dataclasses.dataclass
class ReplaceOrderResponse404:
    """Attributes:
    order_cancel_reject_transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies
        properties that are common between all Transaction.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request. Only present if the Account exists.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account. Only
        present if the Account exists.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    order_cancel_reject_transaction: Union[Unset, "Transaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplaceOrderResponse404":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
