from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

T = TypeVar("T", bound="CalculatedTradeState")


@dataclasses.dataclass
class CalculatedTradeState:
    """The dynamic (calculated) state of an open Trade

    Attributes:
        id (Union[Unset, str]): The Trade's ID.
        unrealized_pl (Union[Unset, str]): The Trade's unrealized profit/loss.
        margin_used (Union[Unset, str]): Margin currently used by the Trade."""

    id: Union[Unset, str] = UNSET
    unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatedTradeState":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
