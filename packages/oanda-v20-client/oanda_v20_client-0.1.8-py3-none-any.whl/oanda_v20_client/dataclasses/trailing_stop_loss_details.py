from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .trailing_stop_loss_details_time_in_force import TrailingStopLossDetailsTimeInForce
from .trailing_stop_loss_details_time_in_force import (
    check_trailing_stop_loss_details_time_in_force,
)
from types import Unset
from typing import Optional, Type, TypeVar

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

    distance: Optional[str]
    time_in_force: Optional[TrailingStopLossDetailsTimeInForce]
    gtd_time: Optional[str]
    client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        distance = d.pop("distance", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[TrailingStopLossDetailsTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_trailing_stop_loss_details_time_in_force(
                _time_in_force
            )
        gtd_time = d.pop("gtdTime", None)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        trailing_stop_loss_details = cls(
            distance=distance,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            client_extensions=client_extensions,
        )
        trailing_stop_loss_details.additional_properties = d
        return trailing_stop_loss_details

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
