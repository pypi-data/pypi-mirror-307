from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .take_profit_details_time_in_force import TakeProfitDetailsTimeInForce
from .take_profit_details_time_in_force import check_take_profit_details_time_in_force
from types import Unset
from typing import Optional, Type, TypeVar

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

    price: Optional[str]
    time_in_force: Optional[TakeProfitDetailsTimeInForce]
    gtd_time: Optional[str]
    client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        price = d.pop("price", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[TakeProfitDetailsTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_take_profit_details_time_in_force(_time_in_force)
        gtd_time = d.pop("gtdTime", None)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        take_profit_details = cls(
            price=price,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            client_extensions=client_extensions,
        )
        take_profit_details.additional_properties = d
        return take_profit_details

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
