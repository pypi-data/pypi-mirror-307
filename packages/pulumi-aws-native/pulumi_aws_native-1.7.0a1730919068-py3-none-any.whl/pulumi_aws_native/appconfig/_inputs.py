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
    'ConfigurationProfileValidatorsArgs',
    'ConfigurationProfileValidatorsArgsDict',
    'EnvironmentMonitorArgs',
    'EnvironmentMonitorArgsDict',
    'ExtensionActionArgs',
    'ExtensionActionArgsDict',
    'ExtensionParameterArgs',
    'ExtensionParameterArgsDict',
]

MYPY = False

if not MYPY:
    class ConfigurationProfileValidatorsArgsDict(TypedDict):
        """
        A list of methods for validating the configuration.
        """
        content: NotRequired[pulumi.Input[str]]
        """
        Either the JSON Schema content or the Amazon Resource Name (ARN) of an Lambda function.
        """
        type: NotRequired[pulumi.Input[str]]
        """
        AWS AppConfig supports validators of type JSON_SCHEMA and LAMBDA.
        """
elif False:
    ConfigurationProfileValidatorsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ConfigurationProfileValidatorsArgs:
    def __init__(__self__, *,
                 content: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        A list of methods for validating the configuration.
        :param pulumi.Input[str] content: Either the JSON Schema content or the Amazon Resource Name (ARN) of an Lambda function.
        :param pulumi.Input[str] type: AWS AppConfig supports validators of type JSON_SCHEMA and LAMBDA.
        """
        if content is not None:
            pulumi.set(__self__, "content", content)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        """
        Either the JSON Schema content or the Amazon Resource Name (ARN) of an Lambda function.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        AWS AppConfig supports validators of type JSON_SCHEMA and LAMBDA.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


if not MYPY:
    class EnvironmentMonitorArgsDict(TypedDict):
        """
        Amazon CloudWatch alarm to monitor during the deployment process.
        """
        alarm_arn: pulumi.Input[str]
        """
        Amazon Resource Name (ARN) of the Amazon CloudWatch alarm.
        """
        alarm_role_arn: NotRequired[pulumi.Input[str]]
        """
        ARN of an AWS Identity and Access Management (IAM) role for AWS AppConfig to monitor AlarmArn.
        """
elif False:
    EnvironmentMonitorArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class EnvironmentMonitorArgs:
    def __init__(__self__, *,
                 alarm_arn: pulumi.Input[str],
                 alarm_role_arn: Optional[pulumi.Input[str]] = None):
        """
        Amazon CloudWatch alarm to monitor during the deployment process.
        :param pulumi.Input[str] alarm_arn: Amazon Resource Name (ARN) of the Amazon CloudWatch alarm.
        :param pulumi.Input[str] alarm_role_arn: ARN of an AWS Identity and Access Management (IAM) role for AWS AppConfig to monitor AlarmArn.
        """
        pulumi.set(__self__, "alarm_arn", alarm_arn)
        if alarm_role_arn is not None:
            pulumi.set(__self__, "alarm_role_arn", alarm_role_arn)

    @property
    @pulumi.getter(name="alarmArn")
    def alarm_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the Amazon CloudWatch alarm.
        """
        return pulumi.get(self, "alarm_arn")

    @alarm_arn.setter
    def alarm_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "alarm_arn", value)

    @property
    @pulumi.getter(name="alarmRoleArn")
    def alarm_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of an AWS Identity and Access Management (IAM) role for AWS AppConfig to monitor AlarmArn.
        """
        return pulumi.get(self, "alarm_role_arn")

    @alarm_role_arn.setter
    def alarm_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alarm_role_arn", value)


if not MYPY:
    class ExtensionActionArgsDict(TypedDict):
        """
        An action for an extension to take at a specific action point.
        """
        name: pulumi.Input[str]
        """
        The name of the extension action.
        """
        uri: pulumi.Input[str]
        """
        The URI of the extension action.
        """
        description: NotRequired[pulumi.Input[str]]
        """
        The description of the extension Action.
        """
        role_arn: NotRequired[pulumi.Input[str]]
        """
        The ARN of the role for invoking the extension action.
        """
elif False:
    ExtensionActionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ExtensionActionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 uri: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None):
        """
        An action for an extension to take at a specific action point.
        :param pulumi.Input[str] name: The name of the extension action.
        :param pulumi.Input[str] uri: The URI of the extension action.
        :param pulumi.Input[str] description: The description of the extension Action.
        :param pulumi.Input[str] role_arn: The ARN of the role for invoking the extension action.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "uri", uri)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the extension action.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Input[str]:
        """
        The URI of the extension action.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the extension Action.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the role for invoking the extension action.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)


if not MYPY:
    class ExtensionParameterArgsDict(TypedDict):
        """
        A parameter for the extension to send to a specific action.
        """
        required: pulumi.Input[bool]
        description: NotRequired[pulumi.Input[str]]
        """
        The description of the extension Parameter.
        """
        dynamic: NotRequired[pulumi.Input[bool]]
elif False:
    ExtensionParameterArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ExtensionParameterArgs:
    def __init__(__self__, *,
                 required: pulumi.Input[bool],
                 description: Optional[pulumi.Input[str]] = None,
                 dynamic: Optional[pulumi.Input[bool]] = None):
        """
        A parameter for the extension to send to a specific action.
        :param pulumi.Input[str] description: The description of the extension Parameter.
        """
        pulumi.set(__self__, "required", required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dynamic is not None:
            pulumi.set(__self__, "dynamic", dynamic)

    @property
    @pulumi.getter
    def required(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "required")

    @required.setter
    def required(self, value: pulumi.Input[bool]):
        pulumi.set(self, "required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the extension Parameter.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def dynamic(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "dynamic")

    @dynamic.setter
    def dynamic(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dynamic", value)


