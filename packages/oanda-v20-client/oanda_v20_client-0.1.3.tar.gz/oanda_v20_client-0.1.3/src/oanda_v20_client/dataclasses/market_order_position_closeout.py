from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="MarketOrderPositionCloseout")


@dataclasses.dataclass
class MarketOrderPositionCloseout:
    """A MarketOrderPositionCloseout specifies the extensions to a Market Order when it has been created to closeout a
    specific Position.

        Attributes:
            instrument (Union[Unset, str]): The instrument of the Position being closed out.
            units (Union[Unset, str]): Indication of how much of the Position to close. Either "ALL", or a DecimalNumber
                reflection a partial close of the Trade. The DecimalNumber must always be positive, and represent a number that
                doesn't exceed the absolute size of the Position."""

    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketOrderPositionCloseout":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
