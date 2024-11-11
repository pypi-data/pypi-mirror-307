from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .calculated_position_state import CalculatedPositionState
from .calculated_trade_state import CalculatedTradeState
from .dynamic_order_state import DynamicOrderState
from typing import List, TypeVar, Union

T = TypeVar("T", bound="AccountChangesState")


@dataclasses.dataclass
class AccountChangesState:
    """An AccountState Object is used to represent an Account's current price-dependent state. Price-dependent Account
    state is dependent on OANDA's current Prices, and includes things like unrealized PL, NAV and Trailing Stop Loss
    Order state.

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
                the Account is in a margin call situation.
            orders (Union[Unset, List['DynamicOrderState']]): The price-dependent state of each pending Order in the
                Account.
            trades (Union[Unset, List['CalculatedTradeState']]): The price-dependent state for each open Trade in the
                Account.
            positions (Union[Unset, List['CalculatedPositionState']]): The price-dependent state for each open Position in
                the Account."""

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
    orders: Union[Unset, List["DynamicOrderState"]] = UNSET
    trades: Union[Unset, List["CalculatedTradeState"]] = UNSET
    positions: Union[Unset, List["CalculatedPositionState"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountChangesState":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
