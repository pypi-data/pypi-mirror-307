from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .daily_financing_transaction_account_financing_mode import (
    DailyFinancingTransactionAccountFinancingMode,
)
from .daily_financing_transaction_type import DailyFinancingTransactionType
from .position_financing import PositionFinancing
from typing import List, TypeVar, Union

T = TypeVar("T", bound="DailyFinancingTransaction")


@dataclasses.dataclass
class DailyFinancingTransaction:
    """A DailyFinancingTransaction represents the daily payment/collection of financing for an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, DailyFinancingTransactionType]): The Type of the Transaction. Always set to "DAILY_FINANCING"
            for a DailyFinancingTransaction.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Account.
        account_balance (Union[Unset, str]): The Account's balance after daily financing.
        account_financing_mode (Union[Unset, DailyFinancingTransactionAccountFinancingMode]): The account financing mode
            at the time of the daily financing.
        position_financings (Union[Unset, List['PositionFinancing']]): The financing paid/collected for each Position in
            the Account."""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, DailyFinancingTransactionType] = UNSET
    financing: Union[Unset, str] = UNSET
    account_balance: Union[Unset, str] = UNSET
    account_financing_mode: Union[
        Unset, DailyFinancingTransactionAccountFinancingMode
    ] = UNSET
    position_financings: Union[Unset, List["PositionFinancing"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyFinancingTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
