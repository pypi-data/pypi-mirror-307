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
    'GetCloudWatchAlarmTemplateGroupResult',
    'AwaitableGetCloudWatchAlarmTemplateGroupResult',
    'get_cloud_watch_alarm_template_group',
    'get_cloud_watch_alarm_template_group_output',
]

@pulumi.output_type
class GetCloudWatchAlarmTemplateGroupResult:
    def __init__(__self__, arn=None, created_at=None, description=None, id=None, identifier=None, modified_at=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if modified_at and not isinstance(modified_at, str):
            raise TypeError("Expected argument 'modified_at' to be a str")
        pulumi.set(__self__, "modified_at", modified_at)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        A cloudwatch alarm template group's ARN (Amazon Resource Name)
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date and time of resource creation.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A resource's optional description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        A cloudwatch alarm template group's id. AWS provided template groups have ids that start with `aws-`
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifier(self) -> Optional[str]:
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> Optional[str]:
        """
        The date and time of latest resource modification.
        """
        return pulumi.get(self, "modified_at")


class AwaitableGetCloudWatchAlarmTemplateGroupResult(GetCloudWatchAlarmTemplateGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudWatchAlarmTemplateGroupResult(
            arn=self.arn,
            created_at=self.created_at,
            description=self.description,
            id=self.id,
            identifier=self.identifier,
            modified_at=self.modified_at)


def get_cloud_watch_alarm_template_group(identifier: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudWatchAlarmTemplateGroupResult:
    """
    Definition of AWS::MediaLive::CloudWatchAlarmTemplateGroup Resource Type
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:medialive:getCloudWatchAlarmTemplateGroup', __args__, opts=opts, typ=GetCloudWatchAlarmTemplateGroupResult).value

    return AwaitableGetCloudWatchAlarmTemplateGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        identifier=pulumi.get(__ret__, 'identifier'),
        modified_at=pulumi.get(__ret__, 'modified_at'))
def get_cloud_watch_alarm_template_group_output(identifier: Optional[pulumi.Input[str]] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudWatchAlarmTemplateGroupResult]:
    """
    Definition of AWS::MediaLive::CloudWatchAlarmTemplateGroup Resource Type
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:medialive:getCloudWatchAlarmTemplateGroup', __args__, opts=opts, typ=GetCloudWatchAlarmTemplateGroupResult)
    return __ret__.apply(lambda __response__: GetCloudWatchAlarmTemplateGroupResult(
        arn=pulumi.get(__response__, 'arn'),
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        identifier=pulumi.get(__response__, 'identifier'),
        modified_at=pulumi.get(__response__, 'modified_at')))
