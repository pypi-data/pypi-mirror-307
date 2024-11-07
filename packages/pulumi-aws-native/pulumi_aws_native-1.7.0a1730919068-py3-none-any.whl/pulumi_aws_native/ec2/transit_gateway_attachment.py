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
from ._inputs import *

__all__ = ['TransitGatewayAttachmentArgs', 'TransitGatewayAttachment']

@pulumi.input_type
class TransitGatewayAttachmentArgs:
    def __init__(__self__, *,
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 transit_gateway_id: pulumi.Input[str],
                 vpc_id: pulumi.Input[str],
                 options: Optional[pulumi.Input['OptionsPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a TransitGatewayAttachment resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The IDs of one or more subnets. You can specify only one subnet per Availability Zone. You must specify at least one subnet, but we recommend that you specify two subnets for better availability. The transit gateway uses one IP address from each specified subnet.
        :param pulumi.Input[str] transit_gateway_id: The ID of the transit gateway.
        :param pulumi.Input[str] vpc_id: The ID of the VPC.
        :param pulumi.Input['OptionsPropertiesArgs'] options: The options for the transit gateway vpc attachment.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags for the attachment.
        """
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The IDs of one or more subnets. You can specify only one subnet per Availability Zone. You must specify at least one subnet, but we recommend that you specify two subnets for better availability. The transit gateway uses one IP address from each specified subnet.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> pulumi.Input[str]:
        """
        The ID of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_gateway_id", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The ID of the VPC.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input['OptionsPropertiesArgs']]:
        """
        The options for the transit gateway vpc attachment.
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input['OptionsPropertiesArgs']]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags for the attachment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class TransitGatewayAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 options: Optional[pulumi.Input[Union['OptionsPropertiesArgs', 'OptionsPropertiesArgsDict']]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::EC2::TransitGatewayAttachment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['OptionsPropertiesArgs', 'OptionsPropertiesArgsDict']] options: The options for the transit gateway vpc attachment.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The IDs of one or more subnets. You can specify only one subnet per Availability Zone. You must specify at least one subnet, but we recommend that you specify two subnets for better availability. The transit gateway uses one IP address from each specified subnet.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags for the attachment.
        :param pulumi.Input[str] transit_gateway_id: The ID of the transit gateway.
        :param pulumi.Input[str] vpc_id: The ID of the VPC.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TransitGatewayAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::EC2::TransitGatewayAttachment

        :param str resource_name: The name of the resource.
        :param TransitGatewayAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TransitGatewayAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 options: Optional[pulumi.Input[Union['OptionsPropertiesArgs', 'OptionsPropertiesArgsDict']]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TransitGatewayAttachmentArgs.__new__(TransitGatewayAttachmentArgs)

            __props__.__dict__["options"] = options
            if subnet_ids is None and not opts.urn:
                raise TypeError("Missing required property 'subnet_ids'")
            __props__.__dict__["subnet_ids"] = subnet_ids
            __props__.__dict__["tags"] = tags
            if transit_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'transit_gateway_id'")
            __props__.__dict__["transit_gateway_id"] = transit_gateway_id
            if vpc_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_id'")
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["aws_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["transitGatewayId", "vpcId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TransitGatewayAttachment, __self__).__init__(
            'aws-native:ec2:TransitGatewayAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TransitGatewayAttachment':
        """
        Get an existing TransitGatewayAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TransitGatewayAttachmentArgs.__new__(TransitGatewayAttachmentArgs)

        __props__.__dict__["aws_id"] = None
        __props__.__dict__["options"] = None
        __props__.__dict__["subnet_ids"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["transit_gateway_id"] = None
        __props__.__dict__["vpc_id"] = None
        return TransitGatewayAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The ID of the attachment.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional['outputs.OptionsProperties']]:
        """
        The options for the transit gateway vpc attachment.
        """
        return pulumi.get(self, "options")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        The IDs of one or more subnets. You can specify only one subnet per Availability Zone. You must specify at least one subnet, but we recommend that you specify two subnets for better availability. The transit gateway uses one IP address from each specified subnet.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags for the attachment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the VPC.
        """
        return pulumi.get(self, "vpc_id")

