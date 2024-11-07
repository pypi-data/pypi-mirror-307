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
    'GetTaskDefinitionResult',
    'AwaitableGetTaskDefinitionResult',
    'get_task_definition',
    'get_task_definition_output',
]

@pulumi.output_type
class GetTaskDefinitionResult:
    def __init__(__self__, arn=None, auto_create_tasks=None, id=None, lo_ra_wan_update_gateway_task_entry=None, name=None, tags=None, task_definition_type=None, update=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auto_create_tasks and not isinstance(auto_create_tasks, bool):
            raise TypeError("Expected argument 'auto_create_tasks' to be a bool")
        pulumi.set(__self__, "auto_create_tasks", auto_create_tasks)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lo_ra_wan_update_gateway_task_entry and not isinstance(lo_ra_wan_update_gateway_task_entry, dict):
            raise TypeError("Expected argument 'lo_ra_wan_update_gateway_task_entry' to be a dict")
        pulumi.set(__self__, "lo_ra_wan_update_gateway_task_entry", lo_ra_wan_update_gateway_task_entry)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if task_definition_type and not isinstance(task_definition_type, str):
            raise TypeError("Expected argument 'task_definition_type' to be a str")
        pulumi.set(__self__, "task_definition_type", task_definition_type)
        if update and not isinstance(update, dict):
            raise TypeError("Expected argument 'update' to be a dict")
        pulumi.set(__self__, "update", update)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        TaskDefinition arn. Returned after successful create.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoCreateTasks")
    def auto_create_tasks(self) -> Optional[bool]:
        """
        Whether to automatically create tasks using this task definition for all gateways with the specified current version. If false, the task must me created by calling CreateWirelessGatewayTask.
        """
        return pulumi.get(self, "auto_create_tasks")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the new wireless gateway task definition
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="loRaWanUpdateGatewayTaskEntry")
    def lo_ra_wan_update_gateway_task_entry(self) -> Optional['outputs.TaskDefinitionLoRaWanUpdateGatewayTaskEntry']:
        """
        The list of task definitions.
        """
        return pulumi.get(self, "lo_ra_wan_update_gateway_task_entry")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the new resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of key-value pairs that contain metadata for the destination.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="taskDefinitionType")
    def task_definition_type(self) -> Optional['TaskDefinitionType']:
        """
        A filter to list only the wireless gateway task definitions that use this task definition type
        """
        return pulumi.get(self, "task_definition_type")

    @property
    @pulumi.getter
    def update(self) -> Optional['outputs.TaskDefinitionUpdateWirelessGatewayTaskCreate']:
        """
        Information about the gateways to update.
        """
        return pulumi.get(self, "update")


class AwaitableGetTaskDefinitionResult(GetTaskDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTaskDefinitionResult(
            arn=self.arn,
            auto_create_tasks=self.auto_create_tasks,
            id=self.id,
            lo_ra_wan_update_gateway_task_entry=self.lo_ra_wan_update_gateway_task_entry,
            name=self.name,
            tags=self.tags,
            task_definition_type=self.task_definition_type,
            update=self.update)


def get_task_definition(id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTaskDefinitionResult:
    """
    Creates a gateway task definition.


    :param str id: The ID of the new wireless gateway task definition
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iotwireless:getTaskDefinition', __args__, opts=opts, typ=GetTaskDefinitionResult).value

    return AwaitableGetTaskDefinitionResult(
        arn=pulumi.get(__ret__, 'arn'),
        auto_create_tasks=pulumi.get(__ret__, 'auto_create_tasks'),
        id=pulumi.get(__ret__, 'id'),
        lo_ra_wan_update_gateway_task_entry=pulumi.get(__ret__, 'lo_ra_wan_update_gateway_task_entry'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        task_definition_type=pulumi.get(__ret__, 'task_definition_type'),
        update=pulumi.get(__ret__, 'update'))
def get_task_definition_output(id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTaskDefinitionResult]:
    """
    Creates a gateway task definition.


    :param str id: The ID of the new wireless gateway task definition
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iotwireless:getTaskDefinition', __args__, opts=opts, typ=GetTaskDefinitionResult)
    return __ret__.apply(lambda __response__: GetTaskDefinitionResult(
        arn=pulumi.get(__response__, 'arn'),
        auto_create_tasks=pulumi.get(__response__, 'auto_create_tasks'),
        id=pulumi.get(__response__, 'id'),
        lo_ra_wan_update_gateway_task_entry=pulumi.get(__response__, 'lo_ra_wan_update_gateway_task_entry'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags'),
        task_definition_type=pulumi.get(__response__, 'task_definition_type'),
        update=pulumi.get(__response__, 'update')))
