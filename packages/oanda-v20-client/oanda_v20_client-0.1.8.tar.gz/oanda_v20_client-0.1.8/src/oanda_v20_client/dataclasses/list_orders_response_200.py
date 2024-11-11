from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order import Order
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="ListOrdersResponse200")


@dataclasses.dataclass
class ListOrdersResponse200:
    """Attributes:
    orders (Union[Unset, List['Order']]): The list of Order detail objects
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    orders: Optional[List["Order"]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order import Order

        d = src_dict.copy()
        orders = []
        _orders = d.pop("orders", None)
        for orders_item_data in _orders or []:
            orders_item = Order.from_dict(orders_item_data)
            orders.append(orders_item)
        last_transaction_id = d.pop("lastTransactionID", None)
        list_orders_response_200 = cls(
            orders=orders, last_transaction_id=last_transaction_id
        )
        list_orders_response_200.additional_properties = d
        return list_orders_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
