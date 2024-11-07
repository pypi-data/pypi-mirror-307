# coding: utf-8

"""
    GraphScope FLEX HTTP SERVICE API

    This is a specification for GraphScope FLEX HTTP service based on the OpenAPI 3.0 specification. You can find out more details about specification at [doc](https://swagger.io/specification/v3/).

    The version of the OpenAPI document: 1.0.0
    Contact: graphscope@alibaba-inc.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from graphscope.flex.rest.models.get_graph_schema_response import GetGraphSchemaResponse
from graphscope.flex.rest.models.get_stored_proc_response import GetStoredProcResponse
from typing import Optional, Set
from typing_extensions import Self

class GetGraphResponse(BaseModel):
    """
    GetGraphResponse
    """ # noqa: E501
    id: StrictStr
    name: StrictStr
    description: Optional[StrictStr] = None
    store_type: Optional[StrictStr] = None
    creation_time: StrictStr
    data_update_time: StrictStr
    schema_update_time: StrictStr
    stored_procedures: Optional[List[GetStoredProcResponse]] = None
    var_schema: GetGraphSchemaResponse = Field(alias="schema")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["id", "name", "description", "store_type", "creation_time", "data_update_time", "schema_update_time", "stored_procedures", "schema"]

    @field_validator('store_type')
    def store_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['mutable_csr']):
            raise ValueError("must be one of enum values ('mutable_csr')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GetGraphResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * Fields in `self.additional_properties` are added to the output dict.
        """
        excluded_fields: Set[str] = set([
            "additional_properties",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in stored_procedures (list)
        _items = []
        if self.stored_procedures:
            for _item_stored_procedures in self.stored_procedures:
                if _item_stored_procedures:
                    _items.append(_item_stored_procedures.to_dict())
            _dict['stored_procedures'] = _items
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.var_schema:
            _dict['schema'] = self.var_schema.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetGraphResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "store_type": obj.get("store_type"),
            "creation_time": obj.get("creation_time"),
            "data_update_time": obj.get("data_update_time"),
            "schema_update_time": obj.get("schema_update_time"),
            "stored_procedures": [GetStoredProcResponse.from_dict(_item) for _item in obj["stored_procedures"]] if obj.get("stored_procedures") is not None else None,
            "schema": GetGraphSchemaResponse.from_dict(obj["schema"]) if obj.get("schema") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj


