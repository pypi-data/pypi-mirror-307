from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        unrealized_pl = d.pop("unrealizedPL", None)
        margin_used = d.pop("marginUsed", None)
        calculated_trade_state = cls(
            id=id, unrealized_pl=unrealized_pl, margin_used=margin_used
        )
        calculated_trade_state.additional_properties = d
        return calculated_trade_state

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
