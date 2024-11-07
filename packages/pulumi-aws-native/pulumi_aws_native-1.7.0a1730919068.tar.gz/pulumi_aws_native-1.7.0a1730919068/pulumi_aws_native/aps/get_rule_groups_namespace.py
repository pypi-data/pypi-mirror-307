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
    'GetRuleGroupsNamespaceResult',
    'AwaitableGetRuleGroupsNamespaceResult',
    'get_rule_groups_namespace',
    'get_rule_groups_namespace_output',
]

@pulumi.output_type
class GetRuleGroupsNamespaceResult:
    def __init__(__self__, arn=None, data=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if data and not isinstance(data, str):
            raise TypeError("Expected argument 'data' to be a str")
        pulumi.set(__self__, "data", data)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The RuleGroupsNamespace ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def data(self) -> Optional[str]:
        """
        The RuleGroupsNamespace data.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRuleGroupsNamespaceResult(GetRuleGroupsNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRuleGroupsNamespaceResult(
            arn=self.arn,
            data=self.data,
            tags=self.tags)


def get_rule_groups_namespace(arn: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRuleGroupsNamespaceResult:
    """
    RuleGroupsNamespace schema for cloudformation.


    :param str arn: The RuleGroupsNamespace ARN.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:aps:getRuleGroupsNamespace', __args__, opts=opts, typ=GetRuleGroupsNamespaceResult).value

    return AwaitableGetRuleGroupsNamespaceResult(
        arn=pulumi.get(__ret__, 'arn'),
        data=pulumi.get(__ret__, 'data'),
        tags=pulumi.get(__ret__, 'tags'))
def get_rule_groups_namespace_output(arn: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRuleGroupsNamespaceResult]:
    """
    RuleGroupsNamespace schema for cloudformation.


    :param str arn: The RuleGroupsNamespace ARN.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:aps:getRuleGroupsNamespace', __args__, opts=opts, typ=GetRuleGroupsNamespaceResult)
    return __ret__.apply(lambda __response__: GetRuleGroupsNamespaceResult(
        arn=pulumi.get(__response__, 'arn'),
        data=pulumi.get(__response__, 'data'),
        tags=pulumi.get(__response__, 'tags')))
