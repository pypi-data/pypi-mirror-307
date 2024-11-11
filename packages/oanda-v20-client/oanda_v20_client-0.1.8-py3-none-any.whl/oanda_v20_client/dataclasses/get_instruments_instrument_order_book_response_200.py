from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_book import OrderBook
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetInstrumentsInstrumentOrderBookResponse200")


@dataclasses.dataclass
class GetInstrumentsInstrumentOrderBookResponse200:
    """Attributes:
    order_book (Union[Unset, OrderBook]): The representation of an instrument's order book at a point in time"""

    order_book: Optional["OrderBook"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_book import OrderBook

        d = src_dict.copy()
        _order_book = d.pop("orderBook", None)
        order_book: Optional[OrderBook]
        if isinstance(_order_book, Unset):
            order_book = None
        else:
            order_book = OrderBook.from_dict(_order_book)
        get_instruments_instrument_order_book_response_200 = cls(order_book=order_book)
        get_instruments_instrument_order_book_response_200.additional_properties = d
        return get_instruments_instrument_order_book_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
