from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trade_summary_state import check_trade_summary_state
from ..models.trade_summary_state import TradeSummaryState
from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="TradeSummary")


@_attrs_define
class TradeSummary:
    """The summary of a Trade within an Account. This representation does not provide the full details of the Trade's
    dependent Orders.

        Attributes:
            id (Union[Unset, str]): The Trade's identifier, unique within the Trade's Account.
            instrument (Union[Unset, str]): The Trade's Instrument.
            price (Union[Unset, str]): The execution price of the Trade.
            open_time (Union[Unset, str]): The date/time when the Trade was opened.
            state (Union[Unset, TradeSummaryState]): The current state of the Trade.
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
            take_profit_order_id (Union[Unset, str]): ID of the Trade's Take Profit Order, only provided if such an Order
                exists.
            stop_loss_order_id (Union[Unset, str]): ID of the Trade's Stop Loss Order, only provided if such an Order
                exists.
            trailing_stop_loss_order_id (Union[Unset, str]): ID of the Trade's Trailing Stop Loss Order, only provided if
                such an Order exists.
    """

    id: Union[Unset, str] = UNSET
    instrument: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    open_time: Union[Unset, str] = UNSET
    state: Union[Unset, TradeSummaryState] = UNSET
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
    take_profit_order_id: Union[Unset, str] = UNSET
    stop_loss_order_id: Union[Unset, str] = UNSET
    trailing_stop_loss_order_id: Union[Unset, str] = UNSET
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

        take_profit_order_id = self.take_profit_order_id

        stop_loss_order_id = self.stop_loss_order_id

        trailing_stop_loss_order_id = self.trailing_stop_loss_order_id

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
        if take_profit_order_id is not UNSET:
            field_dict["takeProfitOrderID"] = take_profit_order_id
        if stop_loss_order_id is not UNSET:
            field_dict["stopLossOrderID"] = stop_loss_order_id
        if trailing_stop_loss_order_id is not UNSET:
            field_dict["trailingStopLossOrderID"] = trailing_stop_loss_order_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        instrument = d.pop("instrument", UNSET)

        price = d.pop("price", UNSET)

        open_time = d.pop("openTime", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, TradeSummaryState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = check_trade_summary_state(_state)

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

        take_profit_order_id = d.pop("takeProfitOrderID", UNSET)

        stop_loss_order_id = d.pop("stopLossOrderID", UNSET)

        trailing_stop_loss_order_id = d.pop("trailingStopLossOrderID", UNSET)

        trade_summary = cls(
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
            take_profit_order_id=take_profit_order_id,
            stop_loss_order_id=stop_loss_order_id,
            trailing_stop_loss_order_id=trailing_stop_loss_order_id,
        )

        trade_summary.additional_properties = d
        return trade_summary

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
