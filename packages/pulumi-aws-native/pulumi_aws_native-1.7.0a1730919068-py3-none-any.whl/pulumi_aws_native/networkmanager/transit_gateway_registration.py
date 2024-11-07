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

__all__ = ['TransitGatewayRegistrationArgs', 'TransitGatewayRegistration']

@pulumi.input_type
class TransitGatewayRegistrationArgs:
    def __init__(__self__, *,
                 global_network_id: pulumi.Input[str],
                 transit_gateway_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a TransitGatewayRegistration resource.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] transit_gateway_arn: The Amazon Resource Name (ARN) of the transit gateway.
        """
        pulumi.set(__self__, "global_network_id", global_network_id)
        pulumi.set(__self__, "transit_gateway_arn", transit_gateway_arn)

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> pulumi.Input[str]:
        """
        The ID of the global network.
        """
        return pulumi.get(self, "global_network_id")

    @global_network_id.setter
    def global_network_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "global_network_id", value)

    @property
    @pulumi.getter(name="transitGatewayArn")
    def transit_gateway_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_arn")

    @transit_gateway_arn.setter
    def transit_gateway_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_gateway_arn", value)


class TransitGatewayRegistration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The AWS::NetworkManager::TransitGatewayRegistration type registers a transit gateway in your global network. The transit gateway can be in any AWS Region, but it must be owned by the same AWS account that owns the global network. You cannot register a transit gateway in more than one global network.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] transit_gateway_arn: The Amazon Resource Name (ARN) of the transit gateway.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TransitGatewayRegistrationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::NetworkManager::TransitGatewayRegistration type registers a transit gateway in your global network. The transit gateway can be in any AWS Region, but it must be owned by the same AWS account that owns the global network. You cannot register a transit gateway in more than one global network.

        :param str resource_name: The name of the resource.
        :param TransitGatewayRegistrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TransitGatewayRegistrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TransitGatewayRegistrationArgs.__new__(TransitGatewayRegistrationArgs)

            if global_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'global_network_id'")
            __props__.__dict__["global_network_id"] = global_network_id
            if transit_gateway_arn is None and not opts.urn:
                raise TypeError("Missing required property 'transit_gateway_arn'")
            __props__.__dict__["transit_gateway_arn"] = transit_gateway_arn
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["globalNetworkId", "transitGatewayArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(TransitGatewayRegistration, __self__).__init__(
            'aws-native:networkmanager:TransitGatewayRegistration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TransitGatewayRegistration':
        """
        Get an existing TransitGatewayRegistration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TransitGatewayRegistrationArgs.__new__(TransitGatewayRegistrationArgs)

        __props__.__dict__["global_network_id"] = None
        __props__.__dict__["transit_gateway_arn"] = None
        return TransitGatewayRegistration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> pulumi.Output[str]:
        """
        The ID of the global network.
        """
        return pulumi.get(self, "global_network_id")

    @property
    @pulumi.getter(name="transitGatewayArn")
    def transit_gateway_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_arn")

