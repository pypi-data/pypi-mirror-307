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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._enums import *
from ._inputs import *

__all__ = ['TargetGroupArgs', 'TargetGroup']

@pulumi.input_type
class TargetGroupArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['TargetGroupType'],
                 config: Optional[pulumi.Input['TargetGroupConfigArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetArgs']]]] = None):
        """
        The set of arguments for constructing a TargetGroup resource.
        :param pulumi.Input['TargetGroupType'] type: The type of target group.
        :param pulumi.Input['TargetGroupConfigArgs'] config: The target group configuration.
        :param pulumi.Input[str] name: The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.
               
               If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags for the target group.
        :param pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetArgs']]] targets: Describes a target.
        """
        pulumi.set(__self__, "type", type)
        if config is not None:
            pulumi.set(__self__, "config", config)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['TargetGroupType']:
        """
        The type of target group.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['TargetGroupType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def config(self) -> Optional[pulumi.Input['TargetGroupConfigArgs']]:
        """
        The target group configuration.
        """
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: Optional[pulumi.Input['TargetGroupConfigArgs']]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags for the target group.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetArgs']]]]:
        """
        Describes a target.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TargetGroupTargetArgs']]]]):
        pulumi.set(self, "targets", value)


class TargetGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[Union['TargetGroupConfigArgs', 'TargetGroupConfigArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupTargetArgs', 'TargetGroupTargetArgsDict']]]]] = None,
                 type: Optional[pulumi.Input['TargetGroupType']] = None,
                 __props__=None):
        """
        A target group is a collection of targets, or compute resources, that run your application or service. A target group can only be used by a single service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['TargetGroupConfigArgs', 'TargetGroupConfigArgsDict']] config: The target group configuration.
        :param pulumi.Input[str] name: The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.
               
               If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags for the target group.
        :param pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupTargetArgs', 'TargetGroupTargetArgsDict']]]] targets: Describes a target.
        :param pulumi.Input['TargetGroupType'] type: The type of target group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TargetGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A target group is a collection of targets, or compute resources, that run your application or service. A target group can only be used by a single service.

        :param str resource_name: The name of the resource.
        :param TargetGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TargetGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[Union['TargetGroupConfigArgs', 'TargetGroupConfigArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TargetGroupTargetArgs', 'TargetGroupTargetArgsDict']]]]] = None,
                 type: Optional[pulumi.Input['TargetGroupType']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TargetGroupArgs.__new__(TargetGroupArgs)

            __props__.__dict__["config"] = config
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["targets"] = targets
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["arn"] = None
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["last_updated_at"] = None
            __props__.__dict__["status"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["config.ipAddressType", "config.lambdaEventStructureVersion", "config.port", "config.protocol", "config.protocolVersion", "config.vpcIdentifier", "name", "type"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TargetGroup, __self__).__init__(
            'aws-native:vpclattice:TargetGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TargetGroup':
        """
        Get an existing TargetGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TargetGroupArgs.__new__(TargetGroupArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["config"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["last_updated_at"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["targets"] = None
        __props__.__dict__["type"] = None
        return TargetGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the target group.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The ID of the target group.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output[Optional['outputs.TargetGroupConfig']]:
        """
        The target group configuration.
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The date and time that the target group was created, specified in ISO-8601 format.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="lastUpdatedAt")
    def last_updated_at(self) -> pulumi.Output[str]:
        """
        The date and time that the target group was last updated, specified in ISO-8601 format.
        """
        return pulumi.get(self, "last_updated_at")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['TargetGroupStatus']:
        """
        The operation's status. You can retry the operation if the status is `CREATE_FAILED` . However, if you retry it while the status is `CREATE_IN_PROGRESS` , there is no change in the status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags for the target group.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Output[Optional[Sequence['outputs.TargetGroupTarget']]]:
        """
        Describes a target.
        """
        return pulumi.get(self, "targets")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output['TargetGroupType']:
        """
        The type of target group.
        """
        return pulumi.get(self, "type")

