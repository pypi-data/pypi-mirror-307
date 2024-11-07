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

__all__ = [
    'GetDestinationResult',
    'AwaitableGetDestinationResult',
    'get_destination',
    'get_destination_output',
]

@pulumi.output_type
class GetDestinationResult:
    def __init__(__self__, arn=None, destination_policy=None, role_arn=None, target_arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if destination_policy and not isinstance(destination_policy, str):
            raise TypeError("Expected argument 'destination_policy' to be a str")
        pulumi.set(__self__, "destination_policy", destination_policy)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if target_arn and not isinstance(target_arn, str):
            raise TypeError("Expected argument 'target_arn' to be a str")
        pulumi.set(__self__, "target_arn", target_arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the CloudWatch Logs destination, such as `arn:aws:logs:us-west-1:123456789012:destination:MyDestination` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="destinationPolicy")
    def destination_policy(self) -> Optional[str]:
        """
        An IAM policy document that governs which AWS accounts can create subscription filters against this destination.
        """
        return pulumi.get(self, "destination_policy")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="targetArn")
    def target_arn(self) -> Optional[str]:
        """
        The ARN of the physical target where the log events are delivered (for example, a Kinesis stream)
        """
        return pulumi.get(self, "target_arn")


class AwaitableGetDestinationResult(GetDestinationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDestinationResult(
            arn=self.arn,
            destination_policy=self.destination_policy,
            role_arn=self.role_arn,
            target_arn=self.target_arn)


def get_destination(destination_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDestinationResult:
    """
    The AWS::Logs::Destination resource specifies a CloudWatch Logs destination. A destination encapsulates a physical resource (such as an Amazon Kinesis data stream) and enables you to subscribe that resource to a stream of log events.


    :param str destination_name: The name of the destination resource
    """
    __args__ = dict()
    __args__['destinationName'] = destination_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:logs:getDestination', __args__, opts=opts, typ=GetDestinationResult).value

    return AwaitableGetDestinationResult(
        arn=pulumi.get(__ret__, 'arn'),
        destination_policy=pulumi.get(__ret__, 'destination_policy'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        target_arn=pulumi.get(__ret__, 'target_arn'))
def get_destination_output(destination_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDestinationResult]:
    """
    The AWS::Logs::Destination resource specifies a CloudWatch Logs destination. A destination encapsulates a physical resource (such as an Amazon Kinesis data stream) and enables you to subscribe that resource to a stream of log events.


    :param str destination_name: The name of the destination resource
    """
    __args__ = dict()
    __args__['destinationName'] = destination_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:logs:getDestination', __args__, opts=opts, typ=GetDestinationResult)
    return __ret__.apply(lambda __response__: GetDestinationResult(
        arn=pulumi.get(__response__, 'arn'),
        destination_policy=pulumi.get(__response__, 'destination_policy'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        target_arn=pulumi.get(__response__, 'target_arn')))
