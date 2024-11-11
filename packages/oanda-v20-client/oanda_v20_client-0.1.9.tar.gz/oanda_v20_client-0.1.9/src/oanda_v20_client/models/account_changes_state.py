from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.calculated_position_state import CalculatedPositionState
    from ..models.dynamic_order_state import DynamicOrderState
    from ..models.calculated_trade_state import CalculatedTradeState


T = TypeVar("T", bound="AccountChangesState")


@_attrs_define
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
                the Account.
    """

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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

        orders: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders, Unset):
            orders = []
            for orders_item_data in self.orders:
                orders_item = orders_item_data.to_dict()
                orders.append(orders_item)

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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if orders is not UNSET:
            field_dict["orders"] = orders
        if trades is not UNSET:
            field_dict["trades"] = trades
        if positions is not UNSET:
            field_dict["positions"] = positions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.calculated_position_state import CalculatedPositionState
        from ..models.dynamic_order_state import DynamicOrderState
        from ..models.calculated_trade_state import CalculatedTradeState

        d = src_dict.copy()
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

        orders = []
        _orders = d.pop("orders", UNSET)
        for orders_item_data in _orders or []:
            orders_item = DynamicOrderState.from_dict(orders_item_data)

            orders.append(orders_item)

        trades = []
        _trades = d.pop("trades", UNSET)
        for trades_item_data in _trades or []:
            trades_item = CalculatedTradeState.from_dict(trades_item_data)

            trades.append(trades_item)

        positions = []
        _positions = d.pop("positions", UNSET)
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
