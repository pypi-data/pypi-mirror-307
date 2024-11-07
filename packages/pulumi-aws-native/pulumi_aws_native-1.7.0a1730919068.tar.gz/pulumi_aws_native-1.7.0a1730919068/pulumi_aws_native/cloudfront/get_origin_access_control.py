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

__all__ = [
    'GetOriginAccessControlResult',
    'AwaitableGetOriginAccessControlResult',
    'get_origin_access_control',
    'get_origin_access_control_output',
]

@pulumi.output_type
class GetOriginAccessControlResult:
    def __init__(__self__, id=None, origin_access_control_config=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if origin_access_control_config and not isinstance(origin_access_control_config, dict):
            raise TypeError("Expected argument 'origin_access_control_config' to be a dict")
        pulumi.set(__self__, "origin_access_control_config", origin_access_control_config)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique identifier of the origin access control.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="originAccessControlConfig")
    def origin_access_control_config(self) -> Optional['outputs.OriginAccessControlConfig']:
        """
        The origin access control.
        """
        return pulumi.get(self, "origin_access_control_config")


class AwaitableGetOriginAccessControlResult(GetOriginAccessControlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOriginAccessControlResult(
            id=self.id,
            origin_access_control_config=self.origin_access_control_config)


def get_origin_access_control(id: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOriginAccessControlResult:
    """
    Resource Type definition for AWS::CloudFront::OriginAccessControl


    :param str id: The unique identifier of the origin access control.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudfront:getOriginAccessControl', __args__, opts=opts, typ=GetOriginAccessControlResult).value

    return AwaitableGetOriginAccessControlResult(
        id=pulumi.get(__ret__, 'id'),
        origin_access_control_config=pulumi.get(__ret__, 'origin_access_control_config'))
def get_origin_access_control_output(id: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOriginAccessControlResult]:
    """
    Resource Type definition for AWS::CloudFront::OriginAccessControl


    :param str id: The unique identifier of the origin access control.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudfront:getOriginAccessControl', __args__, opts=opts, typ=GetOriginAccessControlResult)
    return __ret__.apply(lambda __response__: GetOriginAccessControlResult(
        id=pulumi.get(__response__, 'id'),
        origin_access_control_config=pulumi.get(__response__, 'origin_access_control_config')))
