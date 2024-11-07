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

__all__ = ['QueueFleetAssociationArgs', 'QueueFleetAssociation']

@pulumi.input_type
class QueueFleetAssociationArgs:
    def __init__(__self__, *,
                 farm_id: pulumi.Input[str],
                 fleet_id: pulumi.Input[str],
                 queue_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a QueueFleetAssociation resource.
        :param pulumi.Input[str] farm_id: The identifier of the farm that contains the queue and the fleet.
        :param pulumi.Input[str] fleet_id: The fleet ID.
        :param pulumi.Input[str] queue_id: The queue ID.
        """
        pulumi.set(__self__, "farm_id", farm_id)
        pulumi.set(__self__, "fleet_id", fleet_id)
        pulumi.set(__self__, "queue_id", queue_id)

    @property
    @pulumi.getter(name="farmId")
    def farm_id(self) -> pulumi.Input[str]:
        """
        The identifier of the farm that contains the queue and the fleet.
        """
        return pulumi.get(self, "farm_id")

    @farm_id.setter
    def farm_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "farm_id", value)

    @property
    @pulumi.getter(name="fleetId")
    def fleet_id(self) -> pulumi.Input[str]:
        """
        The fleet ID.
        """
        return pulumi.get(self, "fleet_id")

    @fleet_id.setter
    def fleet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "fleet_id", value)

    @property
    @pulumi.getter(name="queueId")
    def queue_id(self) -> pulumi.Input[str]:
        """
        The queue ID.
        """
        return pulumi.get(self, "queue_id")

    @queue_id.setter
    def queue_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "queue_id", value)


class QueueFleetAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 farm_id: Optional[pulumi.Input[str]] = None,
                 fleet_id: Optional[pulumi.Input[str]] = None,
                 queue_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Definition of AWS::Deadline::QueueFleetAssociation Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] farm_id: The identifier of the farm that contains the queue and the fleet.
        :param pulumi.Input[str] fleet_id: The fleet ID.
        :param pulumi.Input[str] queue_id: The queue ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueueFleetAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Deadline::QueueFleetAssociation Resource Type

        :param str resource_name: The name of the resource.
        :param QueueFleetAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueueFleetAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 farm_id: Optional[pulumi.Input[str]] = None,
                 fleet_id: Optional[pulumi.Input[str]] = None,
                 queue_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueueFleetAssociationArgs.__new__(QueueFleetAssociationArgs)

            if farm_id is None and not opts.urn:
                raise TypeError("Missing required property 'farm_id'")
            __props__.__dict__["farm_id"] = farm_id
            if fleet_id is None and not opts.urn:
                raise TypeError("Missing required property 'fleet_id'")
            __props__.__dict__["fleet_id"] = fleet_id
            if queue_id is None and not opts.urn:
                raise TypeError("Missing required property 'queue_id'")
            __props__.__dict__["queue_id"] = queue_id
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["farmId", "fleetId", "queueId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(QueueFleetAssociation, __self__).__init__(
            'aws-native:deadline:QueueFleetAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'QueueFleetAssociation':
        """
        Get an existing QueueFleetAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = QueueFleetAssociationArgs.__new__(QueueFleetAssociationArgs)

        __props__.__dict__["farm_id"] = None
        __props__.__dict__["fleet_id"] = None
        __props__.__dict__["queue_id"] = None
        return QueueFleetAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="farmId")
    def farm_id(self) -> pulumi.Output[str]:
        """
        The identifier of the farm that contains the queue and the fleet.
        """
        return pulumi.get(self, "farm_id")

    @property
    @pulumi.getter(name="fleetId")
    def fleet_id(self) -> pulumi.Output[str]:
        """
        The fleet ID.
        """
        return pulumi.get(self, "fleet_id")

    @property
    @pulumi.getter(name="queueId")
    def queue_id(self) -> pulumi.Output[str]:
        """
        The queue ID.
        """
        return pulumi.get(self, "queue_id")

