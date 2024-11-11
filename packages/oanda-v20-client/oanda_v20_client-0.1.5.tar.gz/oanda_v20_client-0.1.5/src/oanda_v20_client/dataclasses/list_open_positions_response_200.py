from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .position import Position
from typing import List, TypeVar, Union

T = TypeVar("T", bound="ListOpenPositionsResponse200")


@dataclasses.dataclass
class ListOpenPositionsResponse200:
    """Attributes:
    positions (Union[Unset, List['Position']]): The list of open Positions in the Account.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    positions: Union[Unset, List["Position"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListOpenPositionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
