from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_price import ClientPrice
from .order_fill_transaction_reason import OrderFillTransactionReason
from .order_fill_transaction_reason import check_order_fill_transaction_reason
from .order_fill_transaction_type import OrderFillTransactionType
from .order_fill_transaction_type import check_order_fill_transaction_type
from .trade_open import TradeOpen
from .trade_reduce import TradeReduce
from types import Unset
from typing import List, Optional, Type, TypeVar

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

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[OrderFillTransactionType]
    order_id: Optional[str]
    client_order_id: Optional[str]
    instrument: Optional[str]
    units: Optional[str]
    gain_quote_home_conversion_factor: Optional[str]
    loss_quote_home_conversion_factor: Optional[str]
    price: Optional[str]
    full_vwap: Optional[str]
    full_price: Optional["ClientPrice"]
    reason: Optional[OrderFillTransactionReason]
    pl: Optional[str]
    financing: Optional[str]
    commission: Optional[str]
    guaranteed_execution_fee: Optional[str]
    account_balance: Optional[str]
    trade_opened: Optional["TradeOpen"]
    trades_closed: Optional[List["TradeReduce"]]
    trade_reduced: Optional["TradeReduce"]
    half_spread_cost: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_price import ClientPrice
        from .trade_open import TradeOpen
        from .trade_reduce import TradeReduce

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[OrderFillTransactionType]
        if _type is None:
            type = None
        else:
            type = check_order_fill_transaction_type(_type)
        order_id = d.pop("orderID", None)
        client_order_id = d.pop("clientOrderID", None)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        gain_quote_home_conversion_factor = d.pop("gainQuoteHomeConversionFactor", None)
        loss_quote_home_conversion_factor = d.pop("lossQuoteHomeConversionFactor", None)
        price = d.pop("price", None)
        full_vwap = d.pop("fullVWAP", None)
        _full_price = d.pop("fullPrice", None)
        full_price: Optional[ClientPrice]
        if isinstance(_full_price, Unset):
            full_price = None
        else:
            full_price = ClientPrice.from_dict(_full_price)
        _reason = d.pop("reason", None)
        reason: Optional[OrderFillTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_order_fill_transaction_reason(_reason)
        pl = d.pop("pl", None)
        financing = d.pop("financing", None)
        commission = d.pop("commission", None)
        guaranteed_execution_fee = d.pop("guaranteedExecutionFee", None)
        account_balance = d.pop("accountBalance", None)
        _trade_opened = d.pop("tradeOpened", None)
        trade_opened: Optional[TradeOpen]
        if isinstance(_trade_opened, Unset):
            trade_opened = None
        else:
            trade_opened = TradeOpen.from_dict(_trade_opened)
        trades_closed = []
        _trades_closed = d.pop("tradesClosed", None)
        for trades_closed_item_data in _trades_closed or []:
            trades_closed_item = TradeReduce.from_dict(trades_closed_item_data)
            trades_closed.append(trades_closed_item)
        _trade_reduced = d.pop("tradeReduced", None)
        trade_reduced: Optional[TradeReduce]
        if isinstance(_trade_reduced, Unset):
            trade_reduced = None
        else:
            trade_reduced = TradeReduce.from_dict(_trade_reduced)
        half_spread_cost = d.pop("halfSpreadCost", None)
        order_fill_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            order_id=order_id,
            client_order_id=client_order_id,
            instrument=instrument,
            units=units,
            gain_quote_home_conversion_factor=gain_quote_home_conversion_factor,
            loss_quote_home_conversion_factor=loss_quote_home_conversion_factor,
            price=price,
            full_vwap=full_vwap,
            full_price=full_price,
            reason=reason,
            pl=pl,
            financing=financing,
            commission=commission,
            guaranteed_execution_fee=guaranteed_execution_fee,
            account_balance=account_balance,
            trade_opened=trade_opened,
            trades_closed=trades_closed,
            trade_reduced=trade_reduced,
            half_spread_cost=half_spread_cost,
        )
        order_fill_transaction.additional_properties = d
        return order_fill_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
