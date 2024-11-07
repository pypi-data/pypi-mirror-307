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
    'GetAssessmentTargetResult',
    'AwaitableGetAssessmentTargetResult',
    'get_assessment_target',
    'get_assessment_target_output',
]

@pulumi.output_type
class GetAssessmentTargetResult:
    def __init__(__self__, arn=None, resource_group_arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if resource_group_arn and not isinstance(resource_group_arn, str):
            raise TypeError("Expected argument 'resource_group_arn' to be a str")
        pulumi.set(__self__, "resource_group_arn", resource_group_arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) that specifies the assessment target that is created.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="resourceGroupArn")
    def resource_group_arn(self) -> Optional[str]:
        """
        The ARN that specifies the resource group that is used to create the assessment target. If `resourceGroupArn` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.
        """
        return pulumi.get(self, "resource_group_arn")


class AwaitableGetAssessmentTargetResult(GetAssessmentTargetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAssessmentTargetResult(
            arn=self.arn,
            resource_group_arn=self.resource_group_arn)


def get_assessment_target(arn: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAssessmentTargetResult:
    """
    Resource Type definition for AWS::Inspector::AssessmentTarget


    :param str arn: The Amazon Resource Name (ARN) that specifies the assessment target that is created.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:inspector:getAssessmentTarget', __args__, opts=opts, typ=GetAssessmentTargetResult).value

    return AwaitableGetAssessmentTargetResult(
        arn=pulumi.get(__ret__, 'arn'),
        resource_group_arn=pulumi.get(__ret__, 'resource_group_arn'))
def get_assessment_target_output(arn: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAssessmentTargetResult]:
    """
    Resource Type definition for AWS::Inspector::AssessmentTarget


    :param str arn: The Amazon Resource Name (ARN) that specifies the assessment target that is created.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:inspector:getAssessmentTarget', __args__, opts=opts, typ=GetAssessmentTargetResult)
    return __ret__.apply(lambda __response__: GetAssessmentTargetResult(
        arn=pulumi.get(__response__, 'arn'),
        resource_group_arn=pulumi.get(__response__, 'resource_group_arn')))
