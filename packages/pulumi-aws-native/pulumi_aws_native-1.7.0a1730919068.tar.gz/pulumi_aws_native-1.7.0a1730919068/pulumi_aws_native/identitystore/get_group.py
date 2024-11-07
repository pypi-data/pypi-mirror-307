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

__all__ = [
    'GetGroupResult',
    'AwaitableGetGroupResult',
    'get_group',
    'get_group_output',
]

@pulumi.output_type
class GetGroupResult:
    def __init__(__self__, description=None, display_name=None, group_id=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if group_id and not isinstance(group_id, str):
            raise TypeError("Expected argument 'group_id' to be a str")
        pulumi.set(__self__, "group_id", group_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A string containing the description of the group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        A string containing the name of the group. This value is commonly displayed when the group is referenced.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[str]:
        """
        The unique identifier for a group in the identity store.
        """
        return pulumi.get(self, "group_id")


class AwaitableGetGroupResult(GetGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupResult(
            description=self.description,
            display_name=self.display_name,
            group_id=self.group_id)


def get_group(group_id: Optional[str] = None,
              identity_store_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupResult:
    """
    Resource Type definition for AWS::IdentityStore::Group


    :param str group_id: The unique identifier for a group in the identity store.
    :param str identity_store_id: The globally unique identifier for the identity store.
    """
    __args__ = dict()
    __args__['groupId'] = group_id
    __args__['identityStoreId'] = identity_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:identitystore:getGroup', __args__, opts=opts, typ=GetGroupResult).value

    return AwaitableGetGroupResult(
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        group_id=pulumi.get(__ret__, 'group_id'))
def get_group_output(group_id: Optional[pulumi.Input[str]] = None,
                     identity_store_id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGroupResult]:
    """
    Resource Type definition for AWS::IdentityStore::Group


    :param str group_id: The unique identifier for a group in the identity store.
    :param str identity_store_id: The globally unique identifier for the identity store.
    """
    __args__ = dict()
    __args__['groupId'] = group_id
    __args__['identityStoreId'] = identity_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:identitystore:getGroup', __args__, opts=opts, typ=GetGroupResult)
    return __ret__.apply(lambda __response__: GetGroupResult(
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        group_id=pulumi.get(__response__, 'group_id')))
