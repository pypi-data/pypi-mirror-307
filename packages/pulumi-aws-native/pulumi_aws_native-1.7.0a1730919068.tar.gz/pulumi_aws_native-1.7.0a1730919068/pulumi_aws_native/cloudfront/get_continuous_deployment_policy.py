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
from ._enums import *

__all__ = [
    'GetContinuousDeploymentPolicyResult',
    'AwaitableGetContinuousDeploymentPolicyResult',
    'get_continuous_deployment_policy',
    'get_continuous_deployment_policy_output',
]

@pulumi.output_type
class GetContinuousDeploymentPolicyResult:
    def __init__(__self__, continuous_deployment_policy_config=None, id=None, last_modified_time=None):
        if continuous_deployment_policy_config and not isinstance(continuous_deployment_policy_config, dict):
            raise TypeError("Expected argument 'continuous_deployment_policy_config' to be a dict")
        pulumi.set(__self__, "continuous_deployment_policy_config", continuous_deployment_policy_config)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)

    @property
    @pulumi.getter(name="continuousDeploymentPolicyConfig")
    def continuous_deployment_policy_config(self) -> Optional['outputs.ContinuousDeploymentPolicyConfig']:
        """
        Contains the configuration for a continuous deployment policy.
        """
        return pulumi.get(self, "continuous_deployment_policy_config")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The identifier of the cotinuous deployment policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[str]:
        """
        The date and time when the continuous deployment policy was last modified.
        """
        return pulumi.get(self, "last_modified_time")


class AwaitableGetContinuousDeploymentPolicyResult(GetContinuousDeploymentPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetContinuousDeploymentPolicyResult(
            continuous_deployment_policy_config=self.continuous_deployment_policy_config,
            id=self.id,
            last_modified_time=self.last_modified_time)


def get_continuous_deployment_policy(id: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetContinuousDeploymentPolicyResult:
    """
    Resource Type definition for AWS::CloudFront::ContinuousDeploymentPolicy


    :param str id: The identifier of the cotinuous deployment policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudfront:getContinuousDeploymentPolicy', __args__, opts=opts, typ=GetContinuousDeploymentPolicyResult).value

    return AwaitableGetContinuousDeploymentPolicyResult(
        continuous_deployment_policy_config=pulumi.get(__ret__, 'continuous_deployment_policy_config'),
        id=pulumi.get(__ret__, 'id'),
        last_modified_time=pulumi.get(__ret__, 'last_modified_time'))
def get_continuous_deployment_policy_output(id: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetContinuousDeploymentPolicyResult]:
    """
    Resource Type definition for AWS::CloudFront::ContinuousDeploymentPolicy


    :param str id: The identifier of the cotinuous deployment policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudfront:getContinuousDeploymentPolicy', __args__, opts=opts, typ=GetContinuousDeploymentPolicyResult)
    return __ret__.apply(lambda __response__: GetContinuousDeploymentPolicyResult(
        continuous_deployment_policy_config=pulumi.get(__response__, 'continuous_deployment_policy_config'),
        id=pulumi.get(__response__, 'id'),
        last_modified_time=pulumi.get(__response__, 'last_modified_time')))
