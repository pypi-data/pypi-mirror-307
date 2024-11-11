from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .price_bucket import PriceBucket
from typing import List, Optional, Type, TypeVar

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

    instrument: Optional[str]
    tradeable: Optional[bool]
    timestamp: Optional[str]
    base_bid: Optional[str]
    base_ask: Optional[str]
    bids: Optional[List["PriceBucket"]]
    asks: Optional[List["PriceBucket"]]
    closeout_bid: Optional[str]
    closeout_ask: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .price_bucket import PriceBucket

        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        tradeable = d.pop("tradeable", None)
        timestamp = d.pop("timestamp", None)
        base_bid = d.pop("baseBid", None)
        base_ask = d.pop("baseAsk", None)
        bids = []
        _bids = d.pop("bids", None)
        for bids_item_data in _bids or []:
            bids_item = PriceBucket.from_dict(bids_item_data)
            bids.append(bids_item)
        asks = []
        _asks = d.pop("asks", None)
        for asks_item_data in _asks or []:
            asks_item = PriceBucket.from_dict(asks_item_data)
            asks.append(asks_item)
        closeout_bid = d.pop("closeoutBid", None)
        closeout_ask = d.pop("closeoutAsk", None)
        price = cls(
            instrument=instrument,
            tradeable=tradeable,
            timestamp=timestamp,
            base_bid=base_bid,
            base_ask=base_ask,
            bids=bids,
            asks=asks,
            closeout_bid=closeout_bid,
            closeout_ask=closeout_ask,
        )
        price.additional_properties = d
        return price

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
