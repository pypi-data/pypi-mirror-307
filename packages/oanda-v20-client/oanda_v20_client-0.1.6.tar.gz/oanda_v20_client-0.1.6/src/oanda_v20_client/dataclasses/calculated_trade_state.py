from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="CalculatedTradeState")


@dataclasses.dataclass
class CalculatedTradeState:
    """The dynamic (calculated) state of an open Trade

    Attributes:
        id (Union[Unset, str]): The Trade's ID.
        unrealized_pl (Union[Unset, str]): The Trade's unrealized profit/loss.
        margin_used (Union[Unset, str]): Margin currently used by the Trade."""

    id: Optional[str]
    unrealized_pl: Optional[str]
    margin_used: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatedTradeState":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
