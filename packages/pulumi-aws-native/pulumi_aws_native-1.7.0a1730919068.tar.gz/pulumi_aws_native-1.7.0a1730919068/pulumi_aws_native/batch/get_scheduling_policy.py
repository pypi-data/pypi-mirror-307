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

__all__ = [
    'GetSchedulingPolicyResult',
    'AwaitableGetSchedulingPolicyResult',
    'get_scheduling_policy',
    'get_scheduling_policy_output',
]

@pulumi.output_type
class GetSchedulingPolicyResult:
    def __init__(__self__, arn=None, fairshare_policy=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if fairshare_policy and not isinstance(fairshare_policy, dict):
            raise TypeError("Expected argument 'fairshare_policy' to be a dict")
        pulumi.set(__self__, "fairshare_policy", fairshare_policy)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Returns the scheduling policy ARN, such as `batch: *us-east-1* : *111122223333* :scheduling-policy/ *HighPriority*` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="fairsharePolicy")
    def fairshare_policy(self) -> Optional['outputs.SchedulingPolicyFairsharePolicy']:
        """
        The fair share policy of the scheduling policy.
        """
        return pulumi.get(self, "fairshare_policy")


class AwaitableGetSchedulingPolicyResult(GetSchedulingPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSchedulingPolicyResult(
            arn=self.arn,
            fairshare_policy=self.fairshare_policy)


def get_scheduling_policy(arn: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSchedulingPolicyResult:
    """
    Resource Type schema for AWS::Batch::SchedulingPolicy


    :param str arn: Returns the scheduling policy ARN, such as `batch: *us-east-1* : *111122223333* :scheduling-policy/ *HighPriority*` .
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:batch:getSchedulingPolicy', __args__, opts=opts, typ=GetSchedulingPolicyResult).value

    return AwaitableGetSchedulingPolicyResult(
        arn=pulumi.get(__ret__, 'arn'),
        fairshare_policy=pulumi.get(__ret__, 'fairshare_policy'))
def get_scheduling_policy_output(arn: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSchedulingPolicyResult]:
    """
    Resource Type schema for AWS::Batch::SchedulingPolicy


    :param str arn: Returns the scheduling policy ARN, such as `batch: *us-east-1* : *111122223333* :scheduling-policy/ *HighPriority*` .
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:batch:getSchedulingPolicy', __args__, opts=opts, typ=GetSchedulingPolicyResult)
    return __ret__.apply(lambda __response__: GetSchedulingPolicyResult(
        arn=pulumi.get(__response__, 'arn'),
        fairshare_policy=pulumi.get(__response__, 'fairshare_policy')))
