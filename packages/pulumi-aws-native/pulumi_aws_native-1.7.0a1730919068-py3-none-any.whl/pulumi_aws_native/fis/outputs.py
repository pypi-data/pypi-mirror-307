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
from ._enums import *

__all__ = [
    'ExperimentTemplateAction',
    'ExperimentTemplateExperimentOptions',
    'ExperimentTemplateLogConfiguration',
    'ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties',
    'ExperimentTemplateLogConfigurationS3ConfigurationProperties',
    'ExperimentTemplateStopCondition',
    'ExperimentTemplateTarget',
    'ExperimentTemplateTargetFilter',
]

@pulumi.output_type
class ExperimentTemplateAction(dict):
    """
    Specifies an action for the experiment template.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionId":
            suggest = "action_id"
        elif key == "startAfter":
            suggest = "start_after"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateAction. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateAction.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateAction.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action_id: str,
                 description: Optional[str] = None,
                 parameters: Optional[Mapping[str, str]] = None,
                 start_after: Optional[Sequence[str]] = None,
                 targets: Optional[Mapping[str, str]] = None):
        """
        Specifies an action for the experiment template.
        :param str action_id: The ID of the action.
        :param str description: A description for the action.
        :param Mapping[str, str] parameters: The parameters for the action, if applicable.
        :param Sequence[str] start_after: The name of the action that must be completed before the current action starts.
        :param Mapping[str, str] targets: One or more targets for the action.
        """
        pulumi.set(__self__, "action_id", action_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if start_after is not None:
            pulumi.set(__self__, "start_after", start_after)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)

    @property
    @pulumi.getter(name="actionId")
    def action_id(self) -> str:
        """
        The ID of the action.
        """
        return pulumi.get(self, "action_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the action.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, str]]:
        """
        The parameters for the action, if applicable.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="startAfter")
    def start_after(self) -> Optional[Sequence[str]]:
        """
        The name of the action that must be completed before the current action starts.
        """
        return pulumi.get(self, "start_after")

    @property
    @pulumi.getter
    def targets(self) -> Optional[Mapping[str, str]]:
        """
        One or more targets for the action.
        """
        return pulumi.get(self, "targets")


@pulumi.output_type
class ExperimentTemplateExperimentOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountTargeting":
            suggest = "account_targeting"
        elif key == "emptyTargetResolutionMode":
            suggest = "empty_target_resolution_mode"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateExperimentOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateExperimentOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateExperimentOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 account_targeting: Optional['ExperimentTemplateExperimentOptionsAccountTargeting'] = None,
                 empty_target_resolution_mode: Optional['ExperimentTemplateExperimentOptionsEmptyTargetResolutionMode'] = None):
        """
        :param 'ExperimentTemplateExperimentOptionsAccountTargeting' account_targeting: The account targeting setting for the experiment template.
        :param 'ExperimentTemplateExperimentOptionsEmptyTargetResolutionMode' empty_target_resolution_mode: The target resolution failure mode for the experiment template.
        """
        if account_targeting is not None:
            pulumi.set(__self__, "account_targeting", account_targeting)
        if empty_target_resolution_mode is not None:
            pulumi.set(__self__, "empty_target_resolution_mode", empty_target_resolution_mode)

    @property
    @pulumi.getter(name="accountTargeting")
    def account_targeting(self) -> Optional['ExperimentTemplateExperimentOptionsAccountTargeting']:
        """
        The account targeting setting for the experiment template.
        """
        return pulumi.get(self, "account_targeting")

    @property
    @pulumi.getter(name="emptyTargetResolutionMode")
    def empty_target_resolution_mode(self) -> Optional['ExperimentTemplateExperimentOptionsEmptyTargetResolutionMode']:
        """
        The target resolution failure mode for the experiment template.
        """
        return pulumi.get(self, "empty_target_resolution_mode")


