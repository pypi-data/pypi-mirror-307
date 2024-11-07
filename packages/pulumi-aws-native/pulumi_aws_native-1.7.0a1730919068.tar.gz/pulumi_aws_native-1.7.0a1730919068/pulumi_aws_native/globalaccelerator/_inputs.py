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
from ._enums import *

__all__ = [
    'CrossAccountAttachmentResourceArgs',
    'CrossAccountAttachmentResourceArgsDict',
    'EndpointGroupEndpointConfigurationArgs',
    'EndpointGroupEndpointConfigurationArgsDict',
    'EndpointGroupPortOverrideArgs',
    'EndpointGroupPortOverrideArgsDict',
    'ListenerPortRangeArgs',
    'ListenerPortRangeArgsDict',
]

MYPY = False

if not MYPY:
    class CrossAccountAttachmentResourceArgsDict(TypedDict):
        """
        ARN of resource to share.
        """
        cidr: NotRequired[pulumi.Input[str]]
        """
        An IP address range, in CIDR format, that is specified as resource. The address must be provisioned and advertised in AWS Global Accelerator by following the bring your own IP address (BYOIP) process for Global Accelerator

        For more information, see [Bring your own IP addresses (BYOIP)](https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html) in the AWS Global Accelerator Developer Guide.
        """
        endpoint_id: NotRequired[pulumi.Input[str]]
        """
        The endpoint ID for the endpoint that is specified as a AWS resource.

        An endpoint ID for the cross-account feature is the ARN of an AWS resource, such as a Network Load Balancer, that Global Accelerator supports as an endpoint for an accelerator.
        """
        region: NotRequired[pulumi.Input[str]]
        """
        The AWS Region where a shared endpoint resource is located.
        """
