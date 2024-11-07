# coding: utf-8

"""
    Wandelbots Nova Public API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class TriggerType(str, Enum):
    """
    The type of the trigger.
    """

    """
    allowed enum values
    """
    OPCUA_NODE_VALUE = 'opcua_node_value'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TriggerType from a JSON string"""
        return cls(json.loads(json_str))


