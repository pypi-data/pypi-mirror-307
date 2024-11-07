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
    'GetProtectionResult',
    'AwaitableGetProtectionResult',
    'get_protection',
    'get_protection_output',
]

@pulumi.output_type
class GetProtectionResult:
    def __init__(__self__, application_layer_automatic_response_configuration=None, health_check_arns=None, protection_arn=None, protection_id=None, tags=None):
        if application_layer_automatic_response_configuration and not isinstance(application_layer_automatic_response_configuration, dict):
            raise TypeError("Expected argument 'application_layer_automatic_response_configuration' to be a dict")
        pulumi.set(__self__, "application_layer_automatic_response_configuration", application_layer_automatic_response_configuration)
        if health_check_arns and not isinstance(health_check_arns, list):
            raise TypeError("Expected argument 'health_check_arns' to be a list")
        pulumi.set(__self__, "health_check_arns", health_check_arns)
        if protection_arn and not isinstance(protection_arn, str):
            raise TypeError("Expected argument 'protection_arn' to be a str")
        pulumi.set(__self__, "protection_arn", protection_arn)
        if protection_id and not isinstance(protection_id, str):
            raise TypeError("Expected argument 'protection_id' to be a str")
        pulumi.set(__self__, "protection_id", protection_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="applicationLayerAutomaticResponseConfiguration")
    def application_layer_automatic_response_configuration(self) -> Optional['outputs.ProtectionApplicationLayerAutomaticResponseConfiguration']:
        """
        The automatic application layer DDoS mitigation settings for the protection. This configuration determines whether Shield Advanced automatically manages rules in the web ACL in order to respond to application layer events that Shield Advanced determines to be DDoS attacks.

        If you use AWS CloudFormation to manage the web ACLs that you use with Shield Advanced automatic mitigation, see the additional guidance about web ACL management in the `AWS::WAFv2::WebACL` resource description.
        """
        return pulumi.get(self, "application_layer_automatic_response_configuration")

    @property
    @pulumi.getter(name="healthCheckArns")
    def health_check_arns(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the health check to associate with the protection.
        """
        return pulumi.get(self, "health_check_arns")

    @property
    @pulumi.getter(name="protectionArn")
    def protection_arn(self) -> Optional[str]:
        """
        The ARN (Amazon Resource Name) of the protection.
        """
        return pulumi.get(self, "protection_arn")

    @property
    @pulumi.getter(name="protectionId")
    def protection_id(self) -> Optional[str]:
        """
        The unique identifier (ID) of the protection.
        """
        return pulumi.get(self, "protection_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        One or more tag key-value pairs for the Protection object.
        """
        return pulumi.get(self, "tags")


class AwaitableGetProtectionResult(GetProtectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProtectionResult(
            application_layer_automatic_response_configuration=self.application_layer_automatic_response_configuration,
            health_check_arns=self.health_check_arns,
            protection_arn=self.protection_arn,
            protection_id=self.protection_id,
            tags=self.tags)


def get_protection(protection_arn: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProtectionResult:
    """
    Enables AWS Shield Advanced for a specific AWS resource. The resource can be an Amazon CloudFront distribution, Amazon Route 53 hosted zone, AWS Global Accelerator standard accelerator, Elastic IP Address, Application Load Balancer, or a Classic Load Balancer. You can protect Amazon EC2 instances and Network Load Balancers by association with protected Amazon EC2 Elastic IP addresses.


    :param str protection_arn: The ARN (Amazon Resource Name) of the protection.
    """
    __args__ = dict()
    __args__['protectionArn'] = protection_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:shield:getProtection', __args__, opts=opts, typ=GetProtectionResult).value

    return AwaitableGetProtectionResult(
        application_layer_automatic_response_configuration=pulumi.get(__ret__, 'application_layer_automatic_response_configuration'),
        health_check_arns=pulumi.get(__ret__, 'health_check_arns'),
        protection_arn=pulumi.get(__ret__, 'protection_arn'),
        protection_id=pulumi.get(__ret__, 'protection_id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_protection_output(protection_arn: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProtectionResult]:
    """
    Enables AWS Shield Advanced for a specific AWS resource. The resource can be an Amazon CloudFront distribution, Amazon Route 53 hosted zone, AWS Global Accelerator standard accelerator, Elastic IP Address, Application Load Balancer, or a Classic Load Balancer. You can protect Amazon EC2 instances and Network Load Balancers by association with protected Amazon EC2 Elastic IP addresses.


    :param str protection_arn: The ARN (Amazon Resource Name) of the protection.
    """
    __args__ = dict()
    __args__['protectionArn'] = protection_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:shield:getProtection', __args__, opts=opts, typ=GetProtectionResult)
    return __ret__.apply(lambda __response__: GetProtectionResult(
        application_layer_automatic_response_configuration=pulumi.get(__response__, 'application_layer_automatic_response_configuration'),
        health_check_arns=pulumi.get(__response__, 'health_check_arns'),
        protection_arn=pulumi.get(__response__, 'protection_arn'),
        protection_id=pulumi.get(__response__, 'protection_id'),
        tags=pulumi.get(__response__, 'tags')))
