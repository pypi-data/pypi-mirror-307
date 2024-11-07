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

__all__ = ['UserHierarchyGroupArgs', 'UserHierarchyGroup']

@pulumi.input_type
class UserHierarchyGroupArgs:
    def __init__(__self__, *,
                 instance_arn: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 parent_group_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a UserHierarchyGroup resource.
        :param pulumi.Input[str] instance_arn: The identifier of the Amazon Connect instance.
        :param pulumi.Input[str] name: The name of the user hierarchy group.
        :param pulumi.Input[str] parent_group_arn: The Amazon Resource Name (ARN) for the parent user hierarchy group.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: One or more tags.
        """
        pulumi.set(__self__, "instance_arn", instance_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent_group_arn is not None:
            pulumi.set(__self__, "parent_group_arn", parent_group_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Input[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user hierarchy group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="parentGroupArn")
    def parent_group_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) for the parent user hierarchy group.
        """
        return pulumi.get(self, "parent_group_arn")

    @parent_group_arn.setter
    def parent_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_group_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        One or more tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class UserHierarchyGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_group_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Connect::UserHierarchyGroup

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_arn: The identifier of the Amazon Connect instance.
        :param pulumi.Input[str] name: The name of the user hierarchy group.
        :param pulumi.Input[str] parent_group_arn: The Amazon Resource Name (ARN) for the parent user hierarchy group.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: One or more tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserHierarchyGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Connect::UserHierarchyGroup

        :param str resource_name: The name of the resource.
        :param UserHierarchyGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserHierarchyGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 parent_group_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserHierarchyGroupArgs.__new__(UserHierarchyGroupArgs)

            if instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'instance_arn'")
            __props__.__dict__["instance_arn"] = instance_arn
            __props__.__dict__["name"] = name
            __props__.__dict__["parent_group_arn"] = parent_group_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["user_hierarchy_group_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["parentGroupArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(UserHierarchyGroup, __self__).__init__(
            'aws-native:connect:UserHierarchyGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'UserHierarchyGroup':
        """
        Get an existing UserHierarchyGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = UserHierarchyGroupArgs.__new__(UserHierarchyGroupArgs)

        __props__.__dict__["instance_arn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["parent_group_arn"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["user_hierarchy_group_arn"] = None
        return UserHierarchyGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Output[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the user hierarchy group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentGroupArn")
    def parent_group_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) for the parent user hierarchy group.
        """
        return pulumi.get(self, "parent_group_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        One or more tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="userHierarchyGroupArn")
    def user_hierarchy_group_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the user hierarchy group.
        """
        return pulumi.get(self, "user_hierarchy_group_arn")

