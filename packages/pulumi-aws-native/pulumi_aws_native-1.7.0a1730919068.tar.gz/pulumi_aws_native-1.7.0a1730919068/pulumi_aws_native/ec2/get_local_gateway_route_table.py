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
from .. import outputs as _root_outputs

__all__ = [
    'GetLocalGatewayRouteTableResult',
    'AwaitableGetLocalGatewayRouteTableResult',
    'get_local_gateway_route_table',
    'get_local_gateway_route_table_output',
]

@pulumi.output_type
class GetLocalGatewayRouteTableResult:
    def __init__(__self__, local_gateway_route_table_arn=None, local_gateway_route_table_id=None, outpost_arn=None, owner_id=None, state=None, tags=None):
        if local_gateway_route_table_arn and not isinstance(local_gateway_route_table_arn, str):
            raise TypeError("Expected argument 'local_gateway_route_table_arn' to be a str")
        pulumi.set(__self__, "local_gateway_route_table_arn", local_gateway_route_table_arn)
        if local_gateway_route_table_id and not isinstance(local_gateway_route_table_id, str):
            raise TypeError("Expected argument 'local_gateway_route_table_id' to be a str")
        pulumi.set(__self__, "local_gateway_route_table_id", local_gateway_route_table_id)
        if outpost_arn and not isinstance(outpost_arn, str):
            raise TypeError("Expected argument 'outpost_arn' to be a str")
        pulumi.set(__self__, "outpost_arn", outpost_arn)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="localGatewayRouteTableArn")
    def local_gateway_route_table_arn(self) -> Optional[str]:
        """
        The ARN of the local gateway route table.
        """
        return pulumi.get(self, "local_gateway_route_table_arn")

    @property
    @pulumi.getter(name="localGatewayRouteTableId")
    def local_gateway_route_table_id(self) -> Optional[str]:
        """
        The ID of the local gateway route table.
        """
        return pulumi.get(self, "local_gateway_route_table_id")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> Optional[str]:
        """
        The ARN of the outpost.
        """
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[str]:
        """
        The owner of the local gateway route table.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the local gateway route table.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the local gateway route table.
        """
        return pulumi.get(self, "tags")


class AwaitableGetLocalGatewayRouteTableResult(GetLocalGatewayRouteTableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocalGatewayRouteTableResult(
            local_gateway_route_table_arn=self.local_gateway_route_table_arn,
            local_gateway_route_table_id=self.local_gateway_route_table_id,
            outpost_arn=self.outpost_arn,
            owner_id=self.owner_id,
            state=self.state,
            tags=self.tags)


def get_local_gateway_route_table(local_gateway_route_table_id: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocalGatewayRouteTableResult:
    """
    Describes a route table for a local gateway.


    :param str local_gateway_route_table_id: The ID of the local gateway route table.
    """
    __args__ = dict()
    __args__['localGatewayRouteTableId'] = local_gateway_route_table_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getLocalGatewayRouteTable', __args__, opts=opts, typ=GetLocalGatewayRouteTableResult).value

    return AwaitableGetLocalGatewayRouteTableResult(
        local_gateway_route_table_arn=pulumi.get(__ret__, 'local_gateway_route_table_arn'),
        local_gateway_route_table_id=pulumi.get(__ret__, 'local_gateway_route_table_id'),
        outpost_arn=pulumi.get(__ret__, 'outpost_arn'),
        owner_id=pulumi.get(__ret__, 'owner_id'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))
def get_local_gateway_route_table_output(local_gateway_route_table_id: Optional[pulumi.Input[str]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLocalGatewayRouteTableResult]:
    """
    Describes a route table for a local gateway.


    :param str local_gateway_route_table_id: The ID of the local gateway route table.
    """
    __args__ = dict()
    __args__['localGatewayRouteTableId'] = local_gateway_route_table_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getLocalGatewayRouteTable', __args__, opts=opts, typ=GetLocalGatewayRouteTableResult)
    return __ret__.apply(lambda __response__: GetLocalGatewayRouteTableResult(
        local_gateway_route_table_arn=pulumi.get(__response__, 'local_gateway_route_table_arn'),
        local_gateway_route_table_id=pulumi.get(__response__, 'local_gateway_route_table_id'),
        outpost_arn=pulumi.get(__response__, 'outpost_arn'),
        owner_id=pulumi.get(__response__, 'owner_id'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags')))
