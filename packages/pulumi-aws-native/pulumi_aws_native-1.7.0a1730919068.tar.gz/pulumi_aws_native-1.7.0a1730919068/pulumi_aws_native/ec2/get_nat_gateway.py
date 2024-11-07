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
    'GetNatGatewayResult',
    'AwaitableGetNatGatewayResult',
    'get_nat_gateway',
    'get_nat_gateway_output',
]

@pulumi.output_type
class GetNatGatewayResult:
    def __init__(__self__, nat_gateway_id=None, secondary_allocation_ids=None, secondary_private_ip_address_count=None, secondary_private_ip_addresses=None, tags=None):
        if nat_gateway_id and not isinstance(nat_gateway_id, str):
            raise TypeError("Expected argument 'nat_gateway_id' to be a str")
        pulumi.set(__self__, "nat_gateway_id", nat_gateway_id)
        if secondary_allocation_ids and not isinstance(secondary_allocation_ids, list):
            raise TypeError("Expected argument 'secondary_allocation_ids' to be a list")
        pulumi.set(__self__, "secondary_allocation_ids", secondary_allocation_ids)
        if secondary_private_ip_address_count and not isinstance(secondary_private_ip_address_count, int):
            raise TypeError("Expected argument 'secondary_private_ip_address_count' to be a int")
        pulumi.set(__self__, "secondary_private_ip_address_count", secondary_private_ip_address_count)
        if secondary_private_ip_addresses and not isinstance(secondary_private_ip_addresses, list):
            raise TypeError("Expected argument 'secondary_private_ip_addresses' to be a list")
        pulumi.set(__self__, "secondary_private_ip_addresses", secondary_private_ip_addresses)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="natGatewayId")
    def nat_gateway_id(self) -> Optional[str]:
        """
        The ID of the NAT gateway.
        """
        return pulumi.get(self, "nat_gateway_id")

    @property
    @pulumi.getter(name="secondaryAllocationIds")
    def secondary_allocation_ids(self) -> Optional[Sequence[str]]:
        """
        Secondary EIP allocation IDs. For more information, see [Create a NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-working-with.html) in the *Amazon VPC User Guide*.
        """
        return pulumi.get(self, "secondary_allocation_ids")

    @property
    @pulumi.getter(name="secondaryPrivateIpAddressCount")
    def secondary_private_ip_address_count(self) -> Optional[int]:
        """
        [Private NAT gateway only] The number of secondary private IPv4 addresses you want to assign to the NAT gateway. For more information about secondary addresses, see [Create a NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-creating) in the *Amazon Virtual Private Cloud User Guide*.
          ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be set at the same time.
        """
        return pulumi.get(self, "secondary_private_ip_address_count")

    @property
    @pulumi.getter(name="secondaryPrivateIpAddresses")
    def secondary_private_ip_addresses(self) -> Optional[Sequence[str]]:
        """
        Secondary private IPv4 addresses. For more information about secondary addresses, see [Create a NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html#nat-gateway-creating) in the *Amazon Virtual Private Cloud User Guide*.
          ``SecondaryPrivateIpAddressCount`` and ``SecondaryPrivateIpAddresses`` cannot be set at the same time.
        """
        return pulumi.get(self, "secondary_private_ip_addresses")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the NAT gateway.
        """
        return pulumi.get(self, "tags")


class AwaitableGetNatGatewayResult(GetNatGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNatGatewayResult(
            nat_gateway_id=self.nat_gateway_id,
            secondary_allocation_ids=self.secondary_allocation_ids,
            secondary_private_ip_address_count=self.secondary_private_ip_address_count,
            secondary_private_ip_addresses=self.secondary_private_ip_addresses,
            tags=self.tags)


def get_nat_gateway(nat_gateway_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNatGatewayResult:
    """
    Specifies a network address translation (NAT) gateway in the specified subnet. You can create either a public NAT gateway or a private NAT gateway. The default is a public NAT gateway. If you create a public NAT gateway, you must specify an elastic IP address.
     With a NAT gateway, instances in a private subnet can connect to the internet, other AWS services, or an on-premises network using the IP address of the NAT gateway. For more information, see [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) in the *Amazon VPC User Guide*.
     If you add a default route (``AWS::EC2::Route`` resource) that points to a NAT gateway, specify the NAT gateway ID for the route's ``NatGatewayId`` property.
      When you associate an Elastic IP address or secondary Elastic IP address with a public NAT gateway, the network border group of the Elastic IP address must match the network border group of the Availability Zone (AZ) that the public NAT gateway is in. Otherwise, the NAT gateway fails to launch. You can see the network border group for the AZ by viewing the details of the subnet. Similarly, you can view the network border group for the Elastic IP address by viewing its details. For more information, see [Allocate an Elastic IP address](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html#allocate-eip) in the *Amazon VPC User Guide*.


    :param str nat_gateway_id: The ID of the NAT gateway.
    """
    __args__ = dict()
    __args__['natGatewayId'] = nat_gateway_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getNatGateway', __args__, opts=opts, typ=GetNatGatewayResult).value

    return AwaitableGetNatGatewayResult(
        nat_gateway_id=pulumi.get(__ret__, 'nat_gateway_id'),
        secondary_allocation_ids=pulumi.get(__ret__, 'secondary_allocation_ids'),
        secondary_private_ip_address_count=pulumi.get(__ret__, 'secondary_private_ip_address_count'),
        secondary_private_ip_addresses=pulumi.get(__ret__, 'secondary_private_ip_addresses'),
        tags=pulumi.get(__ret__, 'tags'))
def get_nat_gateway_output(nat_gateway_id: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNatGatewayResult]:
    """
    Specifies a network address translation (NAT) gateway in the specified subnet. You can create either a public NAT gateway or a private NAT gateway. The default is a public NAT gateway. If you create a public NAT gateway, you must specify an elastic IP address.
     With a NAT gateway, instances in a private subnet can connect to the internet, other AWS services, or an on-premises network using the IP address of the NAT gateway. For more information, see [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) in the *Amazon VPC User Guide*.
     If you add a default route (``AWS::EC2::Route`` resource) that points to a NAT gateway, specify the NAT gateway ID for the route's ``NatGatewayId`` property.
      When you associate an Elastic IP address or secondary Elastic IP address with a public NAT gateway, the network border group of the Elastic IP address must match the network border group of the Availability Zone (AZ) that the public NAT gateway is in. Otherwise, the NAT gateway fails to launch. You can see the network border group for the AZ by viewing the details of the subnet. Similarly, you can view the network border group for the Elastic IP address by viewing its details. For more information, see [Allocate an Elastic IP address](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html#allocate-eip) in the *Amazon VPC User Guide*.


    :param str nat_gateway_id: The ID of the NAT gateway.
    """
    __args__ = dict()
    __args__['natGatewayId'] = nat_gateway_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getNatGateway', __args__, opts=opts, typ=GetNatGatewayResult)
    return __ret__.apply(lambda __response__: GetNatGatewayResult(
        nat_gateway_id=pulumi.get(__response__, 'nat_gateway_id'),
        secondary_allocation_ids=pulumi.get(__response__, 'secondary_allocation_ids'),
        secondary_private_ip_address_count=pulumi.get(__response__, 'secondary_private_ip_address_count'),
        secondary_private_ip_addresses=pulumi.get(__response__, 'secondary_private_ip_addresses'),
        tags=pulumi.get(__response__, 'tags')))
