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

__all__ = ['StateMachineVersionArgs', 'StateMachineVersion']

@pulumi.input_type
class StateMachineVersionArgs:
    def __init__(__self__, *,
                 state_machine_arn: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 state_machine_revision_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StateMachineVersion resource.
        :param pulumi.Input[str] state_machine_arn: The Amazon Resource Name (ARN) of the state machine.
        :param pulumi.Input[str] description: An optional description of the state machine version.
        :param pulumi.Input[str] state_machine_revision_id: Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration.
               
               Only publish the state machine version if the current state machine's revision ID matches the specified ID. Use this option to avoid publishing a version if the state machine has changed since you last updated it.
               
               To specify the initial state machine revision, set the value as `INITIAL` .
        """
        pulumi.set(__self__, "state_machine_arn", state_machine_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if state_machine_revision_id is not None:
            pulumi.set(__self__, "state_machine_revision_id", state_machine_revision_id)

    @property
    @pulumi.getter(name="stateMachineArn")
    def state_machine_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the state machine.
        """
        return pulumi.get(self, "state_machine_arn")

    @state_machine_arn.setter
    def state_machine_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "state_machine_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of the state machine version.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="stateMachineRevisionId")
    def state_machine_revision_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration.

        Only publish the state machine version if the current state machine's revision ID matches the specified ID. Use this option to avoid publishing a version if the state machine has changed since you last updated it.

        To specify the initial state machine revision, set the value as `INITIAL` .
        """
        return pulumi.get(self, "state_machine_revision_id")

    @state_machine_revision_id.setter
    def state_machine_revision_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state_machine_revision_id", value)


class StateMachineVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 state_machine_arn: Optional[pulumi.Input[str]] = None,
                 state_machine_revision_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for StateMachineVersion

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of the state machine version.
        :param pulumi.Input[str] state_machine_arn: The Amazon Resource Name (ARN) of the state machine.
        :param pulumi.Input[str] state_machine_revision_id: Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration.
               
               Only publish the state machine version if the current state machine's revision ID matches the specified ID. Use this option to avoid publishing a version if the state machine has changed since you last updated it.
               
               To specify the initial state machine revision, set the value as `INITIAL` .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StateMachineVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for StateMachineVersion

        :param str resource_name: The name of the resource.
        :param StateMachineVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StateMachineVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 state_machine_arn: Optional[pulumi.Input[str]] = None,
                 state_machine_revision_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StateMachineVersionArgs.__new__(StateMachineVersionArgs)

            __props__.__dict__["description"] = description
            if state_machine_arn is None and not opts.urn:
                raise TypeError("Missing required property 'state_machine_arn'")
            __props__.__dict__["state_machine_arn"] = state_machine_arn
            __props__.__dict__["state_machine_revision_id"] = state_machine_revision_id
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["stateMachineArn", "stateMachineRevisionId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(StateMachineVersion, __self__).__init__(
            'aws-native:stepfunctions:StateMachineVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StateMachineVersion':
        """
        Get an existing StateMachineVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StateMachineVersionArgs.__new__(StateMachineVersionArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["state_machine_arn"] = None
        __props__.__dict__["state_machine_revision_id"] = None
        return StateMachineVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Returns the ARN of the state machine version. For example, `arn:aws:states:us-east-1:123456789012:stateMachine:myStateMachine:1` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional description of the state machine version.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="stateMachineArn")
    def state_machine_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the state machine.
        """
        return pulumi.get(self, "state_machine_arn")

    @property
    @pulumi.getter(name="stateMachineRevisionId")
    def state_machine_revision_id(self) -> pulumi.Output[Optional[str]]:
        """
        Identifier for a state machine revision, which is an immutable, read-only snapshot of a state machine’s definition and configuration.

        Only publish the state machine version if the current state machine's revision ID matches the specified ID. Use this option to avoid publishing a version if the state machine has changed since you last updated it.

        To specify the initial state machine revision, set the value as `INITIAL` .
        """
        return pulumi.get(self, "state_machine_revision_id")

