from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .position_side import PositionSide
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="Position")


@dataclasses.dataclass
class Position:
    """The specification of a Position within an Account.

    Attributes:
        instrument (Union[Unset, str]): The Position's Instrument.
        pl (Union[Unset, str]): Profit/loss realized by the Position over the lifetime of the Account.
        unrealized_pl (Union[Unset, str]): The unrealized profit/loss of all open Trades that contribute to this
            Position.
        margin_used (Union[Unset, str]): Margin currently used by the Position.
        resettable_pl (Union[Unset, str]): Profit/loss realized by the Position since the Account's resettablePL was
            last reset by the client.
        financing (Union[Unset, str]): The total amount of financing paid/collected for this instrument over the
            lifetime of the Account.
        commission (Union[Unset, str]): The total amount of commission paid for this instrument over the lifetime of the
            Account.
        guaranteed_execution_fees (Union[Unset, str]): The total amount of fees charged over the lifetime of the Account
            for the execution of guaranteed Stop Loss Orders for this instrument.
        long (Union[Unset, PositionSide]): The representation of a Position for a single direction (long or short).
        short (Union[Unset, PositionSide]): The representation of a Position for a single direction (long or short)."""

    instrument: Optional[str]
    pl: Optional[str]
    unrealized_pl: Optional[str]
    margin_used: Optional[str]
    resettable_pl: Optional[str]
    financing: Optional[str]
    commission: Optional[str]
    guaranteed_execution_fees: Optional[str]
    long: Optional["PositionSide"]
    short: Optional["PositionSide"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .position_side import PositionSide

        d = src_dict.copy()
        instrument = d.pop("instrument", None)
        pl = d.pop("pl", None)
        unrealized_pl = d.pop("unrealizedPL", None)
        margin_used = d.pop("marginUsed", None)
        resettable_pl = d.pop("resettablePL", None)
        financing = d.pop("financing", None)
        commission = d.pop("commission", None)
        guaranteed_execution_fees = d.pop("guaranteedExecutionFees", None)
        _long = d.pop("long", None)
        long: Optional[PositionSide]
        if isinstance(_long, Unset):
            long = None
        else:
            long = PositionSide.from_dict(_long)
        _short = d.pop("short", None)
        short: Optional[PositionSide]
        if isinstance(_short, Unset):
            short = None
        else:
            short = PositionSide.from_dict(_short)
        position = cls(
            instrument=instrument,
            pl=pl,
            unrealized_pl=unrealized_pl,
            margin_used=margin_used,
            resettable_pl=resettable_pl,
            financing=financing,
            commission=commission,
            guaranteed_execution_fees=guaranteed_execution_fees,
            long=long,
            short=short,
        )
        position.additional_properties = d
        return position

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
