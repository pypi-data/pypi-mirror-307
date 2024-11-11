from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .position_side import PositionSide
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    instrument: Union[Unset, str] = UNSET
    pl: Union[Unset, str] = UNSET
    unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    resettable_pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    commission: Union[Unset, str] = UNSET
    guaranteed_execution_fees: Union[Unset, str] = UNSET
    long: Union[Unset, "PositionSide"] = UNSET
    short: Union[Unset, "PositionSide"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Position":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
