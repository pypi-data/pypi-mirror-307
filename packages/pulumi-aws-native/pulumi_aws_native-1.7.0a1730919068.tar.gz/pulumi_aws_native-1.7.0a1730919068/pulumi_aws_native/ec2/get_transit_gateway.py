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
from .. import outputs as _root_outputs

__all__ = [
    'GetTransitGatewayResult',
    'AwaitableGetTransitGatewayResult',
    'get_transit_gateway',
    'get_transit_gateway_output',
]

@pulumi.output_type
class GetTransitGatewayResult:
    def __init__(__self__, association_default_route_table_id=None, auto_accept_shared_attachments=None, default_route_table_association=None, default_route_table_propagation=None, description=None, dns_support=None, id=None, propagation_default_route_table_id=None, security_group_referencing_support=None, tags=None, transit_gateway_arn=None, transit_gateway_cidr_blocks=None, vpn_ecmp_support=None):
        if association_default_route_table_id and not isinstance(association_default_route_table_id, str):
            raise TypeError("Expected argument 'association_default_route_table_id' to be a str")
        pulumi.set(__self__, "association_default_route_table_id", association_default_route_table_id)
        if auto_accept_shared_attachments and not isinstance(auto_accept_shared_attachments, str):
            raise TypeError("Expected argument 'auto_accept_shared_attachments' to be a str")
        pulumi.set(__self__, "auto_accept_shared_attachments", auto_accept_shared_attachments)
        if default_route_table_association and not isinstance(default_route_table_association, str):
            raise TypeError("Expected argument 'default_route_table_association' to be a str")
        pulumi.set(__self__, "default_route_table_association", default_route_table_association)
        if default_route_table_propagation and not isinstance(default_route_table_propagation, str):
            raise TypeError("Expected argument 'default_route_table_propagation' to be a str")
        pulumi.set(__self__, "default_route_table_propagation", default_route_table_propagation)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if dns_support and not isinstance(dns_support, str):
            raise TypeError("Expected argument 'dns_support' to be a str")
        pulumi.set(__self__, "dns_support", dns_support)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if propagation_default_route_table_id and not isinstance(propagation_default_route_table_id, str):
            raise TypeError("Expected argument 'propagation_default_route_table_id' to be a str")
        pulumi.set(__self__, "propagation_default_route_table_id", propagation_default_route_table_id)
        if security_group_referencing_support and not isinstance(security_group_referencing_support, str):
            raise TypeError("Expected argument 'security_group_referencing_support' to be a str")
        pulumi.set(__self__, "security_group_referencing_support", security_group_referencing_support)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if transit_gateway_arn and not isinstance(transit_gateway_arn, str):
            raise TypeError("Expected argument 'transit_gateway_arn' to be a str")
        pulumi.set(__self__, "transit_gateway_arn", transit_gateway_arn)
        if transit_gateway_cidr_blocks and not isinstance(transit_gateway_cidr_blocks, list):
            raise TypeError("Expected argument 'transit_gateway_cidr_blocks' to be a list")
        pulumi.set(__self__, "transit_gateway_cidr_blocks", transit_gateway_cidr_blocks)
        if vpn_ecmp_support and not isinstance(vpn_ecmp_support, str):
            raise TypeError("Expected argument 'vpn_ecmp_support' to be a str")
        pulumi.set(__self__, "vpn_ecmp_support", vpn_ecmp_support)

    @property
    @pulumi.getter(name="associationDefaultRouteTableId")
    def association_default_route_table_id(self) -> Optional[str]:
        """
        The ID of the default association route table.
        """
        return pulumi.get(self, "association_default_route_table_id")

    @property
    @pulumi.getter(name="autoAcceptSharedAttachments")
    def auto_accept_shared_attachments(self) -> Optional[str]:
        """
        Enable or disable automatic acceptance of attachment requests. Disabled by default.
        """
        return pulumi.get(self, "auto_accept_shared_attachments")

    @property
    @pulumi.getter(name="defaultRouteTableAssociation")
    def default_route_table_association(self) -> Optional[str]:
        """
        Enable or disable automatic association with the default association route table. Enabled by default.
        """
        return pulumi.get(self, "default_route_table_association")

    @property
    @pulumi.getter(name="defaultRouteTablePropagation")
    def default_route_table_propagation(self) -> Optional[str]:
        """
        Enable or disable automatic propagation of routes to the default propagation route table. Enabled by default.
        """
        return pulumi.get(self, "default_route_table_propagation")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the transit gateway.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dnsSupport")
    def dns_support(self) -> Optional[str]:
        """
        Enable or disable DNS support. Enabled by default.
        """
        return pulumi.get(self, "dns_support")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the transit gateway.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="propagationDefaultRouteTableId")
    def propagation_default_route_table_id(self) -> Optional[str]:
        """
        The ID of the default propagation route table.
        """
        return pulumi.get(self, "propagation_default_route_table_id")

    @property
    @pulumi.getter(name="securityGroupReferencingSupport")
    def security_group_referencing_support(self) -> Optional[str]:
        """
        Enables you to reference a security group across VPCs attached to a transit gateway (TGW). Use this option to simplify security group management and control of instance-to-instance traffic across VPCs that are connected by transit gateway. You can also use this option to migrate from VPC peering (which was the only option that supported security group referencing) to transit gateways (which now also support security group referencing). This option is disabled by default and there are no additional costs to use this feature.

        For important information about this feature, see [Create a transit gateway](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-transit-gateways.html#create-tgw) in the *AWS Transit Gateway Guide* .
        """
        return pulumi.get(self, "security_group_referencing_support")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the transit gateway.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayArn")
    def transit_gateway_arn(self) -> Optional[str]:
        return pulumi.get(self, "transit_gateway_arn")

    @property
    @pulumi.getter(name="transitGatewayCidrBlocks")
    def transit_gateway_cidr_blocks(self) -> Optional[Sequence[str]]:
        """
        The transit gateway CIDR blocks.
        """
        return pulumi.get(self, "transit_gateway_cidr_blocks")

    @property
    @pulumi.getter(name="vpnEcmpSupport")
    def vpn_ecmp_support(self) -> Optional[str]:
        """
        Enable or disable Equal Cost Multipath Protocol support. Enabled by default.
        """
        return pulumi.get(self, "vpn_ecmp_support")


