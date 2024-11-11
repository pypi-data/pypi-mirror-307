from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CalculatedPositionState")


@dataclasses.dataclass
class CalculatedPositionState:
    """The dynamic (calculated) state of a Position

    Attributes:
        instrument (Union[Unset, str]): The Position's Instrument.
        net_unrealized_pl (Union[Unset, str]): The Position's net unrealized profit/loss
        long_unrealized_pl (Union[Unset, str]): The unrealized profit/loss of the Position's long open Trades
        short_unrealized_pl (Union[Unset, str]): The unrealized profit/loss of the Position's short open Trades
        margin_used (Union[Unset, str]): Margin currently used by the Position."""

    instrument: Optional[str]
    net_unrealized_pl: Optional[str]
    long_unrealized_pl: Optional[str]
    short_unrealized_pl: Optional[str]
    margin_used: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        net_unrealized_pl = d.pop("netUnrealizedPL", None)
        long_unrealized_pl = d.pop("longUnrealizedPL", None)
        short_unrealized_pl = d.pop("shortUnrealizedPL", None)
        margin_used = d.pop("marginUsed", None)
        calculated_position_state = cls(
            instrument=instrument,
            net_unrealized_pl=net_unrealized_pl,
            long_unrealized_pl=long_unrealized_pl,
            short_unrealized_pl=short_unrealized_pl,
            margin_used=margin_used,
        )
        calculated_position_state.additional_properties = d
        return calculated_position_state

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
