from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .create_transaction_type import CreateTransactionType
from .create_transaction_type import check_create_transaction_type
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CreateTransaction")


@dataclasses.dataclass
class CreateTransaction:
    """A CreateTransaction represents the creation of an Account.

    Attributes:
        id (Optional[str]): The Transaction's Identifier.
        time (Optional[str]): The date/time when the Transaction was created.
        user_id (Optional[int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Optional[str]): The ID of the Account the Transaction was created for.
        batch_id (Optional[str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Optional[str]): The Request ID of the request which generated the transaction.
        type (Optional[CreateTransactionType]): The Type of the Transaction. Always set to "CREATE" in a
            CreateTransaction.
        division_id (Optional[int]): The ID of the Division that the Account is in
        site_id (Optional[int]): The ID of the Site that the Account was created at
        account_user_id (Optional[int]): The ID of the user that the Account was created for
        account_number (Optional[int]): The number of the Account within the site/division/user
        home_currency (Optional[str]): The home currency of the Account"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[CreateTransactionType]
    division_id: Optional[int]
    site_id: Optional[int]
    account_user_id: Optional[int]
    account_number: Optional[int]
    home_currency: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[CreateTransactionType]
        if _type is None:
            type = None
        else:
            type = check_create_transaction_type(_type)
        division_id = d.pop("divisionID", None)
        site_id = d.pop("siteID", None)
        account_user_id = d.pop("accountUserID", None)
        account_number = d.pop("accountNumber", None)
        home_currency = d.pop("homeCurrency", None)
        create_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            division_id=division_id,
            site_id=site_id,
            account_user_id=account_user_id,
            account_number=account_number,
            home_currency=home_currency,
        )
        create_transaction.additional_properties = d
        return create_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
