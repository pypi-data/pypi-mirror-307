from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_book import OrderBook
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetInstrumentsInstrumentOrderBookResponse200")


@dataclasses.dataclass
class GetInstrumentsInstrumentOrderBookResponse200:
    """Attributes:
    order_book (Union[Unset, OrderBook]): The representation of an instrument's order book at a point in time"""

    order_book: Optional["OrderBook"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any]
    ) -> "GetInstrumentsInstrumentOrderBookResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
