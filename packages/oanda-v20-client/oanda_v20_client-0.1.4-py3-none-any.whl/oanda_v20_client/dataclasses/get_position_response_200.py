from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .position import Position
from typing import TypeVar, Union

T = TypeVar("T", bound="GetPositionResponse200")


@dataclasses.dataclass
class GetPositionResponse200:
    """Attributes:
    position (Union[Unset, Position]): The specification of a Position within an Account.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    position: Union[Unset, "Position"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetPositionResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
