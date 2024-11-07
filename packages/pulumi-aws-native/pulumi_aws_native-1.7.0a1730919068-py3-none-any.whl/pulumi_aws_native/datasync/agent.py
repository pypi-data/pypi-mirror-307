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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._enums import *

__all__ = ['AgentArgs', 'Agent']

@pulumi.input_type
class AgentArgs:
    def __init__(__self__, *,
                 activation_key: Optional[pulumi.Input[str]] = None,
                 agent_name: Optional[pulumi.Input[str]] = None,
                 security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Agent resource.
        :param pulumi.Input[str] activation_key: Activation key of the Agent.
        :param pulumi.Input[str] agent_name: The name configured for the agent. Text reference used to identify the agent in the console.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: The ARNs of the security group used to protect your data transfer task subnets.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_arns: The ARNs of the subnets in which DataSync will create elastic network interfaces for each data transfer task.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[str] vpc_endpoint_id: The ID of the VPC endpoint that the agent has access to.
        """
        if activation_key is not None:
            pulumi.set(__self__, "activation_key", activation_key)
        if agent_name is not None:
            pulumi.set(__self__, "agent_name", agent_name)
        if security_group_arns is not None:
            pulumi.set(__self__, "security_group_arns", security_group_arns)
        if subnet_arns is not None:
            pulumi.set(__self__, "subnet_arns", subnet_arns)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)

    @property
    @pulumi.getter(name="activationKey")
    def activation_key(self) -> Optional[pulumi.Input[str]]:
        """
        Activation key of the Agent.
        """
        return pulumi.get(self, "activation_key")

    @activation_key.setter
    def activation_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "activation_key", value)

    @property
    @pulumi.getter(name="agentName")
    def agent_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name configured for the agent. Text reference used to identify the agent in the console.
        """
        return pulumi.get(self, "agent_name")

    @agent_name.setter
    def agent_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_name", value)

    @property
    @pulumi.getter(name="securityGroupArns")
    def security_group_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The ARNs of the security group used to protect your data transfer task subnets.
        """
        return pulumi.get(self, "security_group_arns")

    @security_group_arns.setter
    def security_group_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_arns", value)

    @property
    @pulumi.getter(name="subnetArns")
    def subnet_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The ARNs of the subnets in which DataSync will create elastic network interfaces for each data transfer task.
        """
        return pulumi.get(self, "subnet_arns")

    @subnet_arns.setter
    def subnet_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_arns", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC endpoint that the agent has access to.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_endpoint_id", value)


class Agent(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 activation_key: Optional[pulumi.Input[str]] = None,
                 agent_name: Optional[pulumi.Input[str]] = None,
                 security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::DataSync::Agent.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        agent = aws_native.datasync.Agent("agent",
            activation_key="AAAAA-7AAAA-GG7MC-3I9R3-27COD",
            agent_name="MyAgent")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        agent = aws_native.datasync.Agent("agent",
            activation_key="AAAAA-7AAAA-GG7MC-3I9R3-27COD",
            agent_name="MyAgent")

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] activation_key: Activation key of the Agent.
        :param pulumi.Input[str] agent_name: The name configured for the agent. Text reference used to identify the agent in the console.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: The ARNs of the security group used to protect your data transfer task subnets.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_arns: The ARNs of the subnets in which DataSync will create elastic network interfaces for each data transfer task.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[str] vpc_endpoint_id: The ID of the VPC endpoint that the agent has access to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AgentArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::DataSync::Agent.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        agent = aws_native.datasync.Agent("agent",
            activation_key="AAAAA-7AAAA-GG7MC-3I9R3-27COD",
            agent_name="MyAgent")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        agent = aws_native.datasync.Agent("agent",
            activation_key="AAAAA-7AAAA-GG7MC-3I9R3-27COD",
            agent_name="MyAgent")

        ```

        :param str resource_name: The name of the resource.
        :param AgentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AgentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 activation_key: Optional[pulumi.Input[str]] = None,
                 agent_name: Optional[pulumi.Input[str]] = None,
                 security_group_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AgentArgs.__new__(AgentArgs)

            __props__.__dict__["activation_key"] = activation_key
            __props__.__dict__["agent_name"] = agent_name
            __props__.__dict__["security_group_arns"] = security_group_arns
            __props__.__dict__["subnet_arns"] = subnet_arns
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vpc_endpoint_id"] = vpc_endpoint_id
            __props__.__dict__["agent_arn"] = None
            __props__.__dict__["endpoint_type"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["activationKey", "securityGroupArns[*]", "subnetArns[*]", "vpcEndpointId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Agent, __self__).__init__(
            'aws-native:datasync:Agent',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Agent':
        """
        Get an existing Agent resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AgentArgs.__new__(AgentArgs)

        __props__.__dict__["activation_key"] = None
        __props__.__dict__["agent_arn"] = None
        __props__.__dict__["agent_name"] = None
        __props__.__dict__["endpoint_type"] = None
        __props__.__dict__["security_group_arns"] = None
        __props__.__dict__["subnet_arns"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["vpc_endpoint_id"] = None
        return Agent(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="activationKey")
    def activation_key(self) -> pulumi.Output[Optional[str]]:
        """
        Activation key of the Agent.
        """
        return pulumi.get(self, "activation_key")

    @property
    @pulumi.getter(name="agentArn")
    def agent_arn(self) -> pulumi.Output[str]:
        """
        The DataSync Agent ARN.
        """
        return pulumi.get(self, "agent_arn")

    @property
    @pulumi.getter(name="agentName")
    def agent_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name configured for the agent. Text reference used to identify the agent in the console.
        """
        return pulumi.get(self, "agent_name")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> pulumi.Output['AgentEndpointType']:
        """
        The service endpoints that the agent will connect to.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="securityGroupArns")
    def security_group_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The ARNs of the security group used to protect your data transfer task subnets.
        """
        return pulumi.get(self, "security_group_arns")

    @property
    @pulumi.getter(name="subnetArns")
    def subnet_arns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The ARNs of the subnets in which DataSync will create elastic network interfaces for each data transfer task.
        """
        return pulumi.get(self, "subnet_arns")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the VPC endpoint that the agent has access to.
        """
        return pulumi.get(self, "vpc_endpoint_id")

