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

__all__ = ['IpamScopeArgs', 'IpamScope']

@pulumi.input_type
class IpamScopeArgs:
    def __init__(__self__, *,
                 ipam_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a IpamScope resource.
        :param pulumi.Input[str] ipam_id: The Id of the IPAM this scope is a part of.
        :param pulumi.Input[str] description: The description of the scope.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "ipam_id", ipam_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="ipamId")
    def ipam_id(self) -> pulumi.Input[str]:
        """
        The Id of the IPAM this scope is a part of.
        """
        return pulumi.get(self, "ipam_id")

    @ipam_id.setter
    def ipam_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ipam_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the scope.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

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


class IpamScope(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ipam_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Schema of AWS::EC2::IPAMScope Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the scope.
        :param pulumi.Input[str] ipam_id: The Id of the IPAM this scope is a part of.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IpamScopeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Schema of AWS::EC2::IPAMScope Type

        :param str resource_name: The name of the resource.
        :param IpamScopeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IpamScopeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ipam_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IpamScopeArgs.__new__(IpamScopeArgs)

            __props__.__dict__["description"] = description
            if ipam_id is None and not opts.urn:
                raise TypeError("Missing required property 'ipam_id'")
            __props__.__dict__["ipam_id"] = ipam_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["ipam_arn"] = None
            __props__.__dict__["ipam_scope_id"] = None
            __props__.__dict__["ipam_scope_type"] = None
            __props__.__dict__["is_default"] = None
            __props__.__dict__["pool_count"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["ipamId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(IpamScope, __self__).__init__(
            'aws-native:ec2:IpamScope',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IpamScope':
        """
        Get an existing IpamScope resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IpamScopeArgs.__new__(IpamScopeArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["ipam_arn"] = None
        __props__.__dict__["ipam_id"] = None
        __props__.__dict__["ipam_scope_id"] = None
        __props__.__dict__["ipam_scope_type"] = None
        __props__.__dict__["is_default"] = None
        __props__.__dict__["pool_count"] = None
        __props__.__dict__["tags"] = None
        return IpamScope(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IPAM scope.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the scope.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ipamArn")
    def ipam_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IPAM this scope is a part of.
        """
        return pulumi.get(self, "ipam_arn")

    @property
    @pulumi.getter(name="ipamId")
    def ipam_id(self) -> pulumi.Output[str]:
        """
        The Id of the IPAM this scope is a part of.
        """
        return pulumi.get(self, "ipam_id")

    @property
    @pulumi.getter(name="ipamScopeId")
    def ipam_scope_id(self) -> pulumi.Output[str]:
        """
        Id of the IPAM scope.
        """
        return pulumi.get(self, "ipam_scope_id")

    @property
    @pulumi.getter(name="ipamScopeType")
    def ipam_scope_type(self) -> pulumi.Output['IpamScopeType']:
        """
        Determines whether this scope contains publicly routable space or space for a private network
        """
        return pulumi.get(self, "ipam_scope_type")

    @property
    @pulumi.getter(name="isDefault")
    def is_default(self) -> pulumi.Output[bool]:
        """
        Is this one of the default scopes created with the IPAM.
        """
        return pulumi.get(self, "is_default")

    @property
    @pulumi.getter(name="poolCount")
    def pool_count(self) -> pulumi.Output[int]:
        """
        The number of pools that currently exist in this scope.
        """
        return pulumi.get(self, "pool_count")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

