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
    'GetStorageLensGroupResult',
    'AwaitableGetStorageLensGroupResult',
    'get_storage_lens_group',
    'get_storage_lens_group_output',
]

@pulumi.output_type
class GetStorageLensGroupResult:
    def __init__(__self__, filter=None, storage_lens_group_arn=None, tags=None):
        if filter and not isinstance(filter, dict):
            raise TypeError("Expected argument 'filter' to be a dict")
        pulumi.set(__self__, "filter", filter)
        if storage_lens_group_arn and not isinstance(storage_lens_group_arn, str):
            raise TypeError("Expected argument 'storage_lens_group_arn' to be a str")
        pulumi.set(__self__, "storage_lens_group_arn", storage_lens_group_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filter(self) -> Optional['outputs.StorageLensGroupFilter']:
        """
        This property contains the criteria for the Storage Lens group data that is displayed
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter(name="storageLensGroupArn")
    def storage_lens_group_arn(self) -> Optional[str]:
        """
        The ARN for the Amazon S3 Storage Lens Group.
        """
        return pulumi.get(self, "storage_lens_group_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A set of tags (key-value pairs) for this Amazon S3 Storage Lens Group.
        """
        return pulumi.get(self, "tags")


class AwaitableGetStorageLensGroupResult(GetStorageLensGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageLensGroupResult(
            filter=self.filter,
            storage_lens_group_arn=self.storage_lens_group_arn,
            tags=self.tags)


def get_storage_lens_group(name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStorageLensGroupResult:
    """
    The AWS::S3::StorageLensGroup resource is an Amazon S3 resource type that you can use to create Storage Lens Group.


    :param str name: This property contains the Storage Lens group name.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:s3:getStorageLensGroup', __args__, opts=opts, typ=GetStorageLensGroupResult).value

    return AwaitableGetStorageLensGroupResult(
        filter=pulumi.get(__ret__, 'filter'),
        storage_lens_group_arn=pulumi.get(__ret__, 'storage_lens_group_arn'),
        tags=pulumi.get(__ret__, 'tags'))
def get_storage_lens_group_output(name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStorageLensGroupResult]:
    """
    The AWS::S3::StorageLensGroup resource is an Amazon S3 resource type that you can use to create Storage Lens Group.


    :param str name: This property contains the Storage Lens group name.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:s3:getStorageLensGroup', __args__, opts=opts, typ=GetStorageLensGroupResult)
    return __ret__.apply(lambda __response__: GetStorageLensGroupResult(
        filter=pulumi.get(__response__, 'filter'),
        storage_lens_group_arn=pulumi.get(__response__, 'storage_lens_group_arn'),
        tags=pulumi.get(__response__, 'tags')))
