# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 2.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from wandelbots_api_client.v2.models.limits_override import LimitsOverride
from typing import Optional, Set
from typing_extensions import Self

class MoveToTrajectoryViaJointPTPRequest(BaseModel):
    """
    Request to move the motion group via joint point-to-point to a given location on a planned motion. You must use this endpoint in order to start moving from an arbritrary location of the trajectory. Afterwards, you are able to call [streamMoveForward](streamMoveForward) or [streamMoveBackward](streamMoveBackward) to move along planned motion. Use the [stopExecution](stopExecution) endpoint to stop the motion gracefully. 
    """ # noqa: E501
    motion: StrictStr = Field(description="This represents the UUID of a motion. Every executable or partially executable motion is cached and an UUID is returned. Indicate the UUID to execute the motion or retrieve information on the motion.")
    location_on_trajectory: Union[StrictFloat, StrictInt] = Field(description="Gets the target location the robot should move to via joint point-to-point (moveJ). The location is a scalar value that defines a position along a path, typically ranging from 0 to `n`, where `n` denotes the number of motion commands. Each integer value of the location corresponds to a specific motion command, while non-integer values interpolate positions within the segments. The location is calculated from the joint path. ")
    limit_override: Optional[LimitsOverride] = None
    response_coordinate_system: Optional[StrictStr] = Field(default=None, description="Unique identifier addressing a coordinate system in which the responses should be converted. If not set, world coordinate system is used. ")
    __properties: ClassVar[List[str]] = ["motion", "location_on_trajectory", "limit_override", "response_coordinate_system"]

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
        """Create an instance of MoveToTrajectoryViaJointPTPRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of limit_override
        if self.limit_override:
            _dict['limit_override'] = self.limit_override.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MoveToTrajectoryViaJointPTPRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "motion": obj.get("motion"),
            "location_on_trajectory": obj.get("location_on_trajectory"),
            "limit_override": LimitsOverride.from_dict(obj["limit_override"]) if obj.get("limit_override") is not None else None,
            "response_coordinate_system": obj.get("response_coordinate_system")
        })
        return _obj


