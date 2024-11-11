from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_extensions import ClientExtensions
from .trade_summary_state import TradeSummaryState
from typing import List, TypeVar, Union

T = TypeVar("T", bound="TradeSummary")


@dataclasses.dataclass
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
                such an Order exists."""

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TradeSummary":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
