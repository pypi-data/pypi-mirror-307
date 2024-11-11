from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .price_bucket import PriceBucket
from typing import List, TypeVar, Union

T = TypeVar("T", bound="Price")


@dataclasses.dataclass
class Price:
    """The Price representation

    Attributes:
        instrument (Union[Unset, str]): The Price's Instrument.
        tradeable (Union[Unset, bool]): Flag indicating if the Price is tradeable or not
        timestamp (Union[Unset, str]): The date/time when the Price was created.
        base_bid (Union[Unset, str]): The base bid price as calculated by pricing.
        base_ask (Union[Unset, str]): The base ask price as calculated by pricing.
        bids (Union[Unset, List['PriceBucket']]): The list of prices and liquidity available on the Instrument's bid
            side. It is possible for this list to be empty if there is no bid liquidity currently available for the
            Instrument in the Account.
        asks (Union[Unset, List['PriceBucket']]): The list of prices and liquidity available on the Instrument's ask
            side. It is possible for this list to be empty if there is no ask liquidity currently available for the
            Instrument in the Account.
        closeout_bid (Union[Unset, str]): The closeout bid price. This price is used when a bid is required to closeout
            a Position (margin closeout or manual) yet there is no bid liquidity. The closeout bid is never used to open a
            new position.
        closeout_ask (Union[Unset, str]): The closeout ask price. This price is used when an ask is required to closeout
            a Position (margin closeout or manual) yet there is no ask liquidity. The closeout ask is never used to open a
            new position."""

    instrument: Union[Unset, str] = UNSET
    tradeable: Union[Unset, bool] = UNSET
    timestamp: Union[Unset, str] = UNSET
    base_bid: Union[Unset, str] = UNSET
    base_ask: Union[Unset, str] = UNSET
    bids: Union[Unset, List["PriceBucket"]] = UNSET
    asks: Union[Unset, List["PriceBucket"]] = UNSET
    closeout_bid: Union[Unset, str] = UNSET
    closeout_ask: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Price":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