elif False:
    CrossAccountAttachmentResourceArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CrossAccountAttachmentResourceArgs:
    def __init__(__self__, *,
                 cidr: Optional[pulumi.Input[str]] = None,
                 endpoint_id: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        ARN of resource to share.
        :param pulumi.Input[str] cidr: An IP address range, in CIDR format, that is specified as resource. The address must be provisioned and advertised in AWS Global Accelerator by following the bring your own IP address (BYOIP) process for Global Accelerator
               
               For more information, see [Bring your own IP addresses (BYOIP)](https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html) in the AWS Global Accelerator Developer Guide.
        :param pulumi.Input[str] endpoint_id: The endpoint ID for the endpoint that is specified as a AWS resource.
               
               An endpoint ID for the cross-account feature is the ARN of an AWS resource, such as a Network Load Balancer, that Global Accelerator supports as an endpoint for an accelerator.
        :param pulumi.Input[str] region: The AWS Region where a shared endpoint resource is located.
        """
        if cidr is not None:
            pulumi.set(__self__, "cidr", cidr)
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def cidr(self) -> Optional[pulumi.Input[str]]:
        """
        An IP address range, in CIDR format, that is specified as resource. The address must be provisioned and advertised in AWS Global Accelerator by following the bring your own IP address (BYOIP) process for Global Accelerator

        For more information, see [Bring your own IP addresses (BYOIP)](https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html) in the AWS Global Accelerator Developer Guide.
        """
        return pulumi.get(self, "cidr")

    @cidr.setter
    def cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr", value)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The endpoint ID for the endpoint that is specified as a AWS resource.

        An endpoint ID for the cross-account feature is the ARN of an AWS resource, such as a Network Load Balancer, that Global Accelerator supports as an endpoint for an accelerator.
        """
        return pulumi.get(self, "endpoint_id")

    @endpoint_id.setter
    def endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_id", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS Region where a shared endpoint resource is located.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


if not MYPY:
    class EndpointGroupEndpointConfigurationArgsDict(TypedDict):
        """
        The configuration for a given endpoint
        """
        endpoint_id: pulumi.Input[str]
        """
        Id of the endpoint. For Network/Application Load Balancer this value is the ARN.  For EIP, this value is the allocation ID.  For EC2 instances, this is the EC2 instance ID
        """
        attachment_arn: NotRequired[pulumi.Input[str]]
        """
        Attachment ARN that provides access control to the cross account endpoint. Not required for resources hosted in the same account as the endpoint group.
        """
        client_ip_preservation_enabled: NotRequired[pulumi.Input[bool]]
        """
        true if client ip should be preserved
        """
        weight: NotRequired[pulumi.Input[int]]
        """
        The weight for the endpoint.
        """
elif False:
    EndpointGroupEndpointConfigurationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class EndpointGroupEndpointConfigurationArgs:
    def __init__(__self__, *,
                 endpoint_id: pulumi.Input[str],
                 attachment_arn: Optional[pulumi.Input[str]] = None,
                 client_ip_preservation_enabled: Optional[pulumi.Input[bool]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        The configuration for a given endpoint
        :param pulumi.Input[str] endpoint_id: Id of the endpoint. For Network/Application Load Balancer this value is the ARN.  For EIP, this value is the allocation ID.  For EC2 instances, this is the EC2 instance ID
        :param pulumi.Input[str] attachment_arn: Attachment ARN that provides access control to the cross account endpoint. Not required for resources hosted in the same account as the endpoint group.
        :param pulumi.Input[bool] client_ip_preservation_enabled: true if client ip should be preserved
        :param pulumi.Input[int] weight: The weight for the endpoint.
        """
        pulumi.set(__self__, "endpoint_id", endpoint_id)
        if attachment_arn is not None:
            pulumi.set(__self__, "attachment_arn", attachment_arn)
        if client_ip_preservation_enabled is not None:
            pulumi.set(__self__, "client_ip_preservation_enabled", client_ip_preservation_enabled)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> pulumi.Input[str]:
        """
        Id of the endpoint. For Network/Application Load Balancer this value is the ARN.  For EIP, this value is the allocation ID.  For EC2 instances, this is the EC2 instance ID
        """
        return pulumi.get(self, "endpoint_id")

    @endpoint_id.setter
    def endpoint_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_id", value)

    @property
    @pulumi.getter(name="attachmentArn")
    def attachment_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Attachment ARN that provides access control to the cross account endpoint. Not required for resources hosted in the same account as the endpoint group.
        """
        return pulumi.get(self, "attachment_arn")

    @attachment_arn.setter
    def attachment_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attachment_arn", value)

    @property
    @pulumi.getter(name="clientIpPreservationEnabled")
    def client_ip_preservation_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        true if client ip should be preserved
        """
        return pulumi.get(self, "client_ip_preservation_enabled")

    @client_ip_preservation_enabled.setter
    def client_ip_preservation_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "client_ip_preservation_enabled", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        The weight for the endpoint.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


if not MYPY:
    class EndpointGroupPortOverrideArgsDict(TypedDict):
        """
        listener to endpoint port mapping.
        """
        endpoint_port: pulumi.Input[int]
        """
        The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        """
        listener_port: pulumi.Input[int]
        """
        The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
elif False:
    EndpointGroupPortOverrideArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class EndpointGroupPortOverrideArgs:
    def __init__(__self__, *,
                 endpoint_port: pulumi.Input[int],
                 listener_port: pulumi.Input[int]):
        """
        listener to endpoint port mapping.
        :param pulumi.Input[int] endpoint_port: The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        :param pulumi.Input[int] listener_port: The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
        pulumi.set(__self__, "endpoint_port", endpoint_port)
        pulumi.set(__self__, "listener_port", listener_port)

    @property
    @pulumi.getter(name="endpointPort")
    def endpoint_port(self) -> pulumi.Input[int]:
        """
        The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        """
        return pulumi.get(self, "endpoint_port")

    @endpoint_port.setter
    def endpoint_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "endpoint_port", value)

    @property
    @pulumi.getter(name="listenerPort")
    def listener_port(self) -> pulumi.Input[int]:
        """
        The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        """
        return pulumi.get(self, "listener_port")

    @listener_port.setter
    def listener_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "listener_port", value)


if not MYPY:
    class ListenerPortRangeArgsDict(TypedDict):
        """
        A port range to support for connections from  clients to your accelerator.
        """
        from_port: pulumi.Input[int]
        """
        The first port in the range of ports, inclusive.
        """
        to_port: pulumi.Input[int]
        """
        The last port in the range of ports, inclusive.
        """
elif False:
    ListenerPortRangeArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ListenerPortRangeArgs:
    def __init__(__self__, *,
                 from_port: pulumi.Input[int],
                 to_port: pulumi.Input[int]):
        """
        A port range to support for connections from  clients to your accelerator.
        :param pulumi.Input[int] from_port: The first port in the range of ports, inclusive.
        :param pulumi.Input[int] to_port: The last port in the range of ports, inclusive.
        """
        pulumi.set(__self__, "from_port", from_port)
        pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> pulumi.Input[int]:
        """
        The first port in the range of ports, inclusive.
        """
        return pulumi.get(self, "from_port")

    @from_port.setter
    def from_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "from_port", value)

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> pulumi.Input[int]:
        """
        The last port in the range of ports, inclusive.
        """
        return pulumi.get(self, "to_port")

    @to_port.setter
    def to_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "to_port", value)


