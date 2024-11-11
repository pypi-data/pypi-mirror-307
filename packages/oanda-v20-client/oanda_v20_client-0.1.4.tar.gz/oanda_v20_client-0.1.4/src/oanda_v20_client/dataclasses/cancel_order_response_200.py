from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .order_cancel_transaction import OrderCancelTransaction
from typing import List, TypeVar, Union

T = TypeVar("T", bound="CancelOrderResponse200")


@dataclasses.dataclass
class CancelOrderResponse200:
    """Attributes:
    order_cancel_transaction (Union[Unset, OrderCancelTransaction]): An OrderCancelTransaction represents the
        cancellation of an Order in the client's Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order_cancel_transaction: Union[Unset, "OrderCancelTransaction"] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CancelOrderResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
