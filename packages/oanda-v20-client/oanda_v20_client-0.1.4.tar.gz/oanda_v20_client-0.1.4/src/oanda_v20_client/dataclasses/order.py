from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .order_state import OrderState
from typing import TypeVar, Union

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

    id: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    state: Union[Unset, OrderState] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
