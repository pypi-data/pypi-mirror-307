from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .take_profit_details_time_in_force import TakeProfitDetailsTimeInForce
from typing import TypeVar, Union

T = TypeVar("T", bound="TakeProfitDetails")


@dataclasses.dataclass
class TakeProfitDetails:
    """TakeProfitDetails specifies the details of a Take Profit Order to be created on behalf of a client. This may happen
    when an Order is filled that opens a Trade requiring a Take Profit, or when a Trade's dependent Take Profit Order is
    modified directly through the Trade.

        Attributes:
            price (Union[Unset, str]): The price that the Take Profit Order will be triggered at. Only one of the price and
                distance fields may be specified.
            time_in_force (Union[Unset, TakeProfitDetailsTimeInForce]): The time in force for the created Take Profit Order.
                This may only be GTC, GTD or GFD.
            gtd_time (Union[Unset, str]): The date when the Take Profit Order will be cancelled on if timeInForce is GTD.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4."""

    price: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TakeProfitDetailsTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TakeProfitDetails":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
