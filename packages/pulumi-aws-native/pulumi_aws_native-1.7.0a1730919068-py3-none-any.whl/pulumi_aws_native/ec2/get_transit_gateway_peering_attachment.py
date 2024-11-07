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
    'GetTransitGatewayPeeringAttachmentResult',
    'AwaitableGetTransitGatewayPeeringAttachmentResult',
    'get_transit_gateway_peering_attachment',
    'get_transit_gateway_peering_attachment_output',
]

@pulumi.output_type
class GetTransitGatewayPeeringAttachmentResult:
    def __init__(__self__, creation_time=None, state=None, status=None, tags=None, transit_gateway_attachment_id=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if transit_gateway_attachment_id and not isinstance(transit_gateway_attachment_id, str):
            raise TypeError("Expected argument 'transit_gateway_attachment_id' to be a str")
        pulumi.set(__self__, "transit_gateway_attachment_id", transit_gateway_attachment_id)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        The time the transit gateway peering attachment was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the transit gateway peering attachment. Note that the initiating state has been deprecated.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def status(self) -> Optional['outputs.TransitGatewayPeeringAttachmentPeeringAttachmentStatus']:
        """
        The status of the transit gateway peering attachment.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the transit gateway peering attachment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> Optional[str]:
        """
        The ID of the transit gateway peering attachment.
        """
        return pulumi.get(self, "transit_gateway_attachment_id")


class AwaitableGetTransitGatewayPeeringAttachmentResult(GetTransitGatewayPeeringAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayPeeringAttachmentResult(
            creation_time=self.creation_time,
            state=self.state,
            status=self.status,
            tags=self.tags,
            transit_gateway_attachment_id=self.transit_gateway_attachment_id)


def get_transit_gateway_peering_attachment(transit_gateway_attachment_id: Optional[str] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayPeeringAttachmentResult:
    """
    The AWS::EC2::TransitGatewayPeeringAttachment type


    :param str transit_gateway_attachment_id: The ID of the transit gateway peering attachment.
    """
    __args__ = dict()
    __args__['transitGatewayAttachmentId'] = transit_gateway_attachment_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getTransitGatewayPeeringAttachment', __args__, opts=opts, typ=GetTransitGatewayPeeringAttachmentResult).value

    return AwaitableGetTransitGatewayPeeringAttachmentResult(
        creation_time=pulumi.get(__ret__, 'creation_time'),
        state=pulumi.get(__ret__, 'state'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        transit_gateway_attachment_id=pulumi.get(__ret__, 'transit_gateway_attachment_id'))
def get_transit_gateway_peering_attachment_output(transit_gateway_attachment_id: Optional[pulumi.Input[str]] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayPeeringAttachmentResult]:
    """
    The AWS::EC2::TransitGatewayPeeringAttachment type


    :param str transit_gateway_attachment_id: The ID of the transit gateway peering attachment.
    """
    __args__ = dict()
    __args__['transitGatewayAttachmentId'] = transit_gateway_attachment_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getTransitGatewayPeeringAttachment', __args__, opts=opts, typ=GetTransitGatewayPeeringAttachmentResult)
    return __ret__.apply(lambda __response__: GetTransitGatewayPeeringAttachmentResult(
        creation_time=pulumi.get(__response__, 'creation_time'),
        state=pulumi.get(__response__, 'state'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags'),
        transit_gateway_attachment_id=pulumi.get(__response__, 'transit_gateway_attachment_id')))
