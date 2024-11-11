from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .calculated_position_state import CalculatedPositionState
from .calculated_trade_state import CalculatedTradeState
from .dynamic_order_state import DynamicOrderState
from typing import List, Optional, Type, TypeVar

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

    unrealized_pl: Optional[str]
    nav: Optional[str]
    margin_used: Optional[str]
    margin_available: Optional[str]
    position_value: Optional[str]
    margin_closeout_unrealized_pl: Optional[str]
    margin_closeout_nav: Optional[str]
    margin_closeout_margin_used: Optional[str]
    margin_closeout_percent: Optional[str]
    margin_closeout_position_value: Optional[str]
    withdrawal_limit: Optional[str]
    margin_call_margin_used: Optional[str]
    margin_call_percent: Optional[str]
    orders: Optional[List["DynamicOrderState"]]
    trades: Optional[List["CalculatedTradeState"]]
    positions: Optional[List["CalculatedPositionState"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .dynamic_order_state import DynamicOrderState
        from .calculated_trade_state import CalculatedTradeState
        from .calculated_position_state import CalculatedPositionState

        d = src_dict.copy()
        unrealized_pl = d.pop("unrealizedPL", None)
        nav = d.pop("NAV", None)
        margin_used = d.pop("marginUsed", None)
        margin_available = d.pop("marginAvailable", None)
        position_value = d.pop("positionValue", None)
        margin_closeout_unrealized_pl = d.pop("marginCloseoutUnrealizedPL", None)
        margin_closeout_nav = d.pop("marginCloseoutNAV", None)
        margin_closeout_margin_used = d.pop("marginCloseoutMarginUsed", None)
        margin_closeout_percent = d.pop("marginCloseoutPercent", None)
        margin_closeout_position_value = d.pop("marginCloseoutPositionValue", None)
        withdrawal_limit = d.pop("withdrawalLimit", None)
        margin_call_margin_used = d.pop("marginCallMarginUsed", None)
        margin_call_percent = d.pop("marginCallPercent", None)
        orders = []
        _orders = d.pop("orders", None)
        for orders_item_data in _orders or []:
            orders_item = DynamicOrderState.from_dict(orders_item_data)
            orders.append(orders_item)
        trades = []
        _trades = d.pop("trades", None)
        for trades_item_data in _trades or []:
            trades_item = CalculatedTradeState.from_dict(trades_item_data)
            trades.append(trades_item)
        positions = []
        _positions = d.pop("positions", None)
        for positions_item_data in _positions or []:
            positions_item = CalculatedPositionState.from_dict(positions_item_data)
            positions.append(positions_item)
        account_changes_state = cls(
            unrealized_pl=unrealized_pl,
            nav=nav,
            margin_used=margin_used,
            margin_available=margin_available,
            position_value=position_value,
            margin_closeout_unrealized_pl=margin_closeout_unrealized_pl,
            margin_closeout_nav=margin_closeout_nav,
            margin_closeout_margin_used=margin_closeout_margin_used,
            margin_closeout_percent=margin_closeout_percent,
            margin_closeout_position_value=margin_closeout_position_value,
            withdrawal_limit=withdrawal_limit,
            margin_call_margin_used=margin_call_margin_used,
            margin_call_percent=margin_call_percent,
            orders=orders,
            trades=trades,
            positions=positions,
        )
        account_changes_state.additional_properties = d
        return account_changes_state

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
