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

__all__ = [
    'GetLinkResult',
    'AwaitableGetLinkResult',
    'get_link',
    'get_link_output',
]

@pulumi.output_type
class GetLinkResult:
    def __init__(__self__, bandwidth=None, created_at=None, description=None, link_arn=None, link_id=None, provider=None, state=None, tags=None, type=None):
        if bandwidth and not isinstance(bandwidth, dict):
            raise TypeError("Expected argument 'bandwidth' to be a dict")
        pulumi.set(__self__, "bandwidth", bandwidth)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if link_arn and not isinstance(link_arn, str):
            raise TypeError("Expected argument 'link_arn' to be a str")
        pulumi.set(__self__, "link_arn", link_arn)
        if link_id and not isinstance(link_id, str):
            raise TypeError("Expected argument 'link_id' to be a str")
        pulumi.set(__self__, "link_id", link_id)
        if provider and not isinstance(provider, str):
            raise TypeError("Expected argument 'provider' to be a str")
        pulumi.set(__self__, "provider", provider)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional['outputs.LinkBandwidth']:
        """
        The Bandwidth for the link.
        """
        return pulumi.get(self, "bandwidth")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date and time that the device was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the link.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="linkArn")
    def link_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the link.
        """
        return pulumi.get(self, "link_arn")

    @property
    @pulumi.getter(name="linkId")
    def link_id(self) -> Optional[str]:
        """
        The ID of the link.
        """
        return pulumi.get(self, "link_id")

    @property
    @pulumi.getter
    def provider(self) -> Optional[str]:
        """
        The provider of the link.
        """
        return pulumi.get(self, "provider")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the link.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags for the link.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the link.
        """
        return pulumi.get(self, "type")


class AwaitableGetLinkResult(GetLinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinkResult(
            bandwidth=self.bandwidth,
            created_at=self.created_at,
            description=self.description,
            link_arn=self.link_arn,
            link_id=self.link_id,
            provider=self.provider,
            state=self.state,
            tags=self.tags,
            type=self.type)


def get_link(global_network_id: Optional[str] = None,
             link_id: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinkResult:
    """
    The AWS::NetworkManager::Link type describes a link.


    :param str global_network_id: The ID of the global network.
    :param str link_id: The ID of the link.
    """
    __args__ = dict()
    __args__['globalNetworkId'] = global_network_id
    __args__['linkId'] = link_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:networkmanager:getLink', __args__, opts=opts, typ=GetLinkResult).value

    return AwaitableGetLinkResult(
        bandwidth=pulumi.get(__ret__, 'bandwidth'),
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        link_arn=pulumi.get(__ret__, 'link_arn'),
        link_id=pulumi.get(__ret__, 'link_id'),
        provider=pulumi.get(__ret__, 'provider'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))
def get_link_output(global_network_id: Optional[pulumi.Input[str]] = None,
                    link_id: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinkResult]:
    """
    The AWS::NetworkManager::Link type describes a link.


    :param str global_network_id: The ID of the global network.
    :param str link_id: The ID of the link.
    """
    __args__ = dict()
    __args__['globalNetworkId'] = global_network_id
    __args__['linkId'] = link_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:networkmanager:getLink', __args__, opts=opts, typ=GetLinkResult)
    return __ret__.apply(lambda __response__: GetLinkResult(
        bandwidth=pulumi.get(__response__, 'bandwidth'),
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        link_arn=pulumi.get(__response__, 'link_arn'),
        link_id=pulumi.get(__response__, 'link_id'),
        provider=pulumi.get(__response__, 'provider'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags'),
        type=pulumi.get(__response__, 'type')))
