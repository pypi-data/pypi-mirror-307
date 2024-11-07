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
    'GetDeviceResult',
    'AwaitableGetDeviceResult',
    'get_device',
    'get_device_output',
]

@pulumi.output_type
class GetDeviceResult:
    def __init__(__self__, aws_location=None, created_at=None, description=None, device_arn=None, device_id=None, location=None, model=None, serial_number=None, site_id=None, state=None, tags=None, type=None, vendor=None):
        if aws_location and not isinstance(aws_location, dict):
            raise TypeError("Expected argument 'aws_location' to be a dict")
        pulumi.set(__self__, "aws_location", aws_location)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if device_arn and not isinstance(device_arn, str):
            raise TypeError("Expected argument 'device_arn' to be a str")
        pulumi.set(__self__, "device_arn", device_arn)
        if device_id and not isinstance(device_id, str):
            raise TypeError("Expected argument 'device_id' to be a str")
        pulumi.set(__self__, "device_id", device_id)
        if location and not isinstance(location, dict):
            raise TypeError("Expected argument 'location' to be a dict")
        pulumi.set(__self__, "location", location)
        if model and not isinstance(model, str):
            raise TypeError("Expected argument 'model' to be a str")
        pulumi.set(__self__, "model", model)
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if site_id and not isinstance(site_id, str):
            raise TypeError("Expected argument 'site_id' to be a str")
        pulumi.set(__self__, "site_id", site_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vendor and not isinstance(vendor, str):
            raise TypeError("Expected argument 'vendor' to be a str")
        pulumi.set(__self__, "vendor", vendor)

    @property
    @pulumi.getter(name="awsLocation")
    def aws_location(self) -> Optional['outputs.DeviceAwsLocation']:
        """
        The Amazon Web Services location of the device, if applicable.
        """
        return pulumi.get(self, "aws_location")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date and time that the device was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the device.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="deviceArn")
    def device_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the device.
        """
        return pulumi.get(self, "device_arn")

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> Optional[str]:
        """
        The ID of the device.
        """
        return pulumi.get(self, "device_id")

    @property
    @pulumi.getter
    def location(self) -> Optional['outputs.DeviceLocation']:
        """
        The site location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def model(self) -> Optional[str]:
        """
        The device model
        """
        return pulumi.get(self, "model")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[str]:
        """
        The device serial number.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> Optional[str]:
        """
        The site ID.
        """
        return pulumi.get(self, "site_id")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the device.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the device.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The device type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def vendor(self) -> Optional[str]:
        """
        The device vendor.
        """
        return pulumi.get(self, "vendor")


class AwaitableGetDeviceResult(GetDeviceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeviceResult(
            aws_location=self.aws_location,
            created_at=self.created_at,
            description=self.description,
            device_arn=self.device_arn,
            device_id=self.device_id,
            location=self.location,
            model=self.model,
            serial_number=self.serial_number,
            site_id=self.site_id,
            state=self.state,
            tags=self.tags,
            type=self.type,
            vendor=self.vendor)


def get_device(device_id: Optional[str] = None,
               global_network_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeviceResult:
    """
    The AWS::NetworkManager::Device type describes a device.


    :param str device_id: The ID of the device.
    :param str global_network_id: The ID of the global network.
    """
    __args__ = dict()
    __args__['deviceId'] = device_id
    __args__['globalNetworkId'] = global_network_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:networkmanager:getDevice', __args__, opts=opts, typ=GetDeviceResult).value

    return AwaitableGetDeviceResult(
        aws_location=pulumi.get(__ret__, 'aws_location'),
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        device_arn=pulumi.get(__ret__, 'device_arn'),
        device_id=pulumi.get(__ret__, 'device_id'),
        location=pulumi.get(__ret__, 'location'),
        model=pulumi.get(__ret__, 'model'),
        serial_number=pulumi.get(__ret__, 'serial_number'),
        site_id=pulumi.get(__ret__, 'site_id'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'),
        vendor=pulumi.get(__ret__, 'vendor'))
def get_device_output(device_id: Optional[pulumi.Input[str]] = None,
                      global_network_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeviceResult]:
    """
    The AWS::NetworkManager::Device type describes a device.


    :param str device_id: The ID of the device.
    :param str global_network_id: The ID of the global network.
    """
    __args__ = dict()
    __args__['deviceId'] = device_id
    __args__['globalNetworkId'] = global_network_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:networkmanager:getDevice', __args__, opts=opts, typ=GetDeviceResult)
    return __ret__.apply(lambda __response__: GetDeviceResult(
        aws_location=pulumi.get(__response__, 'aws_location'),
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        device_arn=pulumi.get(__response__, 'device_arn'),
        device_id=pulumi.get(__response__, 'device_id'),
        location=pulumi.get(__response__, 'location'),
        model=pulumi.get(__response__, 'model'),
        serial_number=pulumi.get(__response__, 'serial_number'),
        site_id=pulumi.get(__response__, 'site_id'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags'),
        type=pulumi.get(__response__, 'type'),
        vendor=pulumi.get(__response__, 'vendor')))
