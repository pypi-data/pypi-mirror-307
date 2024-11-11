from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .position_side import PositionSide
from typing import Optional, TypeVar

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Position":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
