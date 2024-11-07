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
from wandelbots_api_client.v2.models.joint_limit_exceeded import JointLimitExceeded
from wandelbots_api_client.v2.models.joints import Joints
from wandelbots_api_client.v2.models.out_of_workspace import OutOfWorkspace
from wandelbots_api_client.v2.models.pose import Pose
from wandelbots_api_client.v2.models.safety_zone_violation import SafetyZoneViolation
from wandelbots_api_client.v2.models.singularity import Singularity
from typing import Optional, Set
from typing_extensions import Self

class PlanFailedOnTrajectoryResponse(BaseModel):
    """
    The planning failed. The motion can be executed until the defected command part starts.
    """ # noqa: E501
    motion: Optional[StrictStr] = Field(default=None, description="Identifier of the motion until the error.")
    description: Optional[StrictStr] = None
    last_valid_joint_position: Optional[Joints] = None
    last_valid_tcp_pose: Optional[Pose] = None
    error_location_on_trajectory: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Location on the trajectory where the error occurred. The location is defined as a floating point range from 0 to n, where 0 is the start of the trajectory and n is the end of the trajectory. n is the number commands. The decimal places represent the percentage of the defective command.")
    joint_limit_exceeded: Optional[JointLimitExceeded] = None
    singularity: Optional[Singularity] = None
    safety_zone_violation: Optional[SafetyZoneViolation] = None
    out_of_workspace: Optional[OutOfWorkspace] = None
    __properties: ClassVar[List[str]] = ["motion", "description", "last_valid_joint_position", "last_valid_tcp_pose", "error_location_on_trajectory", "joint_limit_exceeded", "singularity", "safety_zone_violation", "out_of_workspace"]

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
        """Create an instance of PlanFailedOnTrajectoryResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of last_valid_joint_position
        if self.last_valid_joint_position:
            _dict['last_valid_joint_position'] = self.last_valid_joint_position.to_dict()
        # override the default output from pydantic by calling `to_dict()` of last_valid_tcp_pose
        if self.last_valid_tcp_pose:
            _dict['last_valid_tcp_pose'] = self.last_valid_tcp_pose.to_dict()
        # override the default output from pydantic by calling `to_dict()` of joint_limit_exceeded
        if self.joint_limit_exceeded:
            _dict['joint_limit_exceeded'] = self.joint_limit_exceeded.to_dict()
        # override the default output from pydantic by calling `to_dict()` of singularity
        if self.singularity:
            _dict['singularity'] = self.singularity.to_dict()
        # override the default output from pydantic by calling `to_dict()` of safety_zone_violation
        if self.safety_zone_violation:
            _dict['safety_zone_violation'] = self.safety_zone_violation.to_dict()
        # override the default output from pydantic by calling `to_dict()` of out_of_workspace
        if self.out_of_workspace:
            _dict['out_of_workspace'] = self.out_of_workspace.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PlanFailedOnTrajectoryResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "motion": obj.get("motion"),
            "description": obj.get("description"),
            "last_valid_joint_position": Joints.from_dict(obj["last_valid_joint_position"]) if obj.get("last_valid_joint_position") is not None else None,
            "last_valid_tcp_pose": Pose.from_dict(obj["last_valid_tcp_pose"]) if obj.get("last_valid_tcp_pose") is not None else None,
            "error_location_on_trajectory": obj.get("error_location_on_trajectory"),
            "joint_limit_exceeded": JointLimitExceeded.from_dict(obj["joint_limit_exceeded"]) if obj.get("joint_limit_exceeded") is not None else None,
            "singularity": Singularity.from_dict(obj["singularity"]) if obj.get("singularity") is not None else None,
            "safety_zone_violation": SafetyZoneViolation.from_dict(obj["safety_zone_violation"]) if obj.get("safety_zone_violation") is not None else None,
            "out_of_workspace": OutOfWorkspace.from_dict(obj["out_of_workspace"]) if obj.get("out_of_workspace") is not None else None
        })
        return _obj


