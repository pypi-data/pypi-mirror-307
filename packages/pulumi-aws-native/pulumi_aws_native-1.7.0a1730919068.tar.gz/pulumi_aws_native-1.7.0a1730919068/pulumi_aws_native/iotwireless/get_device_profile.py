# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from . import outputs
from .. import outputs as _root_outputs

__all__ = [
    'GetDeviceProfileResult',
    'AwaitableGetDeviceProfileResult',
    'get_device_profile',
    'get_device_profile_output',
]

@pulumi.output_type
class GetDeviceProfileResult:
    def __init__(__self__, arn=None, id=None, lo_ra_wan=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lo_ra_wan and not isinstance(lo_ra_wan, dict):
            raise TypeError("Expected argument 'lo_ra_wan' to be a dict")
        pulumi.set(__self__, "lo_ra_wan", lo_ra_wan)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Service profile Arn. Returned after successful create.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Service profile Id. Returned after successful create.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="loRaWan")
    def lo_ra_wan(self) -> Optional['outputs.DeviceProfileLoRaWanDeviceProfile']:
        """
        LoRaWANDeviceProfile supports all LoRa specific attributes for service profile for CreateDeviceProfile operation
        """
        return pulumi.get(self, "lo_ra_wan")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of service profile
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of key-value pairs that contain metadata for the device profile.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDeviceProfileResult(GetDeviceProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeviceProfileResult(
            arn=self.arn,
            id=self.id,
            lo_ra_wan=self.lo_ra_wan,
            name=self.name,
            tags=self.tags)


def get_device_profile(id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeviceProfileResult:
    """
    Device Profile's resource schema demonstrating some basic constructs and validation rules.


    :param str id: Service profile Id. Returned after successful create.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iotwireless:getDeviceProfile', __args__, opts=opts, typ=GetDeviceProfileResult).value

    return AwaitableGetDeviceProfileResult(
        arn=pulumi.get(__ret__, 'arn'),
        id=pulumi.get(__ret__, 'id'),
        lo_ra_wan=pulumi.get(__ret__, 'lo_ra_wan'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_device_profile_output(id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeviceProfileResult]:
    """
    Device Profile's resource schema demonstrating some basic constructs and validation rules.


    :param str id: Service profile Id. Returned after successful create.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iotwireless:getDeviceProfile', __args__, opts=opts, typ=GetDeviceProfileResult)
    return __ret__.apply(lambda __response__: GetDeviceProfileResult(
        arn=pulumi.get(__response__, 'arn'),
        id=pulumi.get(__response__, 'id'),
        lo_ra_wan=pulumi.get(__response__, 'lo_ra_wan'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
