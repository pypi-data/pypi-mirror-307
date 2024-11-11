from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .trade_client_extensions_modify_transaction import (
    TradeClientExtensionsModifyTransaction,
)
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="SetTradeClientExtensionsResponse200")


@dataclasses.dataclass
class SetTradeClientExtensionsResponse200:
    """Attributes:
    trade_client_extensions_modify_transaction (Union[Unset, TradeClientExtensionsModifyTransaction]): A
        TradeClientExtensionsModifyTransaction represents the modification of a Trade's Client Extensions.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trade_client_extensions_modify_transaction: Optional[
        "TradeClientExtensionsModifyTransaction"
    ]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .trade_client_extensions_modify_transaction import (
            TradeClientExtensionsModifyTransaction,
        )

        d = src_dict.copy()
        _trade_client_extensions_modify_transaction = d.pop(
            "tradeClientExtensionsModifyTransaction", None
        )
        trade_client_extensions_modify_transaction: Optional[
            TradeClientExtensionsModifyTransaction
        ]
        if isinstance(_trade_client_extensions_modify_transaction, Unset):
            trade_client_extensions_modify_transaction = None
        else:
            trade_client_extensions_modify_transaction = (
                TradeClientExtensionsModifyTransaction.from_dict(
                    _trade_client_extensions_modify_transaction
                )
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        set_trade_client_extensions_response_200 = cls(
            trade_client_extensions_modify_transaction=trade_client_extensions_modify_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
        )
        set_trade_client_extensions_response_200.additional_properties = d
        return set_trade_client_extensions_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
