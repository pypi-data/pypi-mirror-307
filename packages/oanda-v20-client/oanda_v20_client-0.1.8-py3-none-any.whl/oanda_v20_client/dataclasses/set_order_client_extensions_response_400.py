from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_client_extensions_modify_reject_transaction import (
    OrderClientExtensionsModifyRejectTransaction,
)
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_client_extensions_modify_reject_transaction import (
            OrderClientExtensionsModifyRejectTransaction,
        )

        d = src_dict.copy()
        _order_client_extensions_modify_reject_transaction = d.pop(
            "orderClientExtensionsModifyRejectTransaction", None
        )
        order_client_extensions_modify_reject_transaction: Optional[
            OrderClientExtensionsModifyRejectTransaction
        ]
        if isinstance(_order_client_extensions_modify_reject_transaction, Unset):
            order_client_extensions_modify_reject_transaction = None
        else:
            order_client_extensions_modify_reject_transaction = (
                OrderClientExtensionsModifyRejectTransaction.from_dict(
                    _order_client_extensions_modify_reject_transaction
                )
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        set_order_client_extensions_response_400 = cls(
            order_client_extensions_modify_reject_transaction=order_client_extensions_modify_reject_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
            error_code=error_code,
            error_message=error_message,
        )
        set_order_client_extensions_response_400.additional_properties = d
        return set_order_client_extensions_response_400

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
