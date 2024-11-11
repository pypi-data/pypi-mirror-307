from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="PositionBookBucket")


@dataclasses.dataclass
class PositionBookBucket:
    """The position book data for a partition of the instrument's prices.

    Attributes:
        price (Union[Unset, str]): The lowest price (inclusive) covered by the bucket. The bucket covers the price range
            from the price to price + the position book's bucketWidth.
        long_count_percent (Union[Unset, str]): The percentage of the total number of positions represented by the long
            positions found in this bucket.
        short_count_percent (Union[Unset, str]): The percentage of the total number of positions represented by the
            short positions found in this bucket."""

    price: Optional[str]
    long_count_percent: Optional[str]
    short_count_percent: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        price = d.pop("price", None)
        long_count_percent = d.pop("longCountPercent", None)
        short_count_percent = d.pop("shortCountPercent", None)
        position_book_bucket = cls(
            price=price,
            long_count_percent=long_count_percent,
            short_count_percent=short_count_percent,
        )
        position_book_bucket.additional_properties = d
        return position_book_bucket

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
