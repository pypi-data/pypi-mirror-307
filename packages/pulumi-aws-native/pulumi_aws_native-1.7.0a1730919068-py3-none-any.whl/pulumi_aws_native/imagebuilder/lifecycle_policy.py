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
from ._inputs import *

__all__ = ['LifecyclePolicyArgs', 'LifecyclePolicy']

@pulumi.input_type
class LifecyclePolicyArgs:
    def __init__(__self__, *,
                 execution_role: pulumi.Input[str],
                 policy_details: pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyPolicyDetailArgs']]],
                 resource_selection: pulumi.Input['LifecyclePolicyResourceSelectionArgs'],
                 resource_type: pulumi.Input['LifecyclePolicyResourceType'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['LifecyclePolicyStatus']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LifecyclePolicy resource.
        :param pulumi.Input[str] execution_role: The execution role of the lifecycle policy.
        :param pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyPolicyDetailArgs']]] policy_details: The policy details of the lifecycle policy.
        :param pulumi.Input['LifecyclePolicyResourceSelectionArgs'] resource_selection: The resource selection of the lifecycle policy.
        :param pulumi.Input['LifecyclePolicyResourceType'] resource_type: The resource type of the lifecycle policy.
        :param pulumi.Input[str] description: The description of the lifecycle policy.
        :param pulumi.Input[str] name: The name of the lifecycle policy.
        :param pulumi.Input['LifecyclePolicyStatus'] status: The status of the lifecycle policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags associated with the lifecycle policy.
        """
        pulumi.set(__self__, "execution_role", execution_role)
        pulumi.set(__self__, "policy_details", policy_details)
        pulumi.set(__self__, "resource_selection", resource_selection)
        pulumi.set(__self__, "resource_type", resource_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="executionRole")
    def execution_role(self) -> pulumi.Input[str]:
        """
        The execution role of the lifecycle policy.
        """
        return pulumi.get(self, "execution_role")

    @execution_role.setter
    def execution_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "execution_role", value)

    @property
    @pulumi.getter(name="policyDetails")
    def policy_details(self) -> pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyPolicyDetailArgs']]]:
        """
        The policy details of the lifecycle policy.
        """
        return pulumi.get(self, "policy_details")

    @policy_details.setter
    def policy_details(self, value: pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyPolicyDetailArgs']]]):
        pulumi.set(self, "policy_details", value)

    @property
    @pulumi.getter(name="resourceSelection")
    def resource_selection(self) -> pulumi.Input['LifecyclePolicyResourceSelectionArgs']:
        """
        The resource selection of the lifecycle policy.
        """
        return pulumi.get(self, "resource_selection")

    @resource_selection.setter
    def resource_selection(self, value: pulumi.Input['LifecyclePolicyResourceSelectionArgs']):
        pulumi.set(self, "resource_selection", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input['LifecyclePolicyResourceType']:
        """
        The resource type of the lifecycle policy.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input['LifecyclePolicyResourceType']):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the lifecycle policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the lifecycle policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input['LifecyclePolicyStatus']]:
        """
        The status of the lifecycle policy.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input['LifecyclePolicyStatus']]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags associated with the lifecycle policy.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class LifecyclePolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 execution_role: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_details: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LifecyclePolicyPolicyDetailArgs', 'LifecyclePolicyPolicyDetailArgsDict']]]]] = None,
                 resource_selection: Optional[pulumi.Input[Union['LifecyclePolicyResourceSelectionArgs', 'LifecyclePolicyResourceSelectionArgsDict']]] = None,
                 resource_type: Optional[pulumi.Input['LifecyclePolicyResourceType']] = None,
                 status: Optional[pulumi.Input['LifecyclePolicyStatus']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::ImageBuilder::LifecyclePolicy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the lifecycle policy.
        :param pulumi.Input[str] execution_role: The execution role of the lifecycle policy.
        :param pulumi.Input[str] name: The name of the lifecycle policy.
        :param pulumi.Input[Sequence[pulumi.Input[Union['LifecyclePolicyPolicyDetailArgs', 'LifecyclePolicyPolicyDetailArgsDict']]]] policy_details: The policy details of the lifecycle policy.
        :param pulumi.Input[Union['LifecyclePolicyResourceSelectionArgs', 'LifecyclePolicyResourceSelectionArgsDict']] resource_selection: The resource selection of the lifecycle policy.
        :param pulumi.Input['LifecyclePolicyResourceType'] resource_type: The resource type of the lifecycle policy.
        :param pulumi.Input['LifecyclePolicyStatus'] status: The status of the lifecycle policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags associated with the lifecycle policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LifecyclePolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::ImageBuilder::LifecyclePolicy

        :param str resource_name: The name of the resource.
        :param LifecyclePolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LifecyclePolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 execution_role: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy_details: Optional[pulumi.Input[Sequence[pulumi.Input[Union['LifecyclePolicyPolicyDetailArgs', 'LifecyclePolicyPolicyDetailArgsDict']]]]] = None,
                 resource_selection: Optional[pulumi.Input[Union['LifecyclePolicyResourceSelectionArgs', 'LifecyclePolicyResourceSelectionArgsDict']]] = None,
                 resource_type: Optional[pulumi.Input['LifecyclePolicyResourceType']] = None,
                 status: Optional[pulumi.Input['LifecyclePolicyStatus']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LifecyclePolicyArgs.__new__(LifecyclePolicyArgs)

            __props__.__dict__["description"] = description
            if execution_role is None and not opts.urn:
                raise TypeError("Missing required property 'execution_role'")
            __props__.__dict__["execution_role"] = execution_role
            __props__.__dict__["name"] = name
            if policy_details is None and not opts.urn:
                raise TypeError("Missing required property 'policy_details'")
            __props__.__dict__["policy_details"] = policy_details
            if resource_selection is None and not opts.urn:
                raise TypeError("Missing required property 'resource_selection'")
            __props__.__dict__["resource_selection"] = resource_selection
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__.__dict__["resource_type"] = resource_type
            __props__.__dict__["status"] = status
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(LifecyclePolicy, __self__).__init__(
            'aws-native:imagebuilder:LifecyclePolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LifecyclePolicy':
        """
        Get an existing LifecyclePolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = LifecyclePolicyArgs.__new__(LifecyclePolicyArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["execution_role"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policy_details"] = None
        __props__.__dict__["resource_selection"] = None
        __props__.__dict__["resource_type"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        return LifecyclePolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the lifecycle policy.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the lifecycle policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="executionRole")
    def execution_role(self) -> pulumi.Output[str]:
        """
        The execution role of the lifecycle policy.
        """
        return pulumi.get(self, "execution_role")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the lifecycle policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyDetails")
    def policy_details(self) -> pulumi.Output[Sequence['outputs.LifecyclePolicyPolicyDetail']]:
        """
        The policy details of the lifecycle policy.
        """
        return pulumi.get(self, "policy_details")

    @property
    @pulumi.getter(name="resourceSelection")
    def resource_selection(self) -> pulumi.Output['outputs.LifecyclePolicyResourceSelection']:
        """
        The resource selection of the lifecycle policy.
        """
        return pulumi.get(self, "resource_selection")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output['LifecyclePolicyResourceType']:
        """
        The resource type of the lifecycle policy.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional['LifecyclePolicyStatus']]:
        """
        The status of the lifecycle policy.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags associated with the lifecycle policy.
        """
        return pulumi.get(self, "tags")

