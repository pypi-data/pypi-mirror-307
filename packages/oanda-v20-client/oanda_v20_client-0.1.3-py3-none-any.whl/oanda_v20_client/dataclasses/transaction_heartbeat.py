from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="TransactionHeartbeat")


@dataclasses.dataclass
class TransactionHeartbeat:
    """A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains
    active.

        Attributes:
            type (Union[Unset, str]): The string "HEARTBEAT"
            last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
            time (Union[Unset, str]): The date/time when the TransactionHeartbeat was created."""

    type: Union[Unset, str] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransactionHeartbeat":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
