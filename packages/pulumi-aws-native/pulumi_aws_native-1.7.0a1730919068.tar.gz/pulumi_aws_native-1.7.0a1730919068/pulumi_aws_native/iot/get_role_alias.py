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
    'GetRoleAliasResult',
    'AwaitableGetRoleAliasResult',
    'get_role_alias',
    'get_role_alias_output',
]

@pulumi.output_type
class GetRoleAliasResult:
    def __init__(__self__, credential_duration_seconds=None, role_alias_arn=None, role_arn=None, tags=None):
        if credential_duration_seconds and not isinstance(credential_duration_seconds, int):
            raise TypeError("Expected argument 'credential_duration_seconds' to be a int")
        pulumi.set(__self__, "credential_duration_seconds", credential_duration_seconds)
        if role_alias_arn and not isinstance(role_alias_arn, str):
            raise TypeError("Expected argument 'role_alias_arn' to be a str")
        pulumi.set(__self__, "role_alias_arn", role_alias_arn)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="credentialDurationSeconds")
    def credential_duration_seconds(self) -> Optional[int]:
        """
        The number of seconds for which the credential is valid.
        """
        return pulumi.get(self, "credential_duration_seconds")

    @property
    @pulumi.getter(name="roleAliasArn")
    def role_alias_arn(self) -> Optional[str]:
        """
        The role alias ARN.
        """
        return pulumi.get(self, "role_alias_arn")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The role ARN.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")


class AwaitableGetRoleAliasResult(GetRoleAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoleAliasResult(
            credential_duration_seconds=self.credential_duration_seconds,
            role_alias_arn=self.role_alias_arn,
            role_arn=self.role_arn,
            tags=self.tags)


def get_role_alias(role_alias: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoleAliasResult:
    """
    Use the AWS::IoT::RoleAlias resource to declare an AWS IoT RoleAlias.


    :param str role_alias: The role alias.
    """
    __args__ = dict()
    __args__['roleAlias'] = role_alias
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iot:getRoleAlias', __args__, opts=opts, typ=GetRoleAliasResult).value

    return AwaitableGetRoleAliasResult(
        credential_duration_seconds=pulumi.get(__ret__, 'credential_duration_seconds'),
        role_alias_arn=pulumi.get(__ret__, 'role_alias_arn'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        tags=pulumi.get(__ret__, 'tags'))
def get_role_alias_output(role_alias: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoleAliasResult]:
    """
    Use the AWS::IoT::RoleAlias resource to declare an AWS IoT RoleAlias.


    :param str role_alias: The role alias.
    """
    __args__ = dict()
    __args__['roleAlias'] = role_alias
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iot:getRoleAlias', __args__, opts=opts, typ=GetRoleAliasResult)
    return __ret__.apply(lambda __response__: GetRoleAliasResult(
        credential_duration_seconds=pulumi.get(__response__, 'credential_duration_seconds'),
        role_alias_arn=pulumi.get(__response__, 'role_alias_arn'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        tags=pulumi.get(__response__, 'tags')))
