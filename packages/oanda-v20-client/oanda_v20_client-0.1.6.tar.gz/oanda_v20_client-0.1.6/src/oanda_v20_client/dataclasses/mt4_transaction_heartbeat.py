from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="MT4TransactionHeartbeat")


@dataclasses.dataclass
class MT4TransactionHeartbeat:
    """A TransactionHeartbeat object is injected into the Transaction stream to ensure that the HTTP connection remains
    active.

        Attributes:
            type (Union[Unset, str]): The string "HEARTBEAT"
            time (Union[Unset, str]): The date/time when the TransactionHeartbeat was created."""

    type: Optional[str]
    time: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MT4TransactionHeartbeat":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
