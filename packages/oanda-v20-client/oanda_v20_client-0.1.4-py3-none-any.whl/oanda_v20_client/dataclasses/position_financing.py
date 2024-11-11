from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .open_trade_financing import OpenTradeFinancing
from typing import List, TypeVar, Union

T = TypeVar("T", bound="PositionFinancing")


@dataclasses.dataclass
class PositionFinancing:
    """OpenTradeFinancing is used to pay/collect daily financing charge for a Position within an Account

    Attributes:
        instrument (Union[Unset, str]): The instrument of the Position that financing is being paid/collected for.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Position.
        open_trade_financings (Union[Unset, List['OpenTradeFinancing']]): The financing paid/collecte for each open
            Trade within the Position."""

    instrument: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    open_trade_financings: Union[Unset, List["OpenTradeFinancing"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PositionFinancing":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
