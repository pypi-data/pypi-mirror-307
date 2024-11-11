from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .position_book_bucket import PositionBookBucket
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="PositionBook")


@dataclasses.dataclass
class PositionBook:
    """The representation of an instrument's position book at a point in time

    Attributes:
        instrument (Union[Unset, str]): The position book's instrument
        time (Union[Unset, str]): The time when the position book snapshot was created
        price (Union[Unset, str]): The price (midpoint) for the position book's instrument at the time of the position
            book snapshot
        bucket_width (Union[Unset, str]): The price width for each bucket. Each bucket covers the price range from the
            bucket's price to the bucket's price + bucketWidth.
        buckets (Union[Unset, List['PositionBookBucket']]): The partitioned position book, divided into buckets using a
            default bucket width. These buckets are only provided for price ranges which actually contain order or position
            data."""

    instrument: Optional[str]
    time: Optional[str]
    price: Optional[str]
    bucket_width: Optional[str]
    buckets: Optional[List["PositionBookBucket"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .position_book_bucket import PositionBookBucket

        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        time = d.pop("time", None)
        price = d.pop("price", None)
        bucket_width = d.pop("bucketWidth", None)
        buckets = []
        _buckets = d.pop("buckets", None)
        for buckets_item_data in _buckets or []:
            buckets_item = PositionBookBucket.from_dict(buckets_item_data)
            buckets.append(buckets_item)
        position_book = cls(
            instrument=instrument,
            time=time,
            price=price,
            bucket_width=bucket_width,
            buckets=buckets,
        )
        position_book.additional_properties = d
        return position_book

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
