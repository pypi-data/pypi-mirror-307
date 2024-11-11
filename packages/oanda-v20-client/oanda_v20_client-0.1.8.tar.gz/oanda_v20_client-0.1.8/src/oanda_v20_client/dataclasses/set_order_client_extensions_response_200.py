from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_client_extensions_modify_transaction import (
    OrderClientExtensionsModifyTransaction,
)
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="SetOrderClientExtensionsResponse200")


@dataclasses.dataclass
class SetOrderClientExtensionsResponse200:
    """Attributes:
    order_client_extensions_modify_transaction (Union[Unset, OrderClientExtensionsModifyTransaction]): A
        OrderClientExtensionsModifyTransaction represents the modification of an Order's Client Extensions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request."""

    order_client_extensions_modify_transaction: Optional[
        "OrderClientExtensionsModifyTransaction"
    ]
    last_transaction_id: Optional[str]
    related_transaction_i_ds: Optional[List[str]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_client_extensions_modify_transaction import (
            OrderClientExtensionsModifyTransaction,
        )

        d = src_dict.copy()
        _order_client_extensions_modify_transaction = d.pop(
            "orderClientExtensionsModifyTransaction", None
        )
        order_client_extensions_modify_transaction: Optional[
            OrderClientExtensionsModifyTransaction
        ]
        if isinstance(_order_client_extensions_modify_transaction, Unset):
            order_client_extensions_modify_transaction = None
        else:
            order_client_extensions_modify_transaction = (
                OrderClientExtensionsModifyTransaction.from_dict(
                    _order_client_extensions_modify_transaction
                )
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        set_order_client_extensions_response_200 = cls(
            order_client_extensions_modify_transaction=order_client_extensions_modify_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
        )
        set_order_client_extensions_response_200.additional_properties = d
        return set_order_client_extensions_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
