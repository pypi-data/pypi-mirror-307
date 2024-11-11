from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .order_client_extensions_modify_transaction import (
    OrderClientExtensionsModifyTransaction,
)
from typing import List, TypeVar, Union

T = TypeVar("T", bound="SetOrderClientExtensionsResponse200")


@dataclasses.dataclass
class SetOrderClientExtensionsResponse200:
    """Attributes:
    order_client_extensions_modify_transaction (Union[Unset, OrderClientExtensionsModifyTransaction]): A
        OrderClientExtensionsModifyTransaction represents the modification of an Order's Client Extensions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request."""

    order_client_extensions_modify_transaction: Union[
        Unset, "OrderClientExtensionsModifyTransaction"
    ] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    related_transaction_i_ds: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetOrderClientExtensionsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
