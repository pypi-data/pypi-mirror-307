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
from ._enums import *

__all__ = [
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    def __init__(__self__, arn=None, channel_ids=None, id=None, name=None, network_settings=None, state=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if channel_ids and not isinstance(channel_ids, list):
            raise TypeError("Expected argument 'channel_ids' to be a list")
        pulumi.set(__self__, "channel_ids", channel_ids)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_settings and not isinstance(network_settings, dict):
            raise TypeError("Expected argument 'network_settings' to be a dict")
        pulumi.set(__self__, "network_settings", network_settings)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the Cluster.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="channelIds")
    def channel_ids(self) -> Optional[Sequence[str]]:
        """
        The MediaLive Channels that are currently running on Nodes in this Cluster.
        """
        return pulumi.get(self, "channel_ids")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique ID of the Cluster.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The user-specified name of the Cluster to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkSettings")
    def network_settings(self) -> Optional['outputs.ClusterNetworkSettings']:
        return pulumi.get(self, "network_settings")

    @property
    @pulumi.getter
    def state(self) -> Optional['ClusterState']:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A collection of key-value pairs.
        """
        return pulumi.get(self, "tags")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            arn=self.arn,
            channel_ids=self.channel_ids,
            id=self.id,
            name=self.name,
            network_settings=self.network_settings,
            state=self.state,
            tags=self.tags)


def get_cluster(id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Definition of AWS::MediaLive::Cluster Resource Type


    :param str id: The unique ID of the Cluster.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:medialive:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        arn=pulumi.get(__ret__, 'arn'),
        channel_ids=pulumi.get(__ret__, 'channel_ids'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        network_settings=pulumi.get(__ret__, 'network_settings'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))
def get_cluster_output(id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    Definition of AWS::MediaLive::Cluster Resource Type


    :param str id: The unique ID of the Cluster.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:medialive:getCluster', __args__, opts=opts, typ=GetClusterResult)
    return __ret__.apply(lambda __response__: GetClusterResult(
        arn=pulumi.get(__response__, 'arn'),
        channel_ids=pulumi.get(__response__, 'channel_ids'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        network_settings=pulumi.get(__response__, 'network_settings'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags')))
