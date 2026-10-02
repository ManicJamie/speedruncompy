from datetime import datetime, tzinfo, timezone
from json import JSONEncoder
from typing import Any, ClassVar, Mapping, Self, Annotated

from pydantic import BaseModel, ConfigDict, model_validator, PlainSerializer, WithJsonSchema, BeforeValidator

from bidict import frozenbidict, BidirectionalMapping

from .. import config

class SpeedrunModel(BaseModel, ser_json_timedelta='float', extra='allow'):
    __condenser_map__: ClassVar[BidirectionalMapping[str, str]] = frozenbidict()
    """Internal mapping of list fields into dict fields, used for constructing dicts at runtime.
    
    Also used by paginated responses to condense lists into a single page."""
    
    __condenser_overrides__: ClassVar[dict[str, str]] = {}
    """Internal mapping of list fields' id names. Used for some types that have a PKEY not named 'id'."""

    @model_validator(mode='after')
    def create_condensed_dicts(self) -> Self:
        for source_field_name, target_field_name in self.__condenser_map__.items():
            source_list = getattr(self, source_field_name)
            setattr(self, target_field_name, 
                    {getattr(item, self.__condenser_overrides__.get(source_field_name, "id")): item 
                     for item in (source_list if source_list is not None else [])})
        
        return self

class ModelEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.model_dump()
        return super().default(o)
    
# Datatypes for transparent conversion

def unix_to_datetime(unix: int) -> datetime:
    return datetime.fromtimestamp(unix, timezone.utc)

def _validate_timestamp(field: datetime | str):
    if isinstance(field, str):
        return datetime.fromisoformat(field)
    return field

def _dump_timestamp(field: datetime):
    return field.isoformat().replace("+00:00", "Z")

Timestamp_ = Annotated[datetime, 
                      PlainSerializer(_dump_timestamp, return_type=str),
                      BeforeValidator(_validate_timestamp, json_schema_input_type=str)]
"""
Python side: `datetime` object
SRC side: RFC 3339 datetime string
"""

def _validate_int(field: int | str):
    if isinstance(field, str):
        return int(field)
    return field

Int64_ = Annotated[int,
                   PlainSerializer(int.__str__, return_type=str),
                   BeforeValidator(_validate_int, json_schema_input_type=str)
                   ]
"""
Python side: `int`
SRC side: integer string
"""

def _validate_duration(field: float | str):
    if isinstance(field, str):
        return float(field.removesuffix("s"))
    return field

def _dump_duration(field: float):
    return f"{field}s"

Duration_ = Annotated[float,
                        PlainSerializer(_dump_duration, return_type=str),
                        BeforeValidator(_validate_duration, json_schema_input_type=str)
                     ]
"""
Python side: `float`
SRC side: `0.0s`
"""