@pulumi.output_type
class ExperimentTemplateLogConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logSchemaVersion":
            suggest = "log_schema_version"
        elif key == "cloudWatchLogsConfiguration":
            suggest = "cloud_watch_logs_configuration"
        elif key == "s3Configuration":
            suggest = "s3_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateLogConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateLogConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateLogConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_schema_version: int,
                 cloud_watch_logs_configuration: Optional['outputs.ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties'] = None,
                 s3_configuration: Optional['outputs.ExperimentTemplateLogConfigurationS3ConfigurationProperties'] = None):
        """
        :param int log_schema_version: The schema version.
        :param 'ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties' cloud_watch_logs_configuration: The configuration for experiment logging to CloudWatch Logs .
        :param 'ExperimentTemplateLogConfigurationS3ConfigurationProperties' s3_configuration: The configuration for experiment logging to Amazon S3 .
        """
        pulumi.set(__self__, "log_schema_version", log_schema_version)
        if cloud_watch_logs_configuration is not None:
            pulumi.set(__self__, "cloud_watch_logs_configuration", cloud_watch_logs_configuration)
        if s3_configuration is not None:
            pulumi.set(__self__, "s3_configuration", s3_configuration)

    @property
    @pulumi.getter(name="logSchemaVersion")
    def log_schema_version(self) -> int:
        """
        The schema version.
        """
        return pulumi.get(self, "log_schema_version")

    @property
    @pulumi.getter(name="cloudWatchLogsConfiguration")
    def cloud_watch_logs_configuration(self) -> Optional['outputs.ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties']:
        """
        The configuration for experiment logging to CloudWatch Logs .
        """
        return pulumi.get(self, "cloud_watch_logs_configuration")

    @property
    @pulumi.getter(name="s3Configuration")
    def s3_configuration(self) -> Optional['outputs.ExperimentTemplateLogConfigurationS3ConfigurationProperties']:
        """
        The configuration for experiment logging to Amazon S3 .
        """
        return pulumi.get(self, "s3_configuration")


@pulumi.output_type
class ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties(dict):
    """
    The configuration for experiment logging to CloudWatch Logs .
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroupArn":
            suggest = "log_group_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateLogConfigurationCloudWatchLogsConfigurationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group_arn: str):
        """
        The configuration for experiment logging to CloudWatch Logs .
        """
        pulumi.set(__self__, "log_group_arn", log_group_arn)

    @property
    @pulumi.getter(name="logGroupArn")
    def log_group_arn(self) -> str:
        return pulumi.get(self, "log_group_arn")


@pulumi.output_type
class ExperimentTemplateLogConfigurationS3ConfigurationProperties(dict):
    """
    The configuration for experiment logging to Amazon S3 .
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateLogConfigurationS3ConfigurationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateLogConfigurationS3ConfigurationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateLogConfigurationS3ConfigurationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: str,
                 prefix: Optional[str] = None):
        """
        The configuration for experiment logging to Amazon S3 .
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        return pulumi.get(self, "prefix")


@pulumi.output_type
class ExperimentTemplateStopCondition(dict):
    def __init__(__self__, *,
                 source: str,
                 value: Optional[str] = None):
        pulumi.set(__self__, "source", source)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def source(self) -> str:
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        return pulumi.get(self, "value")


@pulumi.output_type
class ExperimentTemplateTarget(dict):
    """
    Specifies a target for an experiment.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceType":
            suggest = "resource_type"
        elif key == "selectionMode":
            suggest = "selection_mode"
        elif key == "resourceArns":
            suggest = "resource_arns"
        elif key == "resourceTags":
            suggest = "resource_tags"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExperimentTemplateTarget. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExperimentTemplateTarget.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExperimentTemplateTarget.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 resource_type: str,
                 selection_mode: str,
                 filters: Optional[Sequence['outputs.ExperimentTemplateTargetFilter']] = None,
                 parameters: Optional[Mapping[str, str]] = None,
                 resource_arns: Optional[Sequence[str]] = None,
                 resource_tags: Optional[Mapping[str, str]] = None):
        """
        Specifies a target for an experiment.
        :param str resource_type: The resource type.
        :param str selection_mode: Scopes the identified resources to a specific count or percentage.
        :param Sequence['ExperimentTemplateTargetFilter'] filters: The filters to apply to identify target resources using specific attributes.
        :param Mapping[str, str] parameters: The parameters for the resource type.
        :param Sequence[str] resource_arns: The Amazon Resource Names (ARNs) of the targets.
        :param Mapping[str, str] resource_tags: The tags for the target resources.
        """
        pulumi.set(__self__, "resource_type", resource_type)
        pulumi.set(__self__, "selection_mode", selection_mode)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if resource_arns is not None:
            pulumi.set(__self__, "resource_arns", resource_arns)
        if resource_tags is not None:
            pulumi.set(__self__, "resource_tags", resource_tags)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="selectionMode")
    def selection_mode(self) -> str:
        """
        Scopes the identified resources to a specific count or percentage.
        """
        return pulumi.get(self, "selection_mode")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.ExperimentTemplateTargetFilter']]:
        """
        The filters to apply to identify target resources using specific attributes.
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, str]]:
        """
        The parameters for the resource type.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="resourceArns")
    def resource_arns(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the targets.
        """
        return pulumi.get(self, "resource_arns")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags for the target resources.
        """
        return pulumi.get(self, "resource_tags")


@pulumi.output_type
class ExperimentTemplateTargetFilter(dict):
    """
    Describes a filter used for the target resource input in an experiment template.
    """
    def __init__(__self__, *,
                 path: str,
                 values: Sequence[str]):
        """
        Describes a filter used for the target resource input in an experiment template.
        """
        pulumi.set(__self__, "path", path)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def path(self) -> str:
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        return pulumi.get(self, "values")


