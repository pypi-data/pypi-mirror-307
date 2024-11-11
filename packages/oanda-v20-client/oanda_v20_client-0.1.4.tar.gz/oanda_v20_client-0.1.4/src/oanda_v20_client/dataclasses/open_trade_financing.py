from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

T = TypeVar("T", bound="OpenTradeFinancing")


@dataclasses.dataclass
class OpenTradeFinancing:
    """OpenTradeFinancing is used to pay/collect daily financing charge for an open Trade within an Account

    Attributes:
        trade_id (Union[Unset, str]): The ID of the Trade that financing is being paid/collected for.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Trade."""

    trade_id: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OpenTradeFinancing":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
