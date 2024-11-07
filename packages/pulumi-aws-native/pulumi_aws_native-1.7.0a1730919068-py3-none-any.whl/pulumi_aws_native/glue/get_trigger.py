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

__all__ = [
    'GetTriggerResult',
    'AwaitableGetTriggerResult',
    'get_trigger',
    'get_trigger_output',
]

@pulumi.output_type
class GetTriggerResult:
    def __init__(__self__, actions=None, description=None, event_batching_condition=None, predicate=None, schedule=None, tags=None):
        if actions and not isinstance(actions, list):
            raise TypeError("Expected argument 'actions' to be a list")
        pulumi.set(__self__, "actions", actions)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if event_batching_condition and not isinstance(event_batching_condition, dict):
            raise TypeError("Expected argument 'event_batching_condition' to be a dict")
        pulumi.set(__self__, "event_batching_condition", event_batching_condition)
        if predicate and not isinstance(predicate, dict):
            raise TypeError("Expected argument 'predicate' to be a dict")
        pulumi.set(__self__, "predicate", predicate)
        if schedule and not isinstance(schedule, str):
            raise TypeError("Expected argument 'schedule' to be a str")
        pulumi.set(__self__, "schedule", schedule)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def actions(self) -> Optional[Sequence['outputs.TriggerAction']]:
        """
        The actions initiated by this trigger.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of this trigger.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventBatchingCondition")
    def event_batching_condition(self) -> Optional['outputs.TriggerEventBatchingCondition']:
        """
        Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.
        """
        return pulumi.get(self, "event_batching_condition")

    @property
    @pulumi.getter
    def predicate(self) -> Optional['outputs.TriggerPredicate']:
        """
        The predicate of this trigger, which defines when it will fire.
        """
        return pulumi.get(self, "predicate")

    @property
    @pulumi.getter
    def schedule(self) -> Optional[str]:
        """
        A cron expression used to specify the schedule.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        The tags to use with this trigger.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Glue::Trigger` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "tags")


class AwaitableGetTriggerResult(GetTriggerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTriggerResult(
            actions=self.actions,
            description=self.description,
            event_batching_condition=self.event_batching_condition,
            predicate=self.predicate,
            schedule=self.schedule,
            tags=self.tags)


def get_trigger(name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTriggerResult:
    """
    Resource Type definition for AWS::Glue::Trigger


    :param str name: The name of the trigger.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:glue:getTrigger', __args__, opts=opts, typ=GetTriggerResult).value

    return AwaitableGetTriggerResult(
        actions=pulumi.get(__ret__, 'actions'),
        description=pulumi.get(__ret__, 'description'),
        event_batching_condition=pulumi.get(__ret__, 'event_batching_condition'),
        predicate=pulumi.get(__ret__, 'predicate'),
        schedule=pulumi.get(__ret__, 'schedule'),
        tags=pulumi.get(__ret__, 'tags'))
def get_trigger_output(name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTriggerResult]:
    """
    Resource Type definition for AWS::Glue::Trigger


    :param str name: The name of the trigger.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:glue:getTrigger', __args__, opts=opts, typ=GetTriggerResult)
    return __ret__.apply(lambda __response__: GetTriggerResult(
        actions=pulumi.get(__response__, 'actions'),
        description=pulumi.get(__response__, 'description'),
        event_batching_condition=pulumi.get(__response__, 'event_batching_condition'),
        predicate=pulumi.get(__response__, 'predicate'),
        schedule=pulumi.get(__response__, 'schedule'),
        tags=pulumi.get(__response__, 'tags')))
