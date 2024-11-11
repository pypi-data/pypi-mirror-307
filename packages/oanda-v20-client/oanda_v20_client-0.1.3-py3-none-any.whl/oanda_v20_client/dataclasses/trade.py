from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .stop_loss_order import StopLossOrder
from .take_profit_order import TakeProfitOrder
from .trade_state import TradeState
from .trailing_stop_loss_order import TrailingStopLossOrder
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trade":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
