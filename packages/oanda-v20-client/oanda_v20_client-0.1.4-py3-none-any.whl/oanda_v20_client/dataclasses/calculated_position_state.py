from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

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

    instrument: Union[Unset, str] = UNSET
    net_unrealized_pl: Union[Unset, str] = UNSET
    long_unrealized_pl: Union[Unset, str] = UNSET
    short_unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatedPositionState":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
