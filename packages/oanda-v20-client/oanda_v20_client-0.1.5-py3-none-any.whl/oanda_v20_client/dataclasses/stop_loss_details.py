from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .stop_loss_details_time_in_force import StopLossDetailsTimeInForce
from typing import TypeVar, Union

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

    price: Union[Unset, str] = UNSET
    distance: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, StopLossDetailsTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    guaranteed: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StopLossDetails":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
