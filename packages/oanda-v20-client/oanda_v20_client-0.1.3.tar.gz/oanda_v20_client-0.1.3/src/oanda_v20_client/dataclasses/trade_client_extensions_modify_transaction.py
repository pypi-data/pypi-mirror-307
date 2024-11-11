from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .trade_client_extensions_modify_transaction_type import (
    TradeClientExtensionsModifyTransactionType,
)
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="TradeClientExtensionsModifyTransaction")


@dataclasses.dataclass
class TradeClientExtensionsModifyTransaction:
    """A TradeClientExtensionsModifyTransaction represents the modification of a Trade's Client Extensions.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TradeClientExtensionsModifyTransactionType]): The Type of the Transaction. Always set to
            "TRADE_CLIENT_EXTENSIONS_MODIFY" for a TradeClientExtensionsModifyTransaction.
        trade_id (Union[Unset, str]): The ID of the Trade who's client extensions are to be modified.
        client_trade_id (Union[Unset, str]): The original Client ID of the Trade who's client extensions are to be
            modified.
        trade_client_extensions_modify (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to
            attach a clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this
            field if your account is associated with MT4."""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, TradeClientExtensionsModifyTransactionType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    trade_client_extensions_modify: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any]
    ) -> "TradeClientExtensionsModifyTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
