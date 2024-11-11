from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="CalculatedAccountState")


@dataclasses.dataclass
class CalculatedAccountState:
    """The dynamically calculated state of a client's Account.

    Attributes:
        unrealized_pl (Union[Unset, str]): The total unrealized profit/loss for all Trades currently open in the
            Account.
        nav (Union[Unset, str]): The net asset value of the Account. Equal to Account balance + unrealizedPL.
        margin_used (Union[Unset, str]): Margin currently used for the Account.
        margin_available (Union[Unset, str]): Margin available for Account currency.
        position_value (Union[Unset, str]): The value of the Account's open positions represented in the Account's home
            currency.
        margin_closeout_unrealized_pl (Union[Unset, str]): The Account's margin closeout unrealized PL.
        margin_closeout_nav (Union[Unset, str]): The Account's margin closeout NAV.
        margin_closeout_margin_used (Union[Unset, str]): The Account's margin closeout margin used.
        margin_closeout_percent (Union[Unset, str]): The Account's margin closeout percentage. When this value is 1.0 or
            above the Account is in a margin closeout situation.
        margin_closeout_position_value (Union[Unset, str]): The value of the Account's open positions as used for margin
            closeout calculations represented in the Account's home currency.
        withdrawal_limit (Union[Unset, str]): The current WithdrawalLimit for the account which will be zero or a
            positive value indicating how much can be withdrawn from the account.
        margin_call_margin_used (Union[Unset, str]): The Account's margin call margin used.
        margin_call_percent (Union[Unset, str]): The Account's margin call percentage. When this value is 1.0 or above
            the Account is in a margin call situation."""

    unrealized_pl: Union[Unset, str] = UNSET
    nav: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    margin_available: Union[Unset, str] = UNSET
    position_value: Union[Unset, str] = UNSET
    margin_closeout_unrealized_pl: Union[Unset, str] = UNSET
    margin_closeout_nav: Union[Unset, str] = UNSET
    margin_closeout_margin_used: Union[Unset, str] = UNSET
    margin_closeout_percent: Union[Unset, str] = UNSET
    margin_closeout_position_value: Union[Unset, str] = UNSET
    withdrawal_limit: Union[Unset, str] = UNSET
    margin_call_margin_used: Union[Unset, str] = UNSET
    margin_call_percent: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatedAccountState":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
