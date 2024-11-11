from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.account_guaranteed_stop_loss_order_mode import (
    AccountGuaranteedStopLossOrderMode,
)
from ..models.account_guaranteed_stop_loss_order_mode import (
    check_account_guaranteed_stop_loss_order_mode,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.order import Order
    from ..models.position import Position
    from ..models.trade_summary import TradeSummary


T = TypeVar("T", bound="Account")


@_attrs_define
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
            orders (Union[Unset, List['Order']]): The details of the Orders currently pending in the Account.
    """

    id: Union[Unset, str] = UNSET
    alias: Union[Unset, str] = UNSET
    currency: Union[Unset, str] = UNSET
    balance: Union[Unset, str] = UNSET
    created_by_user_id: Union[Unset, int] = UNSET
    created_time: Union[Unset, str] = UNSET
    guaranteed_stop_loss_order_mode: Union[
        Unset, AccountGuaranteedStopLossOrderMode
    ] = UNSET
    pl: Union[Unset, str] = UNSET
    resettable_pl: Union[Unset, str] = UNSET
    resettable_pl_time: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    commission: Union[Unset, str] = UNSET
    guaranteed_execution_fees: Union[Unset, str] = UNSET
    margin_rate: Union[Unset, str] = UNSET
    margin_call_enter_time: Union[Unset, str] = UNSET
    margin_call_extension_count: Union[Unset, int] = UNSET
    last_margin_call_extension_time: Union[Unset, str] = UNSET
    open_trade_count: Union[Unset, int] = UNSET
    open_position_count: Union[Unset, int] = UNSET
    pending_order_count: Union[Unset, int] = UNSET
    hedging_enabled: Union[Unset, bool] = UNSET
    last_order_fill_timestamp: Union[Unset, str] = UNSET
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
    last_transaction_id: Union[Unset, str] = UNSET
    trades: Union[Unset, List["TradeSummary"]] = UNSET
    positions: Union[Unset, List["Position"]] = UNSET
    orders: Union[Unset, List["Order"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        alias = self.alias

        currency = self.currency

        balance = self.balance

        created_by_user_id = self.created_by_user_id

        created_time = self.created_time

        guaranteed_stop_loss_order_mode: Union[Unset, str] = UNSET
        if not isinstance(self.guaranteed_stop_loss_order_mode, Unset):
            guaranteed_stop_loss_order_mode = self.guaranteed_stop_loss_order_mode

        pl = self.pl

        resettable_pl = self.resettable_pl

        resettable_pl_time = self.resettable_pl_time

        financing = self.financing

        commission = self.commission

        guaranteed_execution_fees = self.guaranteed_execution_fees

        margin_rate = self.margin_rate

        margin_call_enter_time = self.margin_call_enter_time

        margin_call_extension_count = self.margin_call_extension_count

        last_margin_call_extension_time = self.last_margin_call_extension_time

        open_trade_count = self.open_trade_count

        open_position_count = self.open_position_count

        pending_order_count = self.pending_order_count

        hedging_enabled = self.hedging_enabled

        last_order_fill_timestamp = self.last_order_fill_timestamp

        unrealized_pl = self.unrealized_pl

        nav = self.nav

        margin_used = self.margin_used

        margin_available = self.margin_available

        position_value = self.position_value

        margin_closeout_unrealized_pl = self.margin_closeout_unrealized_pl

        margin_closeout_nav = self.margin_closeout_nav

        margin_closeout_margin_used = self.margin_closeout_margin_used

        margin_closeout_percent = self.margin_closeout_percent

        margin_closeout_position_value = self.margin_closeout_position_value

        withdrawal_limit = self.withdrawal_limit

        margin_call_margin_used = self.margin_call_margin_used

        margin_call_percent = self.margin_call_percent

        last_transaction_id = self.last_transaction_id

        trades: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trades, Unset):
            trades = []
            for trades_item_data in self.trades:
                trades_item = trades_item_data.to_dict()
                trades.append(trades_item)

        positions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.positions, Unset):
            positions = []
            for positions_item_data in self.positions:
                positions_item = positions_item_data.to_dict()
                positions.append(positions_item)

        orders: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders, Unset):
            orders = []
            for orders_item_data in self.orders:
                orders_item = orders_item_data.to_dict()
                orders.append(orders_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if alias is not UNSET:
            field_dict["alias"] = alias
        if currency is not UNSET:
            field_dict["currency"] = currency
        if balance is not UNSET:
            field_dict["balance"] = balance
        if created_by_user_id is not UNSET:
            field_dict["createdByUserID"] = created_by_user_id
        if created_time is not UNSET:
            field_dict["createdTime"] = created_time
        if guaranteed_stop_loss_order_mode is not UNSET:
            field_dict["guaranteedStopLossOrderMode"] = guaranteed_stop_loss_order_mode
        if pl is not UNSET:
            field_dict["pl"] = pl
        if resettable_pl is not UNSET:
            field_dict["resettablePL"] = resettable_pl
        if resettable_pl_time is not UNSET:
            field_dict["resettablePLTime"] = resettable_pl_time
        if financing is not UNSET:
            field_dict["financing"] = financing
        if commission is not UNSET:
            field_dict["commission"] = commission
        if guaranteed_execution_fees is not UNSET:
            field_dict["guaranteedExecutionFees"] = guaranteed_execution_fees
        if margin_rate is not UNSET:
            field_dict["marginRate"] = margin_rate
        if margin_call_enter_time is not UNSET:
            field_dict["marginCallEnterTime"] = margin_call_enter_time
        if margin_call_extension_count is not UNSET:
            field_dict["marginCallExtensionCount"] = margin_call_extension_count
        if last_margin_call_extension_time is not UNSET:
            field_dict["lastMarginCallExtensionTime"] = last_margin_call_extension_time
        if open_trade_count is not UNSET:
            field_dict["openTradeCount"] = open_trade_count
        if open_position_count is not UNSET:
            field_dict["openPositionCount"] = open_position_count
        if pending_order_count is not UNSET:
            field_dict["pendingOrderCount"] = pending_order_count
        if hedging_enabled is not UNSET:
            field_dict["hedgingEnabled"] = hedging_enabled
        if last_order_fill_timestamp is not UNSET:
            field_dict["lastOrderFillTimestamp"] = last_order_fill_timestamp
        if unrealized_pl is not UNSET:
            field_dict["unrealizedPL"] = unrealized_pl
        if nav is not UNSET:
            field_dict["NAV"] = nav
        if margin_used is not UNSET:
            field_dict["marginUsed"] = margin_used
        if margin_available is not UNSET:
            field_dict["marginAvailable"] = margin_available
        if position_value is not UNSET:
            field_dict["positionValue"] = position_value
        if margin_closeout_unrealized_pl is not UNSET:
            field_dict["marginCloseoutUnrealizedPL"] = margin_closeout_unrealized_pl
        if margin_closeout_nav is not UNSET:
            field_dict["marginCloseoutNAV"] = margin_closeout_nav
        if margin_closeout_margin_used is not UNSET:
            field_dict["marginCloseoutMarginUsed"] = margin_closeout_margin_used
        if margin_closeout_percent is not UNSET:
            field_dict["marginCloseoutPercent"] = margin_closeout_percent
        if margin_closeout_position_value is not UNSET:
            field_dict["marginCloseoutPositionValue"] = margin_closeout_position_value
        if withdrawal_limit is not UNSET:
            field_dict["withdrawalLimit"] = withdrawal_limit
        if margin_call_margin_used is not UNSET:
            field_dict["marginCallMarginUsed"] = margin_call_margin_used
        if margin_call_percent is not UNSET:
            field_dict["marginCallPercent"] = margin_call_percent
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id
        if trades is not UNSET:
            field_dict["trades"] = trades
        if positions is not UNSET:
            field_dict["positions"] = positions
        if orders is not UNSET:
            field_dict["orders"] = orders

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.order import Order
        from ..models.position import Position
        from ..models.trade_summary import TradeSummary

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        alias = d.pop("alias", UNSET)

        currency = d.pop("currency", UNSET)

        balance = d.pop("balance", UNSET)

        created_by_user_id = d.pop("createdByUserID", UNSET)

        created_time = d.pop("createdTime", UNSET)

        _guaranteed_stop_loss_order_mode = d.pop("guaranteedStopLossOrderMode", UNSET)
        guaranteed_stop_loss_order_mode: Union[
            Unset, AccountGuaranteedStopLossOrderMode
        ]
        if isinstance(_guaranteed_stop_loss_order_mode, Unset):
            guaranteed_stop_loss_order_mode = UNSET
        else:
            guaranteed_stop_loss_order_mode = (
                check_account_guaranteed_stop_loss_order_mode(
                    _guaranteed_stop_loss_order_mode
                )
            )

        pl = d.pop("pl", UNSET)

        resettable_pl = d.pop("resettablePL", UNSET)

        resettable_pl_time = d.pop("resettablePLTime", UNSET)

        financing = d.pop("financing", UNSET)

        commission = d.pop("commission", UNSET)

        guaranteed_execution_fees = d.pop("guaranteedExecutionFees", UNSET)

        margin_rate = d.pop("marginRate", UNSET)

        margin_call_enter_time = d.pop("marginCallEnterTime", UNSET)

        margin_call_extension_count = d.pop("marginCallExtensionCount", UNSET)

        last_margin_call_extension_time = d.pop("lastMarginCallExtensionTime", UNSET)

        open_trade_count = d.pop("openTradeCount", UNSET)

        open_position_count = d.pop("openPositionCount", UNSET)

        pending_order_count = d.pop("pendingOrderCount", UNSET)

        hedging_enabled = d.pop("hedgingEnabled", UNSET)

        last_order_fill_timestamp = d.pop("lastOrderFillTimestamp", UNSET)

        unrealized_pl = d.pop("unrealizedPL", UNSET)

        nav = d.pop("NAV", UNSET)

        margin_used = d.pop("marginUsed", UNSET)

        margin_available = d.pop("marginAvailable", UNSET)

        position_value = d.pop("positionValue", UNSET)

        margin_closeout_unrealized_pl = d.pop("marginCloseoutUnrealizedPL", UNSET)

        margin_closeout_nav = d.pop("marginCloseoutNAV", UNSET)

        margin_closeout_margin_used = d.pop("marginCloseoutMarginUsed", UNSET)

        margin_closeout_percent = d.pop("marginCloseoutPercent", UNSET)

        margin_closeout_position_value = d.pop("marginCloseoutPositionValue", UNSET)

        withdrawal_limit = d.pop("withdrawalLimit", UNSET)

        margin_call_margin_used = d.pop("marginCallMarginUsed", UNSET)

        margin_call_percent = d.pop("marginCallPercent", UNSET)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        trades = []
        _trades = d.pop("trades", UNSET)
        for trades_item_data in _trades or []:
            trades_item = TradeSummary.from_dict(trades_item_data)

            trades.append(trades_item)

        positions = []
        _positions = d.pop("positions", UNSET)
        for positions_item_data in _positions or []:
            positions_item = Position.from_dict(positions_item_data)

            positions.append(positions_item)

        orders = []
        _orders = d.pop("orders", UNSET)
        for orders_item_data in _orders or []:
            orders_item = Order.from_dict(orders_item_data)

            orders.append(orders_item)

        account = cls(
            id=id,
            alias=alias,
            currency=currency,
            balance=balance,
            created_by_user_id=created_by_user_id,
            created_time=created_time,
            guaranteed_stop_loss_order_mode=guaranteed_stop_loss_order_mode,
            pl=pl,
            resettable_pl=resettable_pl,
            resettable_pl_time=resettable_pl_time,
            financing=financing,
            commission=commission,
            guaranteed_execution_fees=guaranteed_execution_fees,
            margin_rate=margin_rate,
            margin_call_enter_time=margin_call_enter_time,
            margin_call_extension_count=margin_call_extension_count,
            last_margin_call_extension_time=last_margin_call_extension_time,
            open_trade_count=open_trade_count,
            open_position_count=open_position_count,
            pending_order_count=pending_order_count,
            hedging_enabled=hedging_enabled,
            last_order_fill_timestamp=last_order_fill_timestamp,
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
            last_transaction_id=last_transaction_id,
            trades=trades,
            positions=positions,
            orders=orders,
        )

        account.additional_properties = d
        return account

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
