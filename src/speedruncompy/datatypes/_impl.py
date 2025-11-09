from json import JSONEncoder
from typing import Any, ClassVar, Mapping, Self

from pydantic import BaseModel, ConfigDict, model_validator

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