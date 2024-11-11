from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .daily_financing_transaction_account_financing_mode import (
    DailyFinancingTransactionAccountFinancingMode,
)
from .daily_financing_transaction_account_financing_mode import (
    check_daily_financing_transaction_account_financing_mode,
)
from .daily_financing_transaction_type import DailyFinancingTransactionType
from .daily_financing_transaction_type import check_daily_financing_transaction_type
from .position_financing import PositionFinancing
from types import Unset
from typing import List, Optional, Type, TypeVar

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

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[DailyFinancingTransactionType]
    financing: Optional[str]
    account_balance: Optional[str]
    account_financing_mode: Optional[DailyFinancingTransactionAccountFinancingMode]
    position_financings: Optional[List["PositionFinancing"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .position_financing import PositionFinancing

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[DailyFinancingTransactionType]
        if _type is None:
            type = None
        else:
            type = check_daily_financing_transaction_type(_type)
        financing = d.pop("financing", None)
        account_balance = d.pop("accountBalance", None)
        _account_financing_mode = d.pop("accountFinancingMode", None)
        account_financing_mode: Optional[DailyFinancingTransactionAccountFinancingMode]
        if isinstance(_account_financing_mode, Unset):
            account_financing_mode = None
        else:
            account_financing_mode = (
                check_daily_financing_transaction_account_financing_mode(
                    _account_financing_mode
                )
            )
        position_financings = []
        _position_financings = d.pop("positionFinancings", None)
        for position_financings_item_data in _position_financings or []:
            position_financings_item = PositionFinancing.from_dict(
                position_financings_item_data
            )
            position_financings.append(position_financings_item)
        daily_financing_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            financing=financing,
            account_balance=account_balance,
            account_financing_mode=account_financing_mode,
            position_financings=position_financings,
        )
        daily_financing_transaction.additional_properties = d
        return daily_financing_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
