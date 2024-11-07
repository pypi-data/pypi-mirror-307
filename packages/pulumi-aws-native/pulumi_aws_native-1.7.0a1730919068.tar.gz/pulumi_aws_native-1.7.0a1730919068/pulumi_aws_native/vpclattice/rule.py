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

__all__ = ['RuleArgs', 'Rule']

@pulumi.input_type
class RuleArgs:
    def __init__(__self__, *,
                 action: pulumi.Input['RuleActionArgs'],
                 match: pulumi.Input['RuleMatchArgs'],
                 priority: pulumi.Input[int],
                 listener_identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Rule resource.
        :param pulumi.Input['RuleActionArgs'] action: Describes the action for a rule.
        :param pulumi.Input['RuleMatchArgs'] match: The rule match.
        :param pulumi.Input[int] priority: The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        :param pulumi.Input[str] listener_identifier: The ID or Amazon Resource Name (ARN) of the listener.
        :param pulumi.Input[str] name: The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.
               
               If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param pulumi.Input[str] service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags for the rule.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "match", match)
        pulumi.set(__self__, "priority", priority)
        if listener_identifier is not None:
            pulumi.set(__self__, "listener_identifier", listener_identifier)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if service_identifier is not None:
            pulumi.set(__self__, "service_identifier", service_identifier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input['RuleActionArgs']:
        """
        Describes the action for a rule.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input['RuleActionArgs']):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def match(self) -> pulumi.Input['RuleMatchArgs']:
        """
        The rule match.
        """
        return pulumi.get(self, "match")

    @match.setter
    def match(self, value: pulumi.Input['RuleMatchArgs']):
        pulumi.set(self, "match", value)

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Input[int]:
        """
        The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: pulumi.Input[int]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter(name="listenerIdentifier")
    def listener_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or Amazon Resource Name (ARN) of the listener.
        """
        return pulumi.get(self, "listener_identifier")

    @listener_identifier.setter
    def listener_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_identifier", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serviceIdentifier")
    def service_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The ID or Amazon Resource Name (ARN) of the service.
        """
        return pulumi.get(self, "service_identifier")

    @service_identifier.setter
    def service_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_identifier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags for the rule.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Rule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[Union['RuleActionArgs', 'RuleActionArgsDict']]] = None,
                 listener_identifier: Optional[pulumi.Input[str]] = None,
                 match: Optional[pulumi.Input[Union['RuleMatchArgs', 'RuleMatchArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 service_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Creates a listener rule. Each listener has a default rule for checking connection requests, but you can define additional rules. Each rule consists of a priority, one or more actions, and one or more conditions.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['RuleActionArgs', 'RuleActionArgsDict']] action: Describes the action for a rule.
        :param pulumi.Input[str] listener_identifier: The ID or Amazon Resource Name (ARN) of the listener.
        :param pulumi.Input[Union['RuleMatchArgs', 'RuleMatchArgsDict']] match: The rule match.
        :param pulumi.Input[str] name: The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.
               
               If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param pulumi.Input[int] priority: The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        :param pulumi.Input[str] service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags for the rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a listener rule. Each listener has a default rule for checking connection requests, but you can define additional rules. Each rule consists of a priority, one or more actions, and one or more conditions.

        :param str resource_name: The name of the resource.
        :param RuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[Union['RuleActionArgs', 'RuleActionArgsDict']]] = None,
                 listener_identifier: Optional[pulumi.Input[str]] = None,
                 match: Optional[pulumi.Input[Union['RuleMatchArgs', 'RuleMatchArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 service_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RuleArgs.__new__(RuleArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["listener_identifier"] = listener_identifier
            if match is None and not opts.urn:
                raise TypeError("Missing required property 'match'")
            __props__.__dict__["match"] = match
            __props__.__dict__["name"] = name
            if priority is None and not opts.urn:
                raise TypeError("Missing required property 'priority'")
            __props__.__dict__["priority"] = priority
            __props__.__dict__["service_identifier"] = service_identifier
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["aws_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["listenerIdentifier", "name", "serviceIdentifier"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Rule, __self__).__init__(
            'aws-native:vpclattice:Rule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Rule':
        """
        Get an existing Rule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RuleArgs.__new__(RuleArgs)

        __props__.__dict__["action"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["aws_id"] = None
        __props__.__dict__["listener_identifier"] = None
        __props__.__dict__["match"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["priority"] = None
        __props__.__dict__["service_identifier"] = None
        __props__.__dict__["tags"] = None
        return Rule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output['outputs.RuleAction']:
        """
        Describes the action for a rule.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the rule.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The ID of the listener.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="listenerIdentifier")
    def listener_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        The ID or Amazon Resource Name (ARN) of the listener.
        """
        return pulumi.get(self, "listener_identifier")

    @property
    @pulumi.getter
    def match(self) -> pulumi.Output['outputs.RuleMatch']:
        """
        The rule match.
        """
        return pulumi.get(self, "match")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[int]:
        """
        The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="serviceIdentifier")
    def service_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        The ID or Amazon Resource Name (ARN) of the service.
        """
        return pulumi.get(self, "service_identifier")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags for the rule.
        """
        return pulumi.get(self, "tags")

