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
    'GetHookVersionResult',
    'AwaitableGetHookVersionResult',
    'get_hook_version',
    'get_hook_version_output',
]

@pulumi.output_type
class GetHookVersionResult:
    def __init__(__self__, arn=None, is_default_version=None, type_arn=None, version_id=None, visibility=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if is_default_version and not isinstance(is_default_version, bool):
            raise TypeError("Expected argument 'is_default_version' to be a bool")
        pulumi.set(__self__, "is_default_version", is_default_version)
        if type_arn and not isinstance(type_arn, str):
            raise TypeError("Expected argument 'type_arn' to be a str")
        pulumi.set(__self__, "type_arn", type_arn)
        if version_id and not isinstance(version_id, str):
            raise TypeError("Expected argument 'version_id' to be a str")
        pulumi.set(__self__, "version_id", version_id)
        if visibility and not isinstance(visibility, str):
            raise TypeError("Expected argument 'visibility' to be a str")
        pulumi.set(__self__, "visibility", visibility)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the type, here the HookVersion. This is used to uniquely identify a HookVersion resource
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="isDefaultVersion")
    def is_default_version(self) -> Optional[bool]:
        """
        Indicates if this type version is the current default version
        """
        return pulumi.get(self, "is_default_version")

    @property
    @pulumi.getter(name="typeArn")
    def type_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the type without the versionID.
        """
        return pulumi.get(self, "type_arn")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[str]:
        """
        The ID of the version of the type represented by this hook instance.
        """
        return pulumi.get(self, "version_id")

    @property
    @pulumi.getter
    def visibility(self) -> Optional['HookVersionVisibility']:
        """
        The scope at which the type is visible and usable in CloudFormation operations.

        Valid values include:

        PRIVATE: The type is only visible and usable within the account in which it is registered. Currently, AWS CloudFormation marks any types you register as PRIVATE.

        PUBLIC: The type is publically visible and usable within any Amazon account.
        """
        return pulumi.get(self, "visibility")


class AwaitableGetHookVersionResult(GetHookVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHookVersionResult(
            arn=self.arn,
            is_default_version=self.is_default_version,
            type_arn=self.type_arn,
            version_id=self.version_id,
            visibility=self.visibility)


def get_hook_version(arn: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHookVersionResult:
    """
    Publishes new or first hook version to AWS CloudFormation Registry.


    :param str arn: The Amazon Resource Name (ARN) of the type, here the HookVersion. This is used to uniquely identify a HookVersion resource
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudformation:getHookVersion', __args__, opts=opts, typ=GetHookVersionResult).value

    return AwaitableGetHookVersionResult(
        arn=pulumi.get(__ret__, 'arn'),
        is_default_version=pulumi.get(__ret__, 'is_default_version'),
        type_arn=pulumi.get(__ret__, 'type_arn'),
        version_id=pulumi.get(__ret__, 'version_id'),
        visibility=pulumi.get(__ret__, 'visibility'))
def get_hook_version_output(arn: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHookVersionResult]:
    """
    Publishes new or first hook version to AWS CloudFormation Registry.


    :param str arn: The Amazon Resource Name (ARN) of the type, here the HookVersion. This is used to uniquely identify a HookVersion resource
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudformation:getHookVersion', __args__, opts=opts, typ=GetHookVersionResult)
    return __ret__.apply(lambda __response__: GetHookVersionResult(
        arn=pulumi.get(__response__, 'arn'),
        is_default_version=pulumi.get(__response__, 'is_default_version'),
        type_arn=pulumi.get(__response__, 'type_arn'),
        version_id=pulumi.get(__response__, 'version_id'),
        visibility=pulumi.get(__response__, 'visibility')))
