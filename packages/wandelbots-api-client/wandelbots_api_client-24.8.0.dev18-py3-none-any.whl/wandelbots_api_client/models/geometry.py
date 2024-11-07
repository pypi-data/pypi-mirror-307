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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.box import Box
from wandelbots_api_client.models.capsule import Capsule
from wandelbots_api_client.models.convex_hull import ConvexHull
from wandelbots_api_client.models.cylinder import Cylinder
from wandelbots_api_client.models.planner_pose import PlannerPose
from wandelbots_api_client.models.rectangle import Rectangle
from wandelbots_api_client.models.rectangular_capsule import RectangularCapsule
from wandelbots_api_client.models.sphere import Sphere
from typing import Optional, Set
from typing_extensions import Self

class Geometry(BaseModel):
    """
    A Geometry is defined by a shape and a pose.
    """ # noqa: E501
    sphere: Optional[Sphere] = None
    box: Optional[Box] = None
    rectangle: Optional[Rectangle] = None
    plane: Optional[Dict[str, Any]] = Field(default=None, description="Defines an x-y plane with infinite size.")
    cylinder: Optional[Cylinder] = None
    convex_hull: Optional[ConvexHull] = None
    capsule: Optional[Capsule] = None
    rectangular_capsule: Optional[RectangularCapsule] = None
    compound: Optional[Compound] = None
    init_pose: PlannerPose
    id: Optional[StrictStr] = Field(default=None, description="An identifier may be used to refer to this geometry, e.g. when giving feedback.")
    __properties: ClassVar[List[str]] = ["sphere", "box", "rectangle", "plane", "cylinder", "convex_hull", "capsule", "rectangular_capsule", "compound", "init_pose", "id"]

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
        """Create an instance of Geometry from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of sphere
        if self.sphere:
            _dict['sphere'] = self.sphere.to_dict()
        # override the default output from pydantic by calling `to_dict()` of box
        if self.box:
            _dict['box'] = self.box.to_dict()
        # override the default output from pydantic by calling `to_dict()` of rectangle
        if self.rectangle:
            _dict['rectangle'] = self.rectangle.to_dict()
        # override the default output from pydantic by calling `to_dict()` of cylinder
        if self.cylinder:
            _dict['cylinder'] = self.cylinder.to_dict()
        # override the default output from pydantic by calling `to_dict()` of convex_hull
        if self.convex_hull:
            _dict['convex_hull'] = self.convex_hull.to_dict()
        # override the default output from pydantic by calling `to_dict()` of capsule
        if self.capsule:
            _dict['capsule'] = self.capsule.to_dict()
        # override the default output from pydantic by calling `to_dict()` of rectangular_capsule
        if self.rectangular_capsule:
            _dict['rectangular_capsule'] = self.rectangular_capsule.to_dict()
        # override the default output from pydantic by calling `to_dict()` of compound
        if self.compound:
            _dict['compound'] = self.compound.to_dict()
        # override the default output from pydantic by calling `to_dict()` of init_pose
        if self.init_pose:
            _dict['init_pose'] = self.init_pose.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Geometry from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "sphere": Sphere.from_dict(obj["sphere"]) if obj.get("sphere") is not None else None,
            "box": Box.from_dict(obj["box"]) if obj.get("box") is not None else None,
            "rectangle": Rectangle.from_dict(obj["rectangle"]) if obj.get("rectangle") is not None else None,
            "plane": obj.get("plane"),
            "cylinder": Cylinder.from_dict(obj["cylinder"]) if obj.get("cylinder") is not None else None,
            "convex_hull": ConvexHull.from_dict(obj["convex_hull"]) if obj.get("convex_hull") is not None else None,
            "capsule": Capsule.from_dict(obj["capsule"]) if obj.get("capsule") is not None else None,
            "rectangular_capsule": RectangularCapsule.from_dict(obj["rectangular_capsule"]) if obj.get("rectangular_capsule") is not None else None,
            "compound": Compound.from_dict(obj["compound"]) if obj.get("compound") is not None else None,
            "init_pose": PlannerPose.from_dict(obj["init_pose"]) if obj.get("init_pose") is not None else None,
            "id": obj.get("id")
        })
        return _obj

from wandelbots_api_client.models.compound import Compound
# TODO: Rewrite to not use raise_errors
Geometry.model_rebuild(raise_errors=False)

