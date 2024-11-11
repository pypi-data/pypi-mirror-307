from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="OrderBookBucket")


@dataclasses.dataclass
class OrderBookBucket:
    """The order book data for a partition of the instrument's prices.

    Attributes:
        price (Union[Unset, str]): The lowest price (inclusive) covered by the bucket. The bucket covers the price range
            from the price to price + the order book's bucketWidth.
        long_count_percent (Union[Unset, str]): The percentage of the total number of orders represented by the long
            orders found in this bucket.
        short_count_percent (Union[Unset, str]): The percentage of the total number of orders represented by the short
            orders found in this bucket."""

    price: Optional[str]
    long_count_percent: Optional[str]
    short_count_percent: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        price = d.pop("price", None)
        long_count_percent = d.pop("longCountPercent", None)
        short_count_percent = d.pop("shortCountPercent", None)
        order_book_bucket = cls(
            price=price,
            long_count_percent=long_count_percent,
            short_count_percent=short_count_percent,
        )
        order_book_bucket.additional_properties = d
        return order_book_bucket

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
