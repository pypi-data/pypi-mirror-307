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
from ._enums import *

__all__ = [
    'GetResolverConfigResult',
    'AwaitableGetResolverConfigResult',
    'get_resolver_config',
    'get_resolver_config_output',
]

@pulumi.output_type
class GetResolverConfigResult:
    def __init__(__self__, autodefined_reverse=None, id=None, owner_id=None):
        if autodefined_reverse and not isinstance(autodefined_reverse, str):
            raise TypeError("Expected argument 'autodefined_reverse' to be a str")
        pulumi.set(__self__, "autodefined_reverse", autodefined_reverse)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)

    @property
    @pulumi.getter(name="autodefinedReverse")
    def autodefined_reverse(self) -> Optional['ResolverConfigAutodefinedReverse']:
        """
        ResolverAutodefinedReverseStatus, possible values are ENABLING, ENABLED, DISABLING AND DISABLED.
        """
        return pulumi.get(self, "autodefined_reverse")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[str]:
        """
        AccountId
        """
        return pulumi.get(self, "owner_id")


class AwaitableGetResolverConfigResult(GetResolverConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResolverConfigResult(
            autodefined_reverse=self.autodefined_reverse,
            id=self.id,
            owner_id=self.owner_id)


def get_resolver_config(resource_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResolverConfigResult:
    """
    Resource schema for AWS::Route53Resolver::ResolverConfig.


    :param str resource_id: ResourceId
    """
    __args__ = dict()
    __args__['resourceId'] = resource_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:route53resolver:getResolverConfig', __args__, opts=opts, typ=GetResolverConfigResult).value

    return AwaitableGetResolverConfigResult(
        autodefined_reverse=pulumi.get(__ret__, 'autodefined_reverse'),
        id=pulumi.get(__ret__, 'id'),
        owner_id=pulumi.get(__ret__, 'owner_id'))
def get_resolver_config_output(resource_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResolverConfigResult]:
    """
    Resource schema for AWS::Route53Resolver::ResolverConfig.


    :param str resource_id: ResourceId
    """
    __args__ = dict()
    __args__['resourceId'] = resource_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:route53resolver:getResolverConfig', __args__, opts=opts, typ=GetResolverConfigResult)
    return __ret__.apply(lambda __response__: GetResolverConfigResult(
        autodefined_reverse=pulumi.get(__response__, 'autodefined_reverse'),
        id=pulumi.get(__response__, 'id'),
        owner_id=pulumi.get(__response__, 'owner_id')))
