from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .stop_loss_order import StopLossOrder
from .take_profit_order import TakeProfitOrder
from .trade_state import TradeState
from .trade_state import check_trade_state
from .trailing_stop_loss_order import TrailingStopLossOrder
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="Trade")


@dataclasses.dataclass
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
                A TrailingStopLossOrder cannot be used to open a new Position."""

    id: Optional[str]
    instrument: Optional[str]
    price: Optional[str]
    open_time: Optional[str]
    state: Optional[TradeState]
    initial_units: Optional[str]
    initial_margin_required: Optional[str]
    current_units: Optional[str]
    realized_pl: Optional[str]
    unrealized_pl: Optional[str]
    margin_used: Optional[str]
    average_close_price: Optional[str]
    closing_transaction_i_ds: Optional[List[str]]
    financing: Optional[str]
    close_time: Optional[str]
    client_extensions: Optional["ClientExtensions"]
    take_profit_order: Optional["TakeProfitOrder"]
    stop_loss_order: Optional["StopLossOrder"]
    trailing_stop_loss_order: Optional["TrailingStopLossOrder"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions
        from .trailing_stop_loss_order import TrailingStopLossOrder
        from .take_profit_order import TakeProfitOrder
        from .stop_loss_order import StopLossOrder

        d = src_dict.copy()
        id = d.pop("id", None)
        instrument = d.pop("instrument", None)
        price = d.pop("price", None)
        open_time = d.pop("openTime", None)
        _state = d.pop("state", None)
        state: Optional[TradeState]
        if isinstance(_state, Unset):
            state = None
        else:
            state = check_trade_state(_state)
        initial_units = d.pop("initialUnits", None)
        initial_margin_required = d.pop("initialMarginRequired", None)
        current_units = d.pop("currentUnits", None)
        realized_pl = d.pop("realizedPL", None)
        unrealized_pl = d.pop("unrealizedPL", None)
        margin_used = d.pop("marginUsed", None)
        average_close_price = d.pop("averageClosePrice", None)
        closing_transaction_i_ds = cast(List[str], d.pop("closingTransactionIDs", None))
        financing = d.pop("financing", None)
        close_time = d.pop("closeTime", None)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        _take_profit_order = d.pop("takeProfitOrder", None)
        take_profit_order: Optional[TakeProfitOrder]
        if isinstance(_take_profit_order, Unset):
            take_profit_order = None
        else:
            take_profit_order = TakeProfitOrder.from_dict(_take_profit_order)
        _stop_loss_order = d.pop("stopLossOrder", None)
        stop_loss_order: Optional[StopLossOrder]
        if isinstance(_stop_loss_order, Unset):
            stop_loss_order = None
        else:
            stop_loss_order = StopLossOrder.from_dict(_stop_loss_order)
        _trailing_stop_loss_order = d.pop("trailingStopLossOrder", None)
        trailing_stop_loss_order: Optional[TrailingStopLossOrder]
        if isinstance(_trailing_stop_loss_order, Unset):
            trailing_stop_loss_order = None
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
