from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order import Order
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetOrderResponse200")


@dataclasses.dataclass
class GetOrderResponse200:
    """Attributes:
    order (Union[Unset, Order]): The base Order definition specifies the properties that are common to all Orders.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order: Optional["Order"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order import Order

        d = src_dict.copy()
        _order = d.pop("order", None)
        order: Optional[Order]
        if isinstance(_order, Unset):
            order = None
        else:
            order = Order.from_dict(_order)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_order_response_200 = cls(
            order=order, last_transaction_id=last_transaction_id
        )
        get_order_response_200.additional_properties = d
        return get_order_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
