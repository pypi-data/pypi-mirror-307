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
from ._enums import *

__all__ = [
    'GetServiceNetworkResult',
    'AwaitableGetServiceNetworkResult',
    'get_service_network',
    'get_service_network_output',
]

@pulumi.output_type
class GetServiceNetworkResult:
    def __init__(__self__, arn=None, auth_type=None, created_at=None, id=None, last_updated_at=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auth_type and not isinstance(auth_type, str):
            raise TypeError("Expected argument 'auth_type' to be a str")
        pulumi.set(__self__, "auth_type", auth_type)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_updated_at and not isinstance(last_updated_at, str):
            raise TypeError("Expected argument 'last_updated_at' to be a str")
        pulumi.set(__self__, "last_updated_at", last_updated_at)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the service network.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> Optional['ServiceNetworkAuthType']:
        """
        The type of IAM policy.

        - `NONE` : The resource does not use an IAM policy. This is the default.
        - `AWS_IAM` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.
        """
        return pulumi.get(self, "auth_type")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date and time that the service network was created, specified in ISO-8601 format.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the service network.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUpdatedAt")
    def last_updated_at(self) -> Optional[str]:
        """
        The date and time of the last update, specified in ISO-8601 format.
        """
        return pulumi.get(self, "last_updated_at")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the service network.
        """
        return pulumi.get(self, "tags")


class AwaitableGetServiceNetworkResult(GetServiceNetworkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceNetworkResult(
            arn=self.arn,
            auth_type=self.auth_type,
            created_at=self.created_at,
            id=self.id,
            last_updated_at=self.last_updated_at,
            tags=self.tags)


def get_service_network(arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceNetworkResult:
    """
    A service network is a logical boundary for a collection of services. You can associate services and VPCs with a service network.


    :param str arn: The Amazon Resource Name (ARN) of the service network.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:vpclattice:getServiceNetwork', __args__, opts=opts, typ=GetServiceNetworkResult).value

    return AwaitableGetServiceNetworkResult(
        arn=pulumi.get(__ret__, 'arn'),
        auth_type=pulumi.get(__ret__, 'auth_type'),
        created_at=pulumi.get(__ret__, 'created_at'),
        id=pulumi.get(__ret__, 'id'),
        last_updated_at=pulumi.get(__ret__, 'last_updated_at'),
        tags=pulumi.get(__ret__, 'tags'))
def get_service_network_output(arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceNetworkResult]:
    """
    A service network is a logical boundary for a collection of services. You can associate services and VPCs with a service network.


    :param str arn: The Amazon Resource Name (ARN) of the service network.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:vpclattice:getServiceNetwork', __args__, opts=opts, typ=GetServiceNetworkResult)
    return __ret__.apply(lambda __response__: GetServiceNetworkResult(
        arn=pulumi.get(__response__, 'arn'),
        auth_type=pulumi.get(__response__, 'auth_type'),
        created_at=pulumi.get(__response__, 'created_at'),
        id=pulumi.get(__response__, 'id'),
        last_updated_at=pulumi.get(__response__, 'last_updated_at'),
        tags=pulumi.get(__response__, 'tags')))
