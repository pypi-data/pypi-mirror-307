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
    'GetVpcLinkResult',
    'AwaitableGetVpcLinkResult',
    'get_vpc_link',
    'get_vpc_link_output',
]

@pulumi.output_type
class GetVpcLinkResult:
    def __init__(__self__, name=None, tags=None, vpc_link_id=None):
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if vpc_link_id and not isinstance(vpc_link_id, str):
            raise TypeError("Expected argument 'vpc_link_id' to be a str")
        pulumi.set(__self__, "vpc_link_id", vpc_link_id)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the VPC link.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The collection of tags. Each tag element is associated with a given resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcLinkId")
    def vpc_link_id(self) -> Optional[str]:
        """
        The VPC link ID.
        """
        return pulumi.get(self, "vpc_link_id")


class AwaitableGetVpcLinkResult(GetVpcLinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcLinkResult(
            name=self.name,
            tags=self.tags,
            vpc_link_id=self.vpc_link_id)


def get_vpc_link(vpc_link_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcLinkResult:
    """
    The ``AWS::ApiGatewayV2::VpcLink`` resource creates a VPC link. Supported only for HTTP APIs. The VPC link status must transition from ``PENDING`` to ``AVAILABLE`` to successfully create a VPC link, which can take up to 10 minutes. To learn more, see [Working with VPC Links for HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vpc-links.html) in the *API Gateway Developer Guide*.


    :param str vpc_link_id: The VPC link ID.
    """
    __args__ = dict()
    __args__['vpcLinkId'] = vpc_link_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigatewayv2:getVpcLink', __args__, opts=opts, typ=GetVpcLinkResult).value

    return AwaitableGetVpcLinkResult(
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_link_id=pulumi.get(__ret__, 'vpc_link_id'))
def get_vpc_link_output(vpc_link_id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcLinkResult]:
    """
    The ``AWS::ApiGatewayV2::VpcLink`` resource creates a VPC link. Supported only for HTTP APIs. The VPC link status must transition from ``PENDING`` to ``AVAILABLE`` to successfully create a VPC link, which can take up to 10 minutes. To learn more, see [Working with VPC Links for HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vpc-links.html) in the *API Gateway Developer Guide*.


    :param str vpc_link_id: The VPC link ID.
    """
    __args__ = dict()
    __args__['vpcLinkId'] = vpc_link_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigatewayv2:getVpcLink', __args__, opts=opts, typ=GetVpcLinkResult)
    return __ret__.apply(lambda __response__: GetVpcLinkResult(
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags'),
        vpc_link_id=pulumi.get(__response__, 'vpc_link_id')))
