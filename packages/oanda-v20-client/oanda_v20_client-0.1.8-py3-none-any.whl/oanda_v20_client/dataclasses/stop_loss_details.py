from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .stop_loss_details_time_in_force import StopLossDetailsTimeInForce
from .stop_loss_details_time_in_force import check_stop_loss_details_time_in_force
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="StopLossDetails")


@dataclasses.dataclass
class StopLossDetails:
    """StopLossDetails specifies the details of a Stop Loss Order to be created on behalf of a client. This may happen when
    an Order is filled that opens a Trade requiring a Stop Loss, or when a Trade's dependent Stop Loss Order is modified
    directly through the Trade.

        Attributes:
            price (Union[Unset, str]): The price that the Stop Loss Order will be triggered at. Only one of the price and
                distance fields may be specified.
            distance (Union[Unset, str]): Specifies the distance (in price units) from the Trade's open price to use as the
                Stop Loss Order price. Only one of the distance and price fields may be specified.
            time_in_force (Union[Unset, StopLossDetailsTimeInForce]): The time in force for the created Stop Loss Order.
                This may only be GTC, GTD or GFD.
            gtd_time (Union[Unset, str]): The date when the Stop Loss Order will be cancelled on if timeInForce is GTD.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            guaranteed (Union[Unset, bool]): Flag indicating that the price for the Stop Loss Order is guaranteed. The
                default value depends on the GuaranteedStopLossOrderMode of the account, if it is REQUIRED, the default will be
                true, for DISABLED or ENABLED the default is false."""

    price: Optional[str]
    distance: Optional[str]
    time_in_force: Optional[StopLossDetailsTimeInForce]
    gtd_time: Optional[str]
    client_extensions: Optional["ClientExtensions"]
    guaranteed: Optional[bool]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        price = d.pop("price", None)
        distance = d.pop("distance", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[StopLossDetailsTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_stop_loss_details_time_in_force(_time_in_force)
        gtd_time = d.pop("gtdTime", None)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        guaranteed = d.pop("guaranteed", None)
        stop_loss_details = cls(
            price=price,
            distance=distance,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            client_extensions=client_extensions,
            guaranteed=guaranteed,
        )
        stop_loss_details.additional_properties = d
        return stop_loss_details

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
