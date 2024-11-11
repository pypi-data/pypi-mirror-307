from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="OpenTradeFinancing")


@dataclasses.dataclass
class OpenTradeFinancing:
    """OpenTradeFinancing is used to pay/collect daily financing charge for an open Trade within an Account

    Attributes:
        trade_id (Union[Unset, str]): The ID of the Trade that financing is being paid/collected for.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Trade."""

    trade_id: Optional[str]
    financing: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", None)
        financing = d.pop("financing", None)
        open_trade_financing = cls(trade_id=trade_id, financing=financing)
        open_trade_financing.additional_properties = d
        return open_trade_financing

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
