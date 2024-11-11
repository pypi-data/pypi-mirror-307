from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .account_guaranteed_stop_loss_order_mode import AccountGuaranteedStopLossOrderMode
from .order import Order
from .position import Position
from .trade_summary import TradeSummary
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="Account")


@dataclasses.dataclass
class Account:
    """The full details of a client's Account. This includes full open Trade, open Position and pending Order
    representation.

        Attributes:
            id (Union[Unset, str]): The Account's identifier
            alias (Union[Unset, str]): Client-assigned alias for the Account. Only provided if the Account has an alias set
            currency (Union[Unset, str]): The home currency of the Account
            balance (Union[Unset, str]): The current balance of the Account.
            created_by_user_id (Union[Unset, int]): ID of the user that created the Account.
            created_time (Union[Unset, str]): The date/time when the Account was created.
            guaranteed_stop_loss_order_mode (Union[Unset, AccountGuaranteedStopLossOrderMode]): The current guaranteed Stop
                Loss Order mode of the Account.
            pl (Union[Unset, str]): The total profit/loss realized over the lifetime of the Account.
            resettable_pl (Union[Unset, str]): The total realized profit/loss for the Account since it was last reset by the
                client.
            resettable_pl_time (Union[Unset, str]): The date/time that the Account's resettablePL was last reset.
            financing (Union[Unset, str]): The total amount of financing paid/collected over the lifetime of the Account.
            commission (Union[Unset, str]): The total amount of commission paid over the lifetime of the Account.
            guaranteed_execution_fees (Union[Unset, str]): The total amount of fees charged over the lifetime of the Account
                for the execution of guaranteed Stop Loss Orders.
            margin_rate (Union[Unset, str]): Client-provided margin rate override for the Account. The effective margin rate
                of the Account is the lesser of this value and the OANDA margin rate for the Account's division. This value is
                only provided if a margin rate override exists for the Account.
            margin_call_enter_time (Union[Unset, str]): The date/time when the Account entered a margin call state. Only
                provided if the Account is in a margin call.
            margin_call_extension_count (Union[Unset, int]): The number of times that the Account's current margin call was
                extended.
            last_margin_call_extension_time (Union[Unset, str]): The date/time of the Account's last margin call extension.
            open_trade_count (Union[Unset, int]): The number of Trades currently open in the Account.
            open_position_count (Union[Unset, int]): The number of Positions currently open in the Account.
            pending_order_count (Union[Unset, int]): The number of Orders currently pending in the Account.
            hedging_enabled (Union[Unset, bool]): Flag indicating that the Account has hedging enabled.
            last_order_fill_timestamp (Union[Unset, str]): The date/time of the last order that was filled for this account.
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
            last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.
            trades (Union[Unset, List['TradeSummary']]): The details of the Trades currently open in the Account.
            positions (Union[Unset, List['Position']]): The details all Account Positions.
            orders (Union[Unset, List['Order']]): The details of the Orders currently pending in the Account."""

    id: Optional[str]
    alias: Optional[str]
    currency: Optional[str]
    balance: Optional[str]
    created_by_user_id: Optional[int]
    created_time: Optional[str]
    guaranteed_stop_loss_order_mode: Optional[AccountGuaranteedStopLossOrderMode]
    pl: Optional[str]
    resettable_pl: Optional[str]
    resettable_pl_time: Optional[str]
    financing: Optional[str]
    commission: Optional[str]
    guaranteed_execution_fees: Optional[str]
    margin_rate: Optional[str]
    margin_call_enter_time: Optional[str]
    margin_call_extension_count: Optional[int]
    last_margin_call_extension_time: Optional[str]
    open_trade_count: Optional[int]
    open_position_count: Optional[int]
    pending_order_count: Optional[int]
    hedging_enabled: Optional[bool]
    last_order_fill_timestamp: Optional[str]
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
    last_transaction_id: Optional[str]
    trades: Optional[List["TradeSummary"]]
    positions: Optional[List["Position"]]
    orders: Optional[List["Order"]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
