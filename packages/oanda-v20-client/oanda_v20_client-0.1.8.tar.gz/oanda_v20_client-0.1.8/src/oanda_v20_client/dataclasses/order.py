from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .order_state import OrderState
from .order_state import check_order_state
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="Order")


@dataclasses.dataclass
class Order:
    """The base Order definition specifies the properties that are common to all Orders.

    Attributes:
        id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
        create_time (Union[Unset, str]): The time when the Order was created.
        state (Union[Unset, OrderState]): The current state of the Order.
        client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
            clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
            your account is associated with MT4."""

    id: Optional[str]
    create_time: Optional[str]
    state: Optional[OrderState]
    client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", None)
        create_time = d.pop("createTime", None)
        _state = d.pop("state", None)
        state: Optional[OrderState]
        if isinstance(_state, Unset):
            state = None
        else:
            state = check_order_state(_state)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        order = cls(
            id=id,
            create_time=create_time,
            state=state,
            client_extensions=client_extensions,
        )
        order.additional_properties = d
        return order

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
