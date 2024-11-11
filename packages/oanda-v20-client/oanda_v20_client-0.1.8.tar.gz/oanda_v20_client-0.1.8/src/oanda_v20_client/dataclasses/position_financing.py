from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .open_trade_financing import OpenTradeFinancing
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="PositionFinancing")


@dataclasses.dataclass
class PositionFinancing:
    """OpenTradeFinancing is used to pay/collect daily financing charge for a Position within an Account

    Attributes:
        instrument (Union[Unset, str]): The instrument of the Position that financing is being paid/collected for.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Position.
        open_trade_financings (Union[Unset, List['OpenTradeFinancing']]): The financing paid/collecte for each open
            Trade within the Position."""

    instrument: Optional[str]
    financing: Optional[str]
    open_trade_financings: Optional[List["OpenTradeFinancing"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .open_trade_financing import OpenTradeFinancing

        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        financing = d.pop("financing", None)
        open_trade_financings = []
        _open_trade_financings = d.pop("openTradeFinancings", None)
        for open_trade_financings_item_data in _open_trade_financings or []:
            open_trade_financings_item = OpenTradeFinancing.from_dict(
                open_trade_financings_item_data
            )
            open_trade_financings.append(open_trade_financings_item)
        position_financing = cls(
            instrument=instrument,
            financing=financing,
            open_trade_financings=open_trade_financings,
        )
        position_financing.additional_properties = d
        return position_financing

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
