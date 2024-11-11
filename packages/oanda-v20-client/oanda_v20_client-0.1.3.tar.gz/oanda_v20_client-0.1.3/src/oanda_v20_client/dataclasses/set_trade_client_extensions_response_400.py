from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .trade_client_extensions_modify_reject_transaction import (
    TradeClientExtensionsModifyRejectTransaction,
)
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="SetTradeClientExtensionsResponse400")


@dataclasses.dataclass
class SetTradeClientExtensionsResponse400:
    """Attributes:
    trade_client_extensions_modify_reject_transaction (Union[Unset, TradeClientExtensionsModifyRejectTransaction]):
        A TradeClientExtensionsModifyRejectTransaction represents the rejection of the modification of a Trade's Client
        Extensions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    trade_client_extensions_modify_reject_transaction: Union[
        Unset, "TradeClientExtensionsModifyRejectTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    error_code: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetTradeClientExtensionsResponse400":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
