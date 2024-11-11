from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .position_book import PositionBook
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetInstrumentsInstrumentPositionBookResponse200")


@dataclasses.dataclass
class GetInstrumentsInstrumentPositionBookResponse200:
    """Attributes:
    position_book (Union[Unset, PositionBook]): The representation of an instrument's position book at a point in
        time"""

    position_book: Optional["PositionBook"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any]
    ) -> "GetInstrumentsInstrumentPositionBookResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
