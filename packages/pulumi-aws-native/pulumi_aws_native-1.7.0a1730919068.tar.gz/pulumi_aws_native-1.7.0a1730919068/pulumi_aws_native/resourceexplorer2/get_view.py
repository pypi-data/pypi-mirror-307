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
    'GetViewResult',
    'AwaitableGetViewResult',
    'get_view',
    'get_view_output',
]

@pulumi.output_type
class GetViewResult:
    def __init__(__self__, filters=None, included_properties=None, tags=None, view_arn=None):
        if filters and not isinstance(filters, dict):
            raise TypeError("Expected argument 'filters' to be a dict")
        pulumi.set(__self__, "filters", filters)
        if included_properties and not isinstance(included_properties, list):
            raise TypeError("Expected argument 'included_properties' to be a list")
        pulumi.set(__self__, "included_properties", included_properties)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if view_arn and not isinstance(view_arn, str):
            raise TypeError("Expected argument 'view_arn' to be a str")
        pulumi.set(__self__, "view_arn", view_arn)

    @property
    @pulumi.getter
    def filters(self) -> Optional['outputs.ViewSearchFilter']:
        """
        An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view. When you use this view in a [Search](https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_Search.html) operation, the filter string is combined with the search's `QueryString` parameter using a logical `AND` operator.

        For information about the supported syntax, see [Search query reference for Resource Explorer](https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html) in the *AWS Resource Explorer User Guide* .

        > This query string in the context of this operation supports only [filter prefixes](https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters) with optional [operators](https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators) . It doesn't support free-form text. For example, the string `region:us* service:ec2 -tag:stage=prod` includes all Amazon EC2 resources in any AWS Region that begin with the letters `us` and are *not* tagged with a key `Stage` that has the value `prod` .
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="includedProperties")
    def included_properties(self) -> Optional[Sequence['outputs.ViewIncludedProperty']]:
        """
        A list of fields that provide additional information about the view.
        """
        return pulumi.get(self, "included_properties")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tag key and value pairs that are attached to the view.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="viewArn")
    def view_arn(self) -> Optional[str]:
        """
        The ARN of the new view. For example:

        `arn:aws:resource-explorer-2:us-east-1:123456789012:view/MyView/EXAMPLE8-90ab-cdef-fedc-EXAMPLE22222`
        """
        return pulumi.get(self, "view_arn")


class AwaitableGetViewResult(GetViewResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetViewResult(
            filters=self.filters,
            included_properties=self.included_properties,
            tags=self.tags,
            view_arn=self.view_arn)


def get_view(view_arn: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetViewResult:
    """
    Definition of AWS::ResourceExplorer2::View Resource Type


    :param str view_arn: The ARN of the new view. For example:
           
           `arn:aws:resource-explorer-2:us-east-1:123456789012:view/MyView/EXAMPLE8-90ab-cdef-fedc-EXAMPLE22222`
    """
    __args__ = dict()
    __args__['viewArn'] = view_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:resourceexplorer2:getView', __args__, opts=opts, typ=GetViewResult).value

    return AwaitableGetViewResult(
        filters=pulumi.get(__ret__, 'filters'),
        included_properties=pulumi.get(__ret__, 'included_properties'),
        tags=pulumi.get(__ret__, 'tags'),
        view_arn=pulumi.get(__ret__, 'view_arn'))
def get_view_output(view_arn: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetViewResult]:
    """
    Definition of AWS::ResourceExplorer2::View Resource Type


    :param str view_arn: The ARN of the new view. For example:
           
           `arn:aws:resource-explorer-2:us-east-1:123456789012:view/MyView/EXAMPLE8-90ab-cdef-fedc-EXAMPLE22222`
    """
    __args__ = dict()
    __args__['viewArn'] = view_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:resourceexplorer2:getView', __args__, opts=opts, typ=GetViewResult)
    return __ret__.apply(lambda __response__: GetViewResult(
        filters=pulumi.get(__response__, 'filters'),
        included_properties=pulumi.get(__response__, 'included_properties'),
        tags=pulumi.get(__response__, 'tags'),
        view_arn=pulumi.get(__response__, 'view_arn')))
