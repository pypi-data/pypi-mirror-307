from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_client_extensions_modify_reject_transaction import (
    OrderClientExtensionsModifyRejectTransaction,
)
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="SetOrderClientExtensionsResponse400")


@dataclasses.dataclass
class SetOrderClientExtensionsResponse400:
    """Attributes:
    order_client_extensions_modify_reject_transaction (Union[Unset, OrderClientExtensionsModifyRejectTransaction]):
        A OrderClientExtensionsModifyRejectTransaction represents the rejection of the modification of an Order's Client
        Extensions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    order_client_extensions_modify_reject_transaction: Optional[
        "OrderClientExtensionsModifyRejectTransaction"
    ]
    last_transaction_id: Optional[str]
    related_transaction_i_ds: Optional[List[str]]
    error_code: Optional[str]
    error_message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SetOrderClientExtensionsResponse400":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
