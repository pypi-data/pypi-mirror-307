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
    'GetFolderResult',
    'AwaitableGetFolderResult',
    'get_folder',
    'get_folder_output',
]

@pulumi.output_type
class GetFolderResult:
    def __init__(__self__, arn=None, created_time=None, last_updated_time=None, name=None, permissions=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if last_updated_time and not isinstance(last_updated_time, str):
            raise TypeError("Expected argument 'last_updated_time' to be a str")
        pulumi.set(__self__, "last_updated_time", last_updated_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if permissions and not isinstance(permissions, list):
            raise TypeError("Expected argument 'permissions' to be a list")
        pulumi.set(__self__, "permissions", permissions)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        <p>The Amazon Resource Name (ARN) for the folder.</p>
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[str]:
        """
        <p>The time that the folder was created.</p>
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> Optional[str]:
        """
        <p>The time that the folder was last updated.</p>
        """
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A display name for the folder.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def permissions(self) -> Optional[Sequence['outputs.FolderResourcePermission']]:
        """
        A structure that describes the principals and the resource-level permissions of a folder.

        To specify no permissions, omit `Permissions` .
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of tags for the folders that you want to apply overrides to.
        """
        return pulumi.get(self, "tags")


class AwaitableGetFolderResult(GetFolderResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFolderResult(
            arn=self.arn,
            created_time=self.created_time,
            last_updated_time=self.last_updated_time,
            name=self.name,
            permissions=self.permissions,
            tags=self.tags)


def get_folder(aws_account_id: Optional[str] = None,
               folder_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFolderResult:
    """
    Definition of the AWS::QuickSight::Folder Resource Type.


    :param str aws_account_id: The ID for the AWS account where you want to create the folder.
    :param str folder_id: The ID of the folder.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['folderId'] = folder_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:quicksight:getFolder', __args__, opts=opts, typ=GetFolderResult).value

    return AwaitableGetFolderResult(
        arn=pulumi.get(__ret__, 'arn'),
        created_time=pulumi.get(__ret__, 'created_time'),
        last_updated_time=pulumi.get(__ret__, 'last_updated_time'),
        name=pulumi.get(__ret__, 'name'),
        permissions=pulumi.get(__ret__, 'permissions'),
        tags=pulumi.get(__ret__, 'tags'))
def get_folder_output(aws_account_id: Optional[pulumi.Input[str]] = None,
                      folder_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFolderResult]:
    """
    Definition of the AWS::QuickSight::Folder Resource Type.


    :param str aws_account_id: The ID for the AWS account where you want to create the folder.
    :param str folder_id: The ID of the folder.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['folderId'] = folder_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:quicksight:getFolder', __args__, opts=opts, typ=GetFolderResult)
    return __ret__.apply(lambda __response__: GetFolderResult(
        arn=pulumi.get(__response__, 'arn'),
        created_time=pulumi.get(__response__, 'created_time'),
        last_updated_time=pulumi.get(__response__, 'last_updated_time'),
        name=pulumi.get(__response__, 'name'),
        permissions=pulumi.get(__response__, 'permissions'),
        tags=pulumi.get(__response__, 'tags')))
