# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.limits_override import LimitsOverride
from wandelbots_api_client.models.motion_command_blending import MotionCommandBlending
from wandelbots_api_client.models.motion_command_path import MotionCommandPath
from typing import Optional, Set
from typing_extensions import Self

class MotionCommand(BaseModel):
    """
    MotionCommand
    """ # noqa: E501
    blending: Optional[MotionCommandBlending] = None
    limits_override: Optional[LimitsOverride] = Field(default=None, description="Limits override is used to override the global limits of the motion group for this segment of the motion. ")
    path: Optional[MotionCommandPath] = None
    __properties: ClassVar[List[str]] = ["blending", "limits_override", "path"]

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
        """Create an instance of MotionCommand from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of blending
        if self.blending:
            _dict['blending'] = self.blending.to_dict()
        # override the default output from pydantic by calling `to_dict()` of limits_override
        if self.limits_override:
            _dict['limits_override'] = self.limits_override.to_dict()
        # override the default output from pydantic by calling `to_dict()` of path
        if self.path:
            _dict['path'] = self.path.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MotionCommand from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "blending": MotionCommandBlending.from_dict(obj["blending"]) if obj.get("blending") is not None else None,
            "limits_override": LimitsOverride.from_dict(obj["limits_override"]) if obj.get("limits_override") is not None else None,
            "path": MotionCommandPath.from_dict(obj["path"]) if obj.get("path") is not None else None
        })
        return _obj


