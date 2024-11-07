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
    'GetChannelPolicyResult',
    'AwaitableGetChannelPolicyResult',
    'get_channel_policy',
    'get_channel_policy_output',
]

@pulumi.output_type
class GetChannelPolicyResult:
    def __init__(__self__, policy=None):
        if policy and not isinstance(policy, dict):
            raise TypeError("Expected argument 'policy' to be a dict")
        pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter
    def policy(self) -> Optional[Any]:
        """
        <p>The IAM policy for the channel. IAM policies are used to control access to your channel.</p>

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::MediaTailor::ChannelPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy")


class AwaitableGetChannelPolicyResult(GetChannelPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetChannelPolicyResult(
            policy=self.policy)


def get_channel_policy(channel_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetChannelPolicyResult:
    """
    Definition of AWS::MediaTailor::ChannelPolicy Resource Type


    :param str channel_name: The name of the channel associated with this Channel Policy.
    """
    __args__ = dict()
    __args__['channelName'] = channel_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mediatailor:getChannelPolicy', __args__, opts=opts, typ=GetChannelPolicyResult).value

    return AwaitableGetChannelPolicyResult(
        policy=pulumi.get(__ret__, 'policy'))
def get_channel_policy_output(channel_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetChannelPolicyResult]:
    """
    Definition of AWS::MediaTailor::ChannelPolicy Resource Type


    :param str channel_name: The name of the channel associated with this Channel Policy.
    """
    __args__ = dict()
    __args__['channelName'] = channel_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:mediatailor:getChannelPolicy', __args__, opts=opts, typ=GetChannelPolicyResult)
    return __ret__.apply(lambda __response__: GetChannelPolicyResult(
        policy=pulumi.get(__response__, 'policy')))
