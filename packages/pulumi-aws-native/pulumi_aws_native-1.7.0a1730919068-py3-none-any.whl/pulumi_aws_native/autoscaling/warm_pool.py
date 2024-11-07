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
from ._inputs import *

__all__ = ['WarmPoolArgs', 'WarmPool']

@pulumi.input_type
class WarmPoolArgs:
    def __init__(__self__, *,
                 auto_scaling_group_name: pulumi.Input[str],
                 instance_reuse_policy: Optional[pulumi.Input['WarmPoolInstanceReusePolicyArgs']] = None,
                 max_group_prepared_capacity: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 pool_state: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WarmPool resource.
        :param pulumi.Input[str] auto_scaling_group_name: The name of the Auto Scaling group.
        :param pulumi.Input['WarmPoolInstanceReusePolicyArgs'] instance_reuse_policy: Indicates whether instances in the Auto Scaling group can be returned to the warm pool on scale in. The default is to terminate instances in the Auto Scaling group when the group scales in.
        :param pulumi.Input[int] max_group_prepared_capacity: Specifies the maximum number of instances that are allowed to be in the warm pool or in any state except `Terminated` for the Auto Scaling group. This is an optional property. Specify it only if you do not want the warm pool size to be determined by the difference between the group's maximum capacity and its desired capacity.
               
               > If a value for `MaxGroupPreparedCapacity` is not specified, Amazon EC2 Auto Scaling launches and maintains the difference between the group's maximum capacity and its desired capacity. If you specify a value for `MaxGroupPreparedCapacity` , Amazon EC2 Auto Scaling uses the difference between the `MaxGroupPreparedCapacity` and the desired capacity instead.
               > 
               > The size of the warm pool is dynamic. Only when `MaxGroupPreparedCapacity` and `MinSize` are set to the same value does the warm pool have an absolute size. 
               
               If the desired capacity of the Auto Scaling group is higher than the `MaxGroupPreparedCapacity` , the capacity of the warm pool is 0, unless you specify a value for `MinSize` . To remove a value that you previously set, include the property but specify -1 for the value.
        :param pulumi.Input[int] min_size: Specifies the minimum number of instances to maintain in the warm pool. This helps you to ensure that there is always a certain number of warmed instances available to handle traffic spikes. Defaults to 0 if not specified.
        :param pulumi.Input[str] pool_state: Sets the instance state to transition to after the lifecycle actions are complete. Default is `Stopped` .
        """
        pulumi.set(__self__, "auto_scaling_group_name", auto_scaling_group_name)
        if instance_reuse_policy is not None:
            pulumi.set(__self__, "instance_reuse_policy", instance_reuse_policy)
        if max_group_prepared_capacity is not None:
            pulumi.set(__self__, "max_group_prepared_capacity", max_group_prepared_capacity)
        if min_size is not None:
            pulumi.set(__self__, "min_size", min_size)
        if pool_state is not None:
            pulumi.set(__self__, "pool_state", pool_state)

    @property
    @pulumi.getter(name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Auto Scaling group.
        """
        return pulumi.get(self, "auto_scaling_group_name")

    @auto_scaling_group_name.setter
    def auto_scaling_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "auto_scaling_group_name", value)

    @property
    @pulumi.getter(name="instanceReusePolicy")
    def instance_reuse_policy(self) -> Optional[pulumi.Input['WarmPoolInstanceReusePolicyArgs']]:
        """
        Indicates whether instances in the Auto Scaling group can be returned to the warm pool on scale in. The default is to terminate instances in the Auto Scaling group when the group scales in.
        """
        return pulumi.get(self, "instance_reuse_policy")

    @instance_reuse_policy.setter
    def instance_reuse_policy(self, value: Optional[pulumi.Input['WarmPoolInstanceReusePolicyArgs']]):
        pulumi.set(self, "instance_reuse_policy", value)

    @property
    @pulumi.getter(name="maxGroupPreparedCapacity")
    def max_group_prepared_capacity(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the maximum number of instances that are allowed to be in the warm pool or in any state except `Terminated` for the Auto Scaling group. This is an optional property. Specify it only if you do not want the warm pool size to be determined by the difference between the group's maximum capacity and its desired capacity.

        > If a value for `MaxGroupPreparedCapacity` is not specified, Amazon EC2 Auto Scaling launches and maintains the difference between the group's maximum capacity and its desired capacity. If you specify a value for `MaxGroupPreparedCapacity` , Amazon EC2 Auto Scaling uses the difference between the `MaxGroupPreparedCapacity` and the desired capacity instead.
        > 
        > The size of the warm pool is dynamic. Only when `MaxGroupPreparedCapacity` and `MinSize` are set to the same value does the warm pool have an absolute size. 

        If the desired capacity of the Auto Scaling group is higher than the `MaxGroupPreparedCapacity` , the capacity of the warm pool is 0, unless you specify a value for `MinSize` . To remove a value that you previously set, include the property but specify -1 for the value.
        """
        return pulumi.get(self, "max_group_prepared_capacity")

    @max_group_prepared_capacity.setter
    def max_group_prepared_capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_group_prepared_capacity", value)

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the minimum number of instances to maintain in the warm pool. This helps you to ensure that there is always a certain number of warmed instances available to handle traffic spikes. Defaults to 0 if not specified.
        """
        return pulumi.get(self, "min_size")

    @min_size.setter
    def min_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_size", value)

    @property
    @pulumi.getter(name="poolState")
    def pool_state(self) -> Optional[pulumi.Input[str]]:
        """
        Sets the instance state to transition to after the lifecycle actions are complete. Default is `Stopped` .
        """
        return pulumi.get(self, "pool_state")

    @pool_state.setter
    def pool_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pool_state", value)


class WarmPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_scaling_group_name: Optional[pulumi.Input[str]] = None,
                 instance_reuse_policy: Optional[pulumi.Input[Union['WarmPoolInstanceReusePolicyArgs', 'WarmPoolInstanceReusePolicyArgsDict']]] = None,
                 max_group_prepared_capacity: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 pool_state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::AutoScaling::WarmPool.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_scaling_group_name: The name of the Auto Scaling group.
        :param pulumi.Input[Union['WarmPoolInstanceReusePolicyArgs', 'WarmPoolInstanceReusePolicyArgsDict']] instance_reuse_policy: Indicates whether instances in the Auto Scaling group can be returned to the warm pool on scale in. The default is to terminate instances in the Auto Scaling group when the group scales in.
        :param pulumi.Input[int] max_group_prepared_capacity: Specifies the maximum number of instances that are allowed to be in the warm pool or in any state except `Terminated` for the Auto Scaling group. This is an optional property. Specify it only if you do not want the warm pool size to be determined by the difference between the group's maximum capacity and its desired capacity.
               
               > If a value for `MaxGroupPreparedCapacity` is not specified, Amazon EC2 Auto Scaling launches and maintains the difference between the group's maximum capacity and its desired capacity. If you specify a value for `MaxGroupPreparedCapacity` , Amazon EC2 Auto Scaling uses the difference between the `MaxGroupPreparedCapacity` and the desired capacity instead.
               > 
               > The size of the warm pool is dynamic. Only when `MaxGroupPreparedCapacity` and `MinSize` are set to the same value does the warm pool have an absolute size. 
               
               If the desired capacity of the Auto Scaling group is higher than the `MaxGroupPreparedCapacity` , the capacity of the warm pool is 0, unless you specify a value for `MinSize` . To remove a value that you previously set, include the property but specify -1 for the value.
        :param pulumi.Input[int] min_size: Specifies the minimum number of instances to maintain in the warm pool. This helps you to ensure that there is always a certain number of warmed instances available to handle traffic spikes. Defaults to 0 if not specified.
        :param pulumi.Input[str] pool_state: Sets the instance state to transition to after the lifecycle actions are complete. Default is `Stopped` .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WarmPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::AutoScaling::WarmPool.

        :param str resource_name: The name of the resource.
        :param WarmPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WarmPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_scaling_group_name: Optional[pulumi.Input[str]] = None,
                 instance_reuse_policy: Optional[pulumi.Input[Union['WarmPoolInstanceReusePolicyArgs', 'WarmPoolInstanceReusePolicyArgsDict']]] = None,
                 max_group_prepared_capacity: Optional[pulumi.Input[int]] = None,
                 min_size: Optional[pulumi.Input[int]] = None,
                 pool_state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WarmPoolArgs.__new__(WarmPoolArgs)

            if auto_scaling_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'auto_scaling_group_name'")
            __props__.__dict__["auto_scaling_group_name"] = auto_scaling_group_name
            __props__.__dict__["instance_reuse_policy"] = instance_reuse_policy
            __props__.__dict__["max_group_prepared_capacity"] = max_group_prepared_capacity
            __props__.__dict__["min_size"] = min_size
            __props__.__dict__["pool_state"] = pool_state
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["autoScalingGroupName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(WarmPool, __self__).__init__(
            'aws-native:autoscaling:WarmPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WarmPool':
        """
        Get an existing WarmPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WarmPoolArgs.__new__(WarmPoolArgs)

        __props__.__dict__["auto_scaling_group_name"] = None
        __props__.__dict__["instance_reuse_policy"] = None
        __props__.__dict__["max_group_prepared_capacity"] = None
        __props__.__dict__["min_size"] = None
        __props__.__dict__["pool_state"] = None
        return WarmPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Auto Scaling group.
        """
        return pulumi.get(self, "auto_scaling_group_name")

    @property
    @pulumi.getter(name="instanceReusePolicy")
    def instance_reuse_policy(self) -> pulumi.Output[Optional['outputs.WarmPoolInstanceReusePolicy']]:
        """
        Indicates whether instances in the Auto Scaling group can be returned to the warm pool on scale in. The default is to terminate instances in the Auto Scaling group when the group scales in.
        """
        return pulumi.get(self, "instance_reuse_policy")

    @property
    @pulumi.getter(name="maxGroupPreparedCapacity")
    def max_group_prepared_capacity(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the maximum number of instances that are allowed to be in the warm pool or in any state except `Terminated` for the Auto Scaling group. This is an optional property. Specify it only if you do not want the warm pool size to be determined by the difference between the group's maximum capacity and its desired capacity.

        > If a value for `MaxGroupPreparedCapacity` is not specified, Amazon EC2 Auto Scaling launches and maintains the difference between the group's maximum capacity and its desired capacity. If you specify a value for `MaxGroupPreparedCapacity` , Amazon EC2 Auto Scaling uses the difference between the `MaxGroupPreparedCapacity` and the desired capacity instead.
        > 
        > The size of the warm pool is dynamic. Only when `MaxGroupPreparedCapacity` and `MinSize` are set to the same value does the warm pool have an absolute size. 

        If the desired capacity of the Auto Scaling group is higher than the `MaxGroupPreparedCapacity` , the capacity of the warm pool is 0, unless you specify a value for `MinSize` . To remove a value that you previously set, include the property but specify -1 for the value.
        """
        return pulumi.get(self, "max_group_prepared_capacity")

    @property
    @pulumi.getter(name="minSize")
    def min_size(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the minimum number of instances to maintain in the warm pool. This helps you to ensure that there is always a certain number of warmed instances available to handle traffic spikes. Defaults to 0 if not specified.
        """
        return pulumi.get(self, "min_size")

    @property
    @pulumi.getter(name="poolState")
    def pool_state(self) -> pulumi.Output[Optional[str]]:
        """
        Sets the instance state to transition to after the lifecycle actions are complete. Default is `Stopped` .
        """
        return pulumi.get(self, "pool_state")

