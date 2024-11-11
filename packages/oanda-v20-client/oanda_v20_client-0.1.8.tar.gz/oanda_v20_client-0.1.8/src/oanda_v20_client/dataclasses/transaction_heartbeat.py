from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="TransactionHeartbeat")


@dataclasses.dataclass
class TransactionHeartbeat:
    """A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains
    active.

        Attributes:
            type (Union[Unset, str]): The string "HEARTBEAT"
            last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
            time (Union[Unset, str]): The date/time when the TransactionHeartbeat was created."""

    type: Optional[str]
    last_transaction_id: Optional[str]
    time: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", None)
        last_transaction_id = d.pop("lastTransactionID", None)
        time = d.pop("time", None)
        transaction_heartbeat = cls(
            type=type, last_transaction_id=last_transaction_id, time=time
        )
        transaction_heartbeat.additional_properties = d
        return transaction_heartbeat

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
