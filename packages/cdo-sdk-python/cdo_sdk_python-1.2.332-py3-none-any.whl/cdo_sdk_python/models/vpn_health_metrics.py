# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class VpnHealthMetrics(BaseModel):
    """
    The vpn health metrics for the device.
    """ # noqa: E501
    active_ravpn_tunnels_avg: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The average number of active RA VPN tunnels.", alias="activeRavpnTunnelsAvg")
    inactive_ravpn_tunnels_avg: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The average number of inactive or down RA VPN tunnels.", alias="inactiveRavpnTunnelsAvg")
    peak_concur_ravpn_tunnels: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The peak concurrent RA VPN tunnels active since the last reset.", alias="peakConcurRavpnTunnels")
    active_s2svpn_tunnels_avg: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The average number of active S2S VPN tunnels.", alias="activeS2svpnTunnelsAvg")
    inactive_s2svpn_tunnels_avg: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The average number of inactive or down S2S VPN tunnels.", alias="inactiveS2svpnTunnelsAvg")
    peak_concur_s2svpn_tunnels: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="The peak concurrent S2S VPN tunnels active since the last reset.", alias="peakConcurS2svpnTunnels")
    __properties: ClassVar[List[str]] = ["activeRavpnTunnelsAvg", "inactiveRavpnTunnelsAvg", "peakConcurRavpnTunnels", "activeS2svpnTunnelsAvg", "inactiveS2svpnTunnelsAvg", "peakConcurS2svpnTunnels"]

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
        """Create an instance of VpnHealthMetrics from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of VpnHealthMetrics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "activeRavpnTunnelsAvg": obj.get("activeRavpnTunnelsAvg"),
            "inactiveRavpnTunnelsAvg": obj.get("inactiveRavpnTunnelsAvg"),
            "peakConcurRavpnTunnels": obj.get("peakConcurRavpnTunnels"),
            "activeS2svpnTunnelsAvg": obj.get("activeS2svpnTunnelsAvg"),
            "inactiveS2svpnTunnelsAvg": obj.get("inactiveS2svpnTunnelsAvg"),
            "peakConcurS2svpnTunnels": obj.get("peakConcurS2svpnTunnels")
        })
        return _obj


