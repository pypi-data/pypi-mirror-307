from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_book_bucket import OrderBookBucket
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="OrderBook")


@dataclasses.dataclass
class OrderBook:
    """The representation of an instrument's order book at a point in time

    Attributes:
        instrument (Union[Unset, str]): The order book's instrument
        time (Union[Unset, str]): The time when the order book snapshot was created.
        price (Union[Unset, str]): The price (midpoint) for the order book's instrument at the time of the order book
            snapshot
        bucket_width (Union[Unset, str]): The price width for each bucket. Each bucket covers the price range from the
            bucket's price to the bucket's price + bucketWidth.
        buckets (Union[Unset, List['OrderBookBucket']]): The partitioned order book, divided into buckets using a
            default bucket width. These buckets are only provided for price ranges which actually contain order or position
            data."""

    instrument: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    bucket_width: Union[Unset, str] = UNSET
    buckets: Union[Unset, List["OrderBookBucket"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderBook":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
