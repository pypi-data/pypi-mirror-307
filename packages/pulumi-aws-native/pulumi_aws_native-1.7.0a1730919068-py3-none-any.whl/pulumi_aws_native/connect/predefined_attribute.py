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

__all__ = ['PredefinedAttributeArgs', 'PredefinedAttribute']

@pulumi.input_type
class PredefinedAttributeArgs:
    def __init__(__self__, *,
                 instance_arn: pulumi.Input[str],
                 values: pulumi.Input['ValuesPropertiesArgs'],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PredefinedAttribute resource.
        :param pulumi.Input[str] instance_arn: The identifier of the Amazon Connect instance.
        :param pulumi.Input['ValuesPropertiesArgs'] values: The values of a predefined attribute.
        :param pulumi.Input[str] name: The name of the predefined attribute.
        """
        pulumi.set(__self__, "instance_arn", instance_arn)
        pulumi.set(__self__, "values", values)
        if name is not None:
            pulumi.set(__self__, "name", name)

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
    def values(self) -> pulumi.Input['ValuesPropertiesArgs']:
        """
        The values of a predefined attribute.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: pulumi.Input['ValuesPropertiesArgs']):
        pulumi.set(self, "values", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the predefined attribute.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class PredefinedAttribute(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 values: Optional[pulumi.Input[Union['ValuesPropertiesArgs', 'ValuesPropertiesArgsDict']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Connect::PredefinedAttribute

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_arn: The identifier of the Amazon Connect instance.
        :param pulumi.Input[str] name: The name of the predefined attribute.
        :param pulumi.Input[Union['ValuesPropertiesArgs', 'ValuesPropertiesArgsDict']] values: The values of a predefined attribute.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PredefinedAttributeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Connect::PredefinedAttribute

        :param str resource_name: The name of the resource.
        :param PredefinedAttributeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PredefinedAttributeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 values: Optional[pulumi.Input[Union['ValuesPropertiesArgs', 'ValuesPropertiesArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PredefinedAttributeArgs.__new__(PredefinedAttributeArgs)

            if instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'instance_arn'")
            __props__.__dict__["instance_arn"] = instance_arn
            __props__.__dict__["name"] = name
            if values is None and not opts.urn:
                raise TypeError("Missing required property 'values'")
            __props__.__dict__["values"] = values
            __props__.__dict__["last_modified_region"] = None
            __props__.__dict__["last_modified_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["instanceArn", "name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(PredefinedAttribute, __self__).__init__(
            'aws-native:connect:PredefinedAttribute',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PredefinedAttribute':
        """
        Get an existing PredefinedAttribute resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PredefinedAttributeArgs.__new__(PredefinedAttributeArgs)

        __props__.__dict__["instance_arn"] = None
        __props__.__dict__["last_modified_region"] = None
        __props__.__dict__["last_modified_time"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["values"] = None
        return PredefinedAttribute(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Output[str]:
        """
        The identifier of the Amazon Connect instance.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter(name="lastModifiedRegion")
    def last_modified_region(self) -> pulumi.Output[str]:
        """
        Last modified region.
        """
        return pulumi.get(self, "last_modified_region")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[float]:
        """
        Last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the predefined attribute.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def values(self) -> pulumi.Output['outputs.ValuesProperties']:
        """
        The values of a predefined attribute.
        """
        return pulumi.get(self, "values")

