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
    'GetPolicyResult',
    'AwaitableGetPolicyResult',
    'get_policy',
    'get_policy_output',
]

@pulumi.output_type
class GetPolicyResult:
    def __init__(__self__, arn=None, id=None, policy_document=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_document and not isinstance(policy_document, dict):
            raise TypeError("Expected argument 'policy_document' to be a dict")
        pulumi.set(__self__, "policy_document", policy_document)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the AWS IoT policy, such as `arn:aws:iot:us-east-2:123456789012:policy/MyPolicy` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The name of this policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[Any]:
        """
        The JSON document that describes the policy.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::IoT::Policy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_document")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        return pulumi.get(self, "tags")


class AwaitableGetPolicyResult(GetPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyResult(
            arn=self.arn,
            id=self.id,
            policy_document=self.policy_document,
            tags=self.tags)


def get_policy(id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyResult:
    """
    Resource Type definition for AWS::IoT::Policy


    :param str id: The name of this policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iot:getPolicy', __args__, opts=opts, typ=GetPolicyResult).value

    return AwaitableGetPolicyResult(
        arn=pulumi.get(__ret__, 'arn'),
        id=pulumi.get(__ret__, 'id'),
        policy_document=pulumi.get(__ret__, 'policy_document'),
        tags=pulumi.get(__ret__, 'tags'))
def get_policy_output(id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyResult]:
    """
    Resource Type definition for AWS::IoT::Policy


    :param str id: The name of this policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iot:getPolicy', __args__, opts=opts, typ=GetPolicyResult)
    return __ret__.apply(lambda __response__: GetPolicyResult(
        arn=pulumi.get(__response__, 'arn'),
        id=pulumi.get(__response__, 'id'),
        policy_document=pulumi.get(__response__, 'policy_document'),
        tags=pulumi.get(__response__, 'tags')))
