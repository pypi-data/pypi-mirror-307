from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .create_transaction_type import CreateTransactionType
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="CreateTransaction")


@dataclasses.dataclass
class CreateTransaction:
    """A CreateTransaction represents the creation of an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, CreateTransactionType]): The Type of the Transaction. Always set to "CREATE" in a
            CreateTransaction.
        division_id (Union[Unset, int]): The ID of the Division that the Account is in
        site_id (Union[Unset, int]): The ID of the Site that the Account was created at
        account_user_id (Union[Unset, int]): The ID of the user that the Account was created for
        account_number (Union[Unset, int]): The number of the Account within the site/division/user
        home_currency (Union[Unset, str]): The home currency of the Account"""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, CreateTransactionType] = UNSET
    division_id: Union[Unset, int] = UNSET
    site_id: Union[Unset, int] = UNSET
    account_user_id: Union[Unset, int] = UNSET
    account_number: Union[Unset, int] = UNSET
    home_currency: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreateTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
