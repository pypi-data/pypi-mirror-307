from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .position import Position
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetPositionResponse200")


@dataclasses.dataclass
class GetPositionResponse200:
    """Attributes:
    position (Union[Unset, Position]): The specification of a Position within an Account.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    position: Optional["Position"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .position import Position

        d = src_dict.copy()
        _position = d.pop("position", None)
        position: Optional[Position]
        if isinstance(_position, Unset):
            position = None
        else:
            position = Position.from_dict(_position)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_position_response_200 = cls(
            position=position, last_transaction_id=last_transaction_id
        )
        get_position_response_200.additional_properties = d
        return get_position_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
