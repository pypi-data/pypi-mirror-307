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
    'GetEventBridgeRuleTemplateResult',
    'AwaitableGetEventBridgeRuleTemplateResult',
    'get_event_bridge_rule_template',
    'get_event_bridge_rule_template_output',
]

@pulumi.output_type
class GetEventBridgeRuleTemplateResult:
    def __init__(__self__, arn=None, created_at=None, description=None, event_targets=None, event_type=None, group_id=None, id=None, identifier=None, modified_at=None, name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if event_targets and not isinstance(event_targets, list):
            raise TypeError("Expected argument 'event_targets' to be a list")
        pulumi.set(__self__, "event_targets", event_targets)
        if event_type and not isinstance(event_type, str):
            raise TypeError("Expected argument 'event_type' to be a str")
        pulumi.set(__self__, "event_type", event_type)
        if group_id and not isinstance(group_id, str):
            raise TypeError("Expected argument 'group_id' to be a str")
        pulumi.set(__self__, "group_id", group_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if modified_at and not isinstance(modified_at, str):
            raise TypeError("Expected argument 'modified_at' to be a str")
        pulumi.set(__self__, "modified_at", modified_at)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        An eventbridge rule template's ARN (Amazon Resource Name)
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        Placeholder documentation for __timestampIso8601
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A resource's optional description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventTargets")
    def event_targets(self) -> Optional[Sequence['outputs.EventBridgeRuleTemplateTarget']]:
        """
        Placeholder documentation for __listOfEventBridgeRuleTemplateTarget
        """
        return pulumi.get(self, "event_targets")

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> Optional['EventBridgeRuleTemplateEventType']:
        """
        The type of event to match with the rule.
        """
        return pulumi.get(self, "event_type")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[str]:
        """
        An eventbridge rule template group's id. AWS provided template groups have ids that start with `aws-`
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        An eventbridge rule template's id. AWS provided templates have ids that start with `aws-`
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifier(self) -> Optional[str]:
        """
        Placeholder documentation for __string
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> Optional[str]:
        """
        Placeholder documentation for __timestampIso8601
        """
        return pulumi.get(self, "modified_at")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A resource's name. Names must be unique within the scope of a resource type in a specific region.
        """
        return pulumi.get(self, "name")


class AwaitableGetEventBridgeRuleTemplateResult(GetEventBridgeRuleTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventBridgeRuleTemplateResult(
            arn=self.arn,
            created_at=self.created_at,
            description=self.description,
            event_targets=self.event_targets,
            event_type=self.event_type,
            group_id=self.group_id,
            id=self.id,
            identifier=self.identifier,
            modified_at=self.modified_at,
            name=self.name)


def get_event_bridge_rule_template(identifier: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventBridgeRuleTemplateResult:
    """
    Definition of AWS::MediaLive::EventBridgeRuleTemplate Resource Type


    :param str identifier: Placeholder documentation for __string
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:medialive:getEventBridgeRuleTemplate', __args__, opts=opts, typ=GetEventBridgeRuleTemplateResult).value

    return AwaitableGetEventBridgeRuleTemplateResult(
        arn=pulumi.get(__ret__, 'arn'),
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        event_targets=pulumi.get(__ret__, 'event_targets'),
        event_type=pulumi.get(__ret__, 'event_type'),
        group_id=pulumi.get(__ret__, 'group_id'),
        id=pulumi.get(__ret__, 'id'),
        identifier=pulumi.get(__ret__, 'identifier'),
        modified_at=pulumi.get(__ret__, 'modified_at'),
        name=pulumi.get(__ret__, 'name'))
def get_event_bridge_rule_template_output(identifier: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventBridgeRuleTemplateResult]:
    """
    Definition of AWS::MediaLive::EventBridgeRuleTemplate Resource Type


    :param str identifier: Placeholder documentation for __string
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:medialive:getEventBridgeRuleTemplate', __args__, opts=opts, typ=GetEventBridgeRuleTemplateResult)
    return __ret__.apply(lambda __response__: GetEventBridgeRuleTemplateResult(
        arn=pulumi.get(__response__, 'arn'),
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        event_targets=pulumi.get(__response__, 'event_targets'),
        event_type=pulumi.get(__response__, 'event_type'),
        group_id=pulumi.get(__response__, 'group_id'),
        id=pulumi.get(__response__, 'id'),
        identifier=pulumi.get(__response__, 'identifier'),
        modified_at=pulumi.get(__response__, 'modified_at'),
        name=pulumi.get(__response__, 'name')))
