from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .liquidity_regeneration_schedule_step import LiquidityRegenerationScheduleStep
from typing import List, TypeVar, Union

T = TypeVar("T", bound="LiquidityRegenerationSchedule")


@dataclasses.dataclass
class LiquidityRegenerationSchedule:
    """A LiquidityRegenerationSchedule indicates how liquidity that is used when filling an Order for an instrument is
    regenerated following the fill.  A liquidity regeneration schedule will be in effect until the timestamp of its
    final step, but may be replaced by a schedule created for an Order of the same instrument that is filled while it is
    still in effect.

        Attributes:
            steps (Union[Unset, List['LiquidityRegenerationScheduleStep']]): The steps in the Liquidity Regeneration
                Schedule"""

    steps: Union[Unset, List["LiquidityRegenerationScheduleStep"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LiquidityRegenerationSchedule":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
