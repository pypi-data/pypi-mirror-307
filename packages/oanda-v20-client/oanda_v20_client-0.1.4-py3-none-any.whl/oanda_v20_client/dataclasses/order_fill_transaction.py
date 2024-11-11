from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_price import ClientPrice
from .order_fill_transaction_reason import OrderFillTransactionReason
from .order_fill_transaction_type import OrderFillTransactionType
from .trade_open import TradeOpen
from .trade_reduce import TradeReduce
from typing import List, TypeVar, Union

T = TypeVar("T", bound="OrderFillTransaction")


@dataclasses.dataclass
class OrderFillTransaction:
    """An OrderFillTransaction represents the filling of an Order in the client's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, OrderFillTransactionType]): The Type of the Transaction. Always set to "ORDER_FILL" for an
            OrderFillTransaction.
        order_id (Union[Unset, str]): The ID of the Order filled.
        client_order_id (Union[Unset, str]): The client Order ID of the Order filled (only provided if the client has
            assigned one).
        instrument (Union[Unset, str]): The name of the filled Order's instrument.
        units (Union[Unset, str]): The number of units filled by the OrderFill.
        gain_quote_home_conversion_factor (Union[Unset, str]): This is the conversion factor in effect for the Account
            at the time of the OrderFill for converting any gains realized in Instrument quote units into units of the
            Account's home currency.
        loss_quote_home_conversion_factor (Union[Unset, str]): This is the conversion factor in effect for the Account
            at the time of the OrderFill for converting any losses realized in Instrument quote units into units of the
            Account's home currency.
        price (Union[Unset, str]): This field is now deprecated and should no longer be used. The individual
            tradesClosed, tradeReduced and tradeOpened fields contain the exact/official price each unit was filled at.
        full_vwap (Union[Unset, str]): The price that all of the units of the OrderFill should have been filled at, in
            the absence of guaranteed price execution. This factors in the Account's current ClientPrice, used liquidity and
            the units of the OrderFill only. If no Trades were closed with their price clamped for guaranteed stop loss
            enforcement, then this value will match the price fields of each Trade opened, closed, and reduced, and they
            will all be the exact same.
        full_price (Union[Unset, ClientPrice]): The specification of an Account-specific Price.
        reason (Union[Unset, OrderFillTransactionReason]): The reason that an Order was filled
        pl (Union[Unset, str]): The profit or loss incurred when the Order was filled.
        financing (Union[Unset, str]): The financing paid or collected when the Order was filled.
        commission (Union[Unset, str]): The commission charged in the Account's home currency as a result of filling the
            Order. The commission is always represented as a positive quantity of the Account's home currency, however it
            reduces the balance in the Account.
        guaranteed_execution_fee (Union[Unset, str]): The total guaranteed execution fees charged for all Trades opened,
            closed or reduced with guaranteed Stop Loss Orders.
        account_balance (Union[Unset, str]): The Account's balance after the Order was filled.
        trade_opened (Union[Unset, TradeOpen]): A TradeOpen object represents a Trade for an instrument that was opened
            in an Account. It is found embedded in Transactions that affect the position of an instrument in the Account,
            specifically the OrderFill Transaction.
        trades_closed (Union[Unset, List['TradeReduce']]): The Trades that were closed when the Order was filled (only
            provided if filling the Order resulted in a closing open Trades).
        trade_reduced (Union[Unset, TradeReduce]): A TradeReduce object represents a Trade for an instrument that was
            reduced (either partially or fully) in an Account. It is found embedded in Transactions that affect the position
            of an instrument in the account, specifically the OrderFill Transaction.
        half_spread_cost (Union[Unset, str]): The half spread cost for the OrderFill, which is the sum of the
            halfSpreadCost values in the tradeOpened, tradesClosed and tradeReduced fields. This can be a positive or
            negative value and is represented in the home currency of the Account."""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, OrderFillTransactionType] = UNSET
    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    gain_quote_home_conversion_factor: Union[Unset, str] = UNSET
    loss_quote_home_conversion_factor: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    full_vwap: Union[Unset, str] = UNSET
    full_price: Union[Unset, "ClientPrice"] = UNSET
    reason: Union[Unset, OrderFillTransactionReason] = UNSET
    pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    commission: Union[Unset, str] = UNSET
    guaranteed_execution_fee: Union[Unset, str] = UNSET
    account_balance: Union[Unset, str] = UNSET
    trade_opened: Union[Unset, "TradeOpen"] = UNSET
    trades_closed: Union[Unset, List["TradeReduce"]] = UNSET
    trade_reduced: Union[Unset, "TradeReduce"] = UNSET
    half_spread_cost: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderFillTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