class AwaitableGetTransitGatewayResult(GetTransitGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayResult(
            association_default_route_table_id=self.association_default_route_table_id,
            auto_accept_shared_attachments=self.auto_accept_shared_attachments,
            default_route_table_association=self.default_route_table_association,
            default_route_table_propagation=self.default_route_table_propagation,
            description=self.description,
            dns_support=self.dns_support,
            id=self.id,
            propagation_default_route_table_id=self.propagation_default_route_table_id,
            security_group_referencing_support=self.security_group_referencing_support,
            tags=self.tags,
            transit_gateway_arn=self.transit_gateway_arn,
            transit_gateway_cidr_blocks=self.transit_gateway_cidr_blocks,
            vpn_ecmp_support=self.vpn_ecmp_support)


def get_transit_gateway(id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayResult:
    """
    Resource Type definition for AWS::EC2::TransitGateway


    :param str id: The ID of the transit gateway.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getTransitGateway', __args__, opts=opts, typ=GetTransitGatewayResult).value

    return AwaitableGetTransitGatewayResult(
        association_default_route_table_id=pulumi.get(__ret__, 'association_default_route_table_id'),
        auto_accept_shared_attachments=pulumi.get(__ret__, 'auto_accept_shared_attachments'),
        default_route_table_association=pulumi.get(__ret__, 'default_route_table_association'),
        default_route_table_propagation=pulumi.get(__ret__, 'default_route_table_propagation'),
        description=pulumi.get(__ret__, 'description'),
        dns_support=pulumi.get(__ret__, 'dns_support'),
        id=pulumi.get(__ret__, 'id'),
        propagation_default_route_table_id=pulumi.get(__ret__, 'propagation_default_route_table_id'),
        security_group_referencing_support=pulumi.get(__ret__, 'security_group_referencing_support'),
        tags=pulumi.get(__ret__, 'tags'),
        transit_gateway_arn=pulumi.get(__ret__, 'transit_gateway_arn'),
        transit_gateway_cidr_blocks=pulumi.get(__ret__, 'transit_gateway_cidr_blocks'),
        vpn_ecmp_support=pulumi.get(__ret__, 'vpn_ecmp_support'))
def get_transit_gateway_output(id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayResult]:
    """
    Resource Type definition for AWS::EC2::TransitGateway


    :param str id: The ID of the transit gateway.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getTransitGateway', __args__, opts=opts, typ=GetTransitGatewayResult)
    return __ret__.apply(lambda __response__: GetTransitGatewayResult(
        association_default_route_table_id=pulumi.get(__response__, 'association_default_route_table_id'),
        auto_accept_shared_attachments=pulumi.get(__response__, 'auto_accept_shared_attachments'),
        default_route_table_association=pulumi.get(__response__, 'default_route_table_association'),
        default_route_table_propagation=pulumi.get(__response__, 'default_route_table_propagation'),
        description=pulumi.get(__response__, 'description'),
        dns_support=pulumi.get(__response__, 'dns_support'),
        id=pulumi.get(__response__, 'id'),
        propagation_default_route_table_id=pulumi.get(__response__, 'propagation_default_route_table_id'),
        security_group_referencing_support=pulumi.get(__response__, 'security_group_referencing_support'),
        tags=pulumi.get(__response__, 'tags'),
        transit_gateway_arn=pulumi.get(__response__, 'transit_gateway_arn'),
        transit_gateway_cidr_blocks=pulumi.get(__response__, 'transit_gateway_cidr_blocks'),
        vpn_ecmp_support=pulumi.get(__response__, 'vpn_ecmp_support')))
