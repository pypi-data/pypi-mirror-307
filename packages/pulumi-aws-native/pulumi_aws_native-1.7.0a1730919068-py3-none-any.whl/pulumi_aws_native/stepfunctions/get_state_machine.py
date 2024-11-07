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
    'GetStateMachineResult',
    'AwaitableGetStateMachineResult',
    'get_state_machine',
    'get_state_machine_output',
]

@pulumi.output_type
class GetStateMachineResult:
    def __init__(__self__, arn=None, definition_string=None, encryption_configuration=None, logging_configuration=None, name=None, role_arn=None, state_machine_revision_id=None, tags=None, tracing_configuration=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if definition_string and not isinstance(definition_string, str):
            raise TypeError("Expected argument 'definition_string' to be a str")
        pulumi.set(__self__, "definition_string", definition_string)
        if encryption_configuration and not isinstance(encryption_configuration, dict):
            raise TypeError("Expected argument 'encryption_configuration' to be a dict")
        pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        if logging_configuration and not isinstance(logging_configuration, dict):
            raise TypeError("Expected argument 'logging_configuration' to be a dict")
        pulumi.set(__self__, "logging_configuration", logging_configuration)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if state_machine_revision_id and not isinstance(state_machine_revision_id, str):
            raise TypeError("Expected argument 'state_machine_revision_id' to be a str")
        pulumi.set(__self__, "state_machine_revision_id", state_machine_revision_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if tracing_configuration and not isinstance(tracing_configuration, dict):
            raise TypeError("Expected argument 'tracing_configuration' to be a dict")
        pulumi.set(__self__, "tracing_configuration", tracing_configuration)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Returns the ARN of the resource.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="definitionString")
    def definition_string(self) -> Optional[str]:
        """
        The Amazon States Language definition of the state machine. The state machine definition must be in JSON. See [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) .
        """
        return pulumi.get(self, "definition_string")

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> Optional['outputs.StateMachineEncryptionConfiguration']:
        """
        Encryption configuration for the state machine.
        """
        return pulumi.get(self, "encryption_configuration")

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> Optional['outputs.StateMachineLoggingConfiguration']:
        """
        Defines what execution history events are logged and where they are logged.

        > By default, the `level` is set to `OFF` . For more information see [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        """
        return pulumi.get(self, "logging_configuration")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Returns the name of the state machine. For example:

        `{ "Fn::GetAtt": ["MyStateMachine", "Name"] }`

        Returns the name of your state machine:

        `HelloWorld-StateMachine`

        If you did not specify the name it will be similar to the following:

        `MyStateMachine-1234abcdefgh`

        For more information about using `Fn::GetAtt` , see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html) .
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="stateMachineRevisionId")
    def state_machine_revision_id(self) -> Optional[str]:
        """
        Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration.
        """
        return pulumi.get(self, "state_machine_revision_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The list of tags to add to a resource.

        Tags may only contain Unicode letters, digits, white space, or these symbols: `_ . : / = + - @` .
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tracingConfiguration")
    def tracing_configuration(self) -> Optional['outputs.StateMachineTracingConfiguration']:
        """
        Selects whether or not the state machine's AWS X-Ray tracing is enabled.
        """
        return pulumi.get(self, "tracing_configuration")


class AwaitableGetStateMachineResult(GetStateMachineResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStateMachineResult(
            arn=self.arn,
            definition_string=self.definition_string,
            encryption_configuration=self.encryption_configuration,
            logging_configuration=self.logging_configuration,
            name=self.name,
            role_arn=self.role_arn,
            state_machine_revision_id=self.state_machine_revision_id,
            tags=self.tags,
            tracing_configuration=self.tracing_configuration)


def get_state_machine(arn: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStateMachineResult:
    """
    Resource schema for StateMachine


    :param str arn: Returns the ARN of the resource.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:stepfunctions:getStateMachine', __args__, opts=opts, typ=GetStateMachineResult).value

    return AwaitableGetStateMachineResult(
        arn=pulumi.get(__ret__, 'arn'),
        definition_string=pulumi.get(__ret__, 'definition_string'),
        encryption_configuration=pulumi.get(__ret__, 'encryption_configuration'),
        logging_configuration=pulumi.get(__ret__, 'logging_configuration'),
        name=pulumi.get(__ret__, 'name'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        state_machine_revision_id=pulumi.get(__ret__, 'state_machine_revision_id'),
        tags=pulumi.get(__ret__, 'tags'),
        tracing_configuration=pulumi.get(__ret__, 'tracing_configuration'))
def get_state_machine_output(arn: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStateMachineResult]:
    """
    Resource schema for StateMachine


    :param str arn: Returns the ARN of the resource.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:stepfunctions:getStateMachine', __args__, opts=opts, typ=GetStateMachineResult)
    return __ret__.apply(lambda __response__: GetStateMachineResult(
        arn=pulumi.get(__response__, 'arn'),
        definition_string=pulumi.get(__response__, 'definition_string'),
        encryption_configuration=pulumi.get(__response__, 'encryption_configuration'),
        logging_configuration=pulumi.get(__response__, 'logging_configuration'),
        name=pulumi.get(__response__, 'name'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        state_machine_revision_id=pulumi.get(__response__, 'state_machine_revision_id'),
        tags=pulumi.get(__response__, 'tags'),
        tracing_configuration=pulumi.get(__response__, 'tracing_configuration')))
