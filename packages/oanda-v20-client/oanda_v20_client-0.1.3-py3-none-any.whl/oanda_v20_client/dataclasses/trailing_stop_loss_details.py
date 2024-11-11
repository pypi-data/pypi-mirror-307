from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .trailing_stop_loss_details_time_in_force import TrailingStopLossDetailsTimeInForce
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="TrailingStopLossDetails")


@dataclasses.dataclass
class TrailingStopLossDetails:
    """TrailingStopLossDetails specifies the details of a Trailing Stop Loss Order to be created on behalf of a client.
    This may happen when an Order is filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's
    dependent Trailing Stop Loss Order is modified directly through the Trade.

        Attributes:
            distance (Union[Unset, str]): The distance (in price units) from the Trade's fill price that the Trailing Stop
                Loss Order will be triggered at.
            time_in_force (Union[Unset, TrailingStopLossDetailsTimeInForce]): The time in force for the created Trailing
                Stop Loss Order. This may only be GTC, GTD or GFD.
            gtd_time (Union[Unset, str]): The date when the Trailing Stop Loss Order will be cancelled on if timeInForce is
                GTD.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4."""

    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TrailingStopLossDetailsTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrailingStopLossDetails":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
