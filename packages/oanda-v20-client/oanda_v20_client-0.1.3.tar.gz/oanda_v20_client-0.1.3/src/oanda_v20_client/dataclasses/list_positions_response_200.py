from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .position import Position
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="ListPositionsResponse200")


@dataclasses.dataclass
class ListPositionsResponse200:
    """Attributes:
    positions (Union[Unset, List['Position']]): The list of Account Positions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    positions: Union[Unset, List["Position"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListPositionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
