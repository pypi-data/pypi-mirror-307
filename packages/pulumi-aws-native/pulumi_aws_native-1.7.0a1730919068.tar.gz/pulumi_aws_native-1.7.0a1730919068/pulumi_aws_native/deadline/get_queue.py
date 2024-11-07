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
from ._enums import *

__all__ = [
    'GetQueueResult',
    'AwaitableGetQueueResult',
    'get_queue',
    'get_queue_output',
]

@pulumi.output_type
class GetQueueResult:
    def __init__(__self__, allowed_storage_profile_ids=None, arn=None, default_budget_action=None, description=None, display_name=None, job_attachment_settings=None, job_run_as_user=None, queue_id=None, required_file_system_location_names=None, role_arn=None, tags=None):
        if allowed_storage_profile_ids and not isinstance(allowed_storage_profile_ids, list):
            raise TypeError("Expected argument 'allowed_storage_profile_ids' to be a list")
        pulumi.set(__self__, "allowed_storage_profile_ids", allowed_storage_profile_ids)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if default_budget_action and not isinstance(default_budget_action, str):
            raise TypeError("Expected argument 'default_budget_action' to be a str")
        pulumi.set(__self__, "default_budget_action", default_budget_action)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if job_attachment_settings and not isinstance(job_attachment_settings, dict):
            raise TypeError("Expected argument 'job_attachment_settings' to be a dict")
        pulumi.set(__self__, "job_attachment_settings", job_attachment_settings)
        if job_run_as_user and not isinstance(job_run_as_user, dict):
            raise TypeError("Expected argument 'job_run_as_user' to be a dict")
        pulumi.set(__self__, "job_run_as_user", job_run_as_user)
        if queue_id and not isinstance(queue_id, str):
            raise TypeError("Expected argument 'queue_id' to be a str")
        pulumi.set(__self__, "queue_id", queue_id)
        if required_file_system_location_names and not isinstance(required_file_system_location_names, list):
            raise TypeError("Expected argument 'required_file_system_location_names' to be a list")
        pulumi.set(__self__, "required_file_system_location_names", required_file_system_location_names)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowedStorageProfileIds")
    def allowed_storage_profile_ids(self) -> Optional[Sequence[str]]:
        """
        The identifiers of the storage profiles that this queue can use to share assets between workers using different operating systems.
        """
        return pulumi.get(self, "allowed_storage_profile_ids")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the queue.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultBudgetAction")
    def default_budget_action(self) -> Optional['QueueDefaultQueueBudgetAction']:
        """
        The default action taken on a queue summary if a budget wasn't configured.
        """
        return pulumi.get(self, "default_budget_action")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the queue that helps identify what the queue is used for.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the queue summary to update.

        > This field can store any content. Escape or encode this content before displaying it on a webpage or any other system that might interpret the content of this field.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="jobAttachmentSettings")
    def job_attachment_settings(self) -> Optional['outputs.QueueJobAttachmentSettings']:
        """
        The job attachment settings. These are the Amazon S3 bucket name and the Amazon S3 prefix.
        """
        return pulumi.get(self, "job_attachment_settings")

    @property
    @pulumi.getter(name="jobRunAsUser")
    def job_run_as_user(self) -> Optional['outputs.QueueJobRunAsUser']:
        """
        Identifies the user for a job.
        """
        return pulumi.get(self, "job_run_as_user")

    @property
    @pulumi.getter(name="queueId")
    def queue_id(self) -> Optional[str]:
        """
        The queue ID.
        """
        return pulumi.get(self, "queue_id")

    @property
    @pulumi.getter(name="requiredFileSystemLocationNames")
    def required_file_system_location_names(self) -> Optional[Sequence[str]]:
        """
        The file system location that the queue uses.
        """
        return pulumi.get(self, "required_file_system_location_names")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role that workers use when running jobs in this queue.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetQueueResult(GetQueueResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetQueueResult(
            allowed_storage_profile_ids=self.allowed_storage_profile_ids,
            arn=self.arn,
            default_budget_action=self.default_budget_action,
            description=self.description,
            display_name=self.display_name,
            job_attachment_settings=self.job_attachment_settings,
            job_run_as_user=self.job_run_as_user,
            queue_id=self.queue_id,
            required_file_system_location_names=self.required_file_system_location_names,
            role_arn=self.role_arn,
            tags=self.tags)


def get_queue(arn: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetQueueResult:
    """
    Definition of AWS::Deadline::Queue Resource Type


    :param str arn: The Amazon Resource Name (ARN) of the queue.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:deadline:getQueue', __args__, opts=opts, typ=GetQueueResult).value

    return AwaitableGetQueueResult(
        allowed_storage_profile_ids=pulumi.get(__ret__, 'allowed_storage_profile_ids'),
        arn=pulumi.get(__ret__, 'arn'),
        default_budget_action=pulumi.get(__ret__, 'default_budget_action'),
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        job_attachment_settings=pulumi.get(__ret__, 'job_attachment_settings'),
        job_run_as_user=pulumi.get(__ret__, 'job_run_as_user'),
        queue_id=pulumi.get(__ret__, 'queue_id'),
        required_file_system_location_names=pulumi.get(__ret__, 'required_file_system_location_names'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        tags=pulumi.get(__ret__, 'tags'))
def get_queue_output(arn: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetQueueResult]:
    """
    Definition of AWS::Deadline::Queue Resource Type


    :param str arn: The Amazon Resource Name (ARN) of the queue.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:deadline:getQueue', __args__, opts=opts, typ=GetQueueResult)
    return __ret__.apply(lambda __response__: GetQueueResult(
        allowed_storage_profile_ids=pulumi.get(__response__, 'allowed_storage_profile_ids'),
        arn=pulumi.get(__response__, 'arn'),
        default_budget_action=pulumi.get(__response__, 'default_budget_action'),
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        job_attachment_settings=pulumi.get(__response__, 'job_attachment_settings'),
        job_run_as_user=pulumi.get(__response__, 'job_run_as_user'),
        queue_id=pulumi.get(__response__, 'queue_id'),
        required_file_system_location_names=pulumi.get(__response__, 'required_file_system_location_names'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        tags=pulumi.get(__response__, 'tags')))
