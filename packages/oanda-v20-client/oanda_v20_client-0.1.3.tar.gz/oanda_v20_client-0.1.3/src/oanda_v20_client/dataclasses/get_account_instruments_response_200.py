from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .instrument import Instrument
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="GetAccountInstrumentsResponse200")


@dataclasses.dataclass
class GetAccountInstrumentsResponse200:
    """Attributes:
    instruments (Union[Unset, List['Instrument']]): The requested list of instruments.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account."""

    instruments: Union[Unset, List["Instrument"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetAccountInstrumentsResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
