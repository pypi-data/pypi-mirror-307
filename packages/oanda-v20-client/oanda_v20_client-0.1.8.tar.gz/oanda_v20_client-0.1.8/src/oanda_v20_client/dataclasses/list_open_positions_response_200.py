from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .position import Position
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="ListOpenPositionsResponse200")


@dataclasses.dataclass
class ListOpenPositionsResponse200:
    """Attributes:
    positions (Union[Unset, List['Position']]): The list of open Positions in the Account.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    positions: Optional[List["Position"]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .position import Position

        d = src_dict.copy()
        positions = []
        _positions = d.pop("positions", None)
        for positions_item_data in _positions or []:
            positions_item = Position.from_dict(positions_item_data)
            positions.append(positions_item)
        last_transaction_id = d.pop("lastTransactionID", None)
        list_open_positions_response_200 = cls(
            positions=positions, last_transaction_id=last_transaction_id
        )
        list_open_positions_response_200.additional_properties = d
        return list_open_positions_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
