from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trade_state import check_trade_state
from ..models.trade_state import TradeState
from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions
    from ..models.stop_loss_order import StopLossOrder
    from ..models.take_profit_order import TakeProfitOrder
    from ..models.trailing_stop_loss_order import TrailingStopLossOrder


T = TypeVar("T", bound="Trade")


@_attrs_define
class Trade:
    """The specification of a Trade within an Account. This includes the full representation of the Trade's dependent
    Orders in addition to the IDs of those Orders.

        Attributes:
            id (Union[Unset, str]): The Trade's identifier, unique within the Trade's Account.
            instrument (Union[Unset, str]): The Trade's Instrument.
            price (Union[Unset, str]): The execution price of the Trade.
            open_time (Union[Unset, str]): The date/time when the Trade was opened.
            state (Union[Unset, TradeState]): The current state of the Trade.
            initial_units (Union[Unset, str]): The initial size of the Trade. Negative values indicate a short Trade, and
                positive values indicate a long Trade.
            initial_margin_required (Union[Unset, str]): The margin required at the time the Trade was created. Note, this
                is the 'pure' margin required, it is not the 'effective' margin used that factors in the trade risk if a GSLO is
                attached to the trade.
            current_units (Union[Unset, str]): The number of units currently open for the Trade. This value is reduced to
                0.0 as the Trade is closed.
            realized_pl (Union[Unset, str]): The total profit/loss realized on the closed portion of the Trade.
            unrealized_pl (Union[Unset, str]): The unrealized profit/loss on the open portion of the Trade.
            margin_used (Union[Unset, str]): Margin currently used by the Trade.
            average_close_price (Union[Unset, str]): The average closing price of the Trade. Only present if the Trade has
                been closed or reduced at least once.
            closing_transaction_i_ds (Union[Unset, List[str]]): The IDs of the Transactions that have closed portions of
                this Trade.
            financing (Union[Unset, str]): The financing paid/collected for this Trade.
            close_time (Union[Unset, str]): The date/time when the Trade was fully closed. Only provided for Trades whose
                state is CLOSED.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            take_profit_order (Union[Unset, TakeProfitOrder]): A TakeProfitOrder is an order that is linked to an open Trade
                and created with a price threshold. The Order will be filled (closing the Trade) by the first price that is
                equal to or better than the threshold. A TakeProfitOrder cannot be used to open a new Position.
            stop_loss_order (Union[Unset, StopLossOrder]): A StopLossOrder is an order that is linked to an open Trade and
                created with a price threshold. The Order will be filled (closing the Trade) by the first price that is equal to
                or worse than the threshold. A StopLossOrder cannot be used to open a new Position.
            trailing_stop_loss_order (Union[Unset, TrailingStopLossOrder]): A TrailingStopLossOrder is an order that is
                linked to an open Trade and created with a price distance. The price distance is used to calculate a trailing
                stop value for the order that is in the losing direction from the market price at the time of the order's
                creation. The trailing stop value will follow the market price as it moves in the winning direction, and the
                order will filled (closing the Trade) by the first price that is equal to or worse than the trailing stop value.
                A TrailingStopLossOrder cannot be used to open a new Position.
    """

    id: Union[Unset, str] = UNSET
    instrument: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    open_time: Union[Unset, str] = UNSET
    state: Union[Unset, TradeState] = UNSET
    initial_units: Union[Unset, str] = UNSET
    initial_margin_required: Union[Unset, str] = UNSET
    current_units: Union[Unset, str] = UNSET
    realized_pl: Union[Unset, str] = UNSET
    unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    average_close_price: Union[Unset, str] = UNSET
    closing_transaction_i_ds: Union[Unset, List[str]] = UNSET
    financing: Union[Unset, str] = UNSET
    close_time: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_order: Union[Unset, "TakeProfitOrder"] = UNSET
    stop_loss_order: Union[Unset, "StopLossOrder"] = UNSET
    trailing_stop_loss_order: Union[Unset, "TrailingStopLossOrder"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        instrument = self.instrument

        price = self.price

        open_time = self.open_time

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state

        initial_units = self.initial_units

        initial_margin_required = self.initial_margin_required

        current_units = self.current_units

        realized_pl = self.realized_pl

        unrealized_pl = self.unrealized_pl

        margin_used = self.margin_used

        average_close_price = self.average_close_price

        closing_transaction_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.closing_transaction_i_ds, Unset):
            closing_transaction_i_ds = self.closing_transaction_i_ds

        financing = self.financing

        close_time = self.close_time

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        take_profit_order: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_order, Unset):
            take_profit_order = self.take_profit_order.to_dict()

        stop_loss_order: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_order, Unset):
            stop_loss_order = self.stop_loss_order.to_dict()

        trailing_stop_loss_order: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trailing_stop_loss_order, Unset):
            trailing_stop_loss_order = self.trailing_stop_loss_order.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if price is not UNSET:
            field_dict["price"] = price
        if open_time is not UNSET:
            field_dict["openTime"] = open_time
        if state is not UNSET:
            field_dict["state"] = state
        if initial_units is not UNSET:
            field_dict["initialUnits"] = initial_units
        if initial_margin_required is not UNSET:
            field_dict["initialMarginRequired"] = initial_margin_required
        if current_units is not UNSET:
            field_dict["currentUnits"] = current_units
        if realized_pl is not UNSET:
            field_dict["realizedPL"] = realized_pl
        if unrealized_pl is not UNSET:
            field_dict["unrealizedPL"] = unrealized_pl
        if margin_used is not UNSET:
            field_dict["marginUsed"] = margin_used
        if average_close_price is not UNSET:
            field_dict["averageClosePrice"] = average_close_price
        if closing_transaction_i_ds is not UNSET:
            field_dict["closingTransactionIDs"] = closing_transaction_i_ds
        if financing is not UNSET:
            field_dict["financing"] = financing
        if close_time is not UNSET:
            field_dict["closeTime"] = close_time
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if take_profit_order is not UNSET:
            field_dict["takeProfitOrder"] = take_profit_order
        if stop_loss_order is not UNSET:
            field_dict["stopLossOrder"] = stop_loss_order
        if trailing_stop_loss_order is not UNSET:
            field_dict["trailingStopLossOrder"] = trailing_stop_loss_order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions
        from ..models.stop_loss_order import StopLossOrder
        from ..models.take_profit_order import TakeProfitOrder
        from ..models.trailing_stop_loss_order import TrailingStopLossOrder

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        instrument = d.pop("instrument", UNSET)

        price = d.pop("price", UNSET)

        open_time = d.pop("openTime", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, TradeState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = check_trade_state(_state)

        initial_units = d.pop("initialUnits", UNSET)

        initial_margin_required = d.pop("initialMarginRequired", UNSET)

        current_units = d.pop("currentUnits", UNSET)

        realized_pl = d.pop("realizedPL", UNSET)

        unrealized_pl = d.pop("unrealizedPL", UNSET)

        margin_used = d.pop("marginUsed", UNSET)

        average_close_price = d.pop("averageClosePrice", UNSET)

        closing_transaction_i_ds = cast(
            List[str], d.pop("closingTransactionIDs", UNSET)
        )

        financing = d.pop("financing", UNSET)

        close_time = d.pop("closeTime", UNSET)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        _take_profit_order = d.pop("takeProfitOrder", UNSET)
        take_profit_order: Union[Unset, TakeProfitOrder]
        if isinstance(_take_profit_order, Unset):
            take_profit_order = UNSET
        else:
            take_profit_order = TakeProfitOrder.from_dict(_take_profit_order)

        _stop_loss_order = d.pop("stopLossOrder", UNSET)
        stop_loss_order: Union[Unset, StopLossOrder]
        if isinstance(_stop_loss_order, Unset):
            stop_loss_order = UNSET
        else:
            stop_loss_order = StopLossOrder.from_dict(_stop_loss_order)

        _trailing_stop_loss_order = d.pop("trailingStopLossOrder", UNSET)
        trailing_stop_loss_order: Union[Unset, TrailingStopLossOrder]
        if isinstance(_trailing_stop_loss_order, Unset):
            trailing_stop_loss_order = UNSET
        else:
            trailing_stop_loss_order = TrailingStopLossOrder.from_dict(
                _trailing_stop_loss_order
            )

        trade = cls(
            id=id,
            instrument=instrument,
            price=price,
            open_time=open_time,
            state=state,
            initial_units=initial_units,
            initial_margin_required=initial_margin_required,
            current_units=current_units,
            realized_pl=realized_pl,
            unrealized_pl=unrealized_pl,
            margin_used=margin_used,
            average_close_price=average_close_price,
            closing_transaction_i_ds=closing_transaction_i_ds,
            financing=financing,
            close_time=close_time,
            client_extensions=client_extensions,
            take_profit_order=take_profit_order,
            stop_loss_order=stop_loss_order,
            trailing_stop_loss_order=trailing_stop_loss_order,
        )

        trade.additional_properties = d
        return trade

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
