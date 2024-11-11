from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .position_book import PositionBook
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetInstrumentsInstrumentPositionBookResponse200")


@dataclasses.dataclass
class GetInstrumentsInstrumentPositionBookResponse200:
    """Attributes:
    position_book (Union[Unset, PositionBook]): The representation of an instrument's position book at a point in
        time"""

    position_book: Optional["PositionBook"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .position_book import PositionBook

        d = src_dict.copy()
        _position_book = d.pop("positionBook", None)
        position_book: Optional[PositionBook]
        if isinstance(_position_book, Unset):
            position_book = None
        else:
            position_book = PositionBook.from_dict(_position_book)
        get_instruments_instrument_position_book_response_200 = cls(
            position_book=position_book
        )
        get_instruments_instrument_position_book_response_200.additional_properties = d
        return get_instruments_instrument_position_book_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
