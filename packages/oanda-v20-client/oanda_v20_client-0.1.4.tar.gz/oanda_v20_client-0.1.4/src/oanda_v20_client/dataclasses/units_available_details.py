from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

T = TypeVar("T", bound="UnitsAvailableDetails")


@dataclasses.dataclass
class UnitsAvailableDetails:
    """Representation of many units of an Instrument are available to be traded for both long and short Orders.

    Attributes:
        long (Union[Unset, str]): The units available for long Orders.
        short (Union[Unset, str]): The units available for short Orders."""

    long: Union[Unset, str] = UNSET
    short: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnitsAvailableDetails":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
