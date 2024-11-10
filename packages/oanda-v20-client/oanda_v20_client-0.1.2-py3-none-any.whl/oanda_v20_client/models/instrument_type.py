from typing import Literal, Set, cast

InstrumentType = Literal["CFD", "CURRENCY", "METAL"]

INSTRUMENT_TYPE_VALUES: Set[InstrumentType] = {
    "CFD",
    "CURRENCY",
    "METAL",
}


def check_instrument_type(value: str) -> InstrumentType:
    if value in INSTRUMENT_TYPE_VALUES:
        return cast(InstrumentType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INSTRUMENT_TYPE_VALUES!r}"
    )
