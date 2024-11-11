from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .trade_client_extensions_modify_reject_transaction import (
    TradeClientExtensionsModifyRejectTransaction,
)
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="SetTradeClientExtensionsResponse404")


@dataclasses.dataclass
class SetTradeClientExtensionsResponse404:
    """Attributes:
    trade_client_extensions_modify_reject_transaction (Union[Unset, TradeClientExtensionsModifyRejectTransaction]):
        A TradeClientExtensionsModifyRejectTransaction represents the rejection of the modification of a Trade's Client
        Extensions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account. Only
        present if the Account exists.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request. Only present if the Account exists.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    trade_client_extensions_modify_reject_transaction: Optional[
        "TradeClientExtensionsModifyRejectTransaction"
    ]
    last_transaction_id: Optional[str]
    related_transaction_i_ds: Optional[List[str]]
    error_code: Optional[str]
    error_message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetTradeClientExtensionsResponse404":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
