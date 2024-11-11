from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .trade_client_extensions_modify_transaction import (
    TradeClientExtensionsModifyTransaction,
)
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="SetTradeClientExtensionsResponse200")


@dataclasses.dataclass
class SetTradeClientExtensionsResponse200:
    """Attributes:
    trade_client_extensions_modify_transaction (Union[Unset, TradeClientExtensionsModifyTransaction]): A
        TradeClientExtensionsModifyTransaction represents the modification of a Trade's Client Extensions.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    trade_client_extensions_modify_transaction: Union[
        Unset, "TradeClientExtensionsModifyTransaction"
    ] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetTradeClientExtensionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
