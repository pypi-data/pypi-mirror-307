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
from ._enums import *

__all__ = [
    'GetChannelResult',
    'AwaitableGetChannelResult',
    'get_channel',
    'get_channel_output',
]

@pulumi.output_type
class GetChannelResult:
    def __init__(__self__, arn=None, authorized=None, ingest_endpoint=None, insecure_ingest=None, latency_mode=None, name=None, playback_url=None, preset=None, recording_configuration_arn=None, tags=None, type=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if authorized and not isinstance(authorized, bool):
            raise TypeError("Expected argument 'authorized' to be a bool")
        pulumi.set(__self__, "authorized", authorized)
        if ingest_endpoint and not isinstance(ingest_endpoint, str):
            raise TypeError("Expected argument 'ingest_endpoint' to be a str")
        pulumi.set(__self__, "ingest_endpoint", ingest_endpoint)
        if insecure_ingest and not isinstance(insecure_ingest, bool):
            raise TypeError("Expected argument 'insecure_ingest' to be a bool")
        pulumi.set(__self__, "insecure_ingest", insecure_ingest)
        if latency_mode and not isinstance(latency_mode, str):
            raise TypeError("Expected argument 'latency_mode' to be a str")
        pulumi.set(__self__, "latency_mode", latency_mode)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if playback_url and not isinstance(playback_url, str):
            raise TypeError("Expected argument 'playback_url' to be a str")
        pulumi.set(__self__, "playback_url", playback_url)
        if preset and not isinstance(preset, str):
            raise TypeError("Expected argument 'preset' to be a str")
        pulumi.set(__self__, "preset", preset)
        if recording_configuration_arn and not isinstance(recording_configuration_arn, str):
            raise TypeError("Expected argument 'recording_configuration_arn' to be a str")
        pulumi.set(__self__, "recording_configuration_arn", recording_configuration_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Channel ARN is automatically generated on creation and assigned as the unique identifier.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def authorized(self) -> Optional[bool]:
        """
        Whether the channel is authorized.
        """
        return pulumi.get(self, "authorized")

    @property
    @pulumi.getter(name="ingestEndpoint")
    def ingest_endpoint(self) -> Optional[str]:
        """
        Channel ingest endpoint, part of the definition of an ingest server, used when you set up streaming software.
        """
        return pulumi.get(self, "ingest_endpoint")

    @property
    @pulumi.getter(name="insecureIngest")
    def insecure_ingest(self) -> Optional[bool]:
        """
        Whether the channel allows insecure ingest.
        """
        return pulumi.get(self, "insecure_ingest")

    @property
    @pulumi.getter(name="latencyMode")
    def latency_mode(self) -> Optional['ChannelLatencyMode']:
        """
        Channel latency mode.
        """
        return pulumi.get(self, "latency_mode")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Channel
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="playbackUrl")
    def playback_url(self) -> Optional[str]:
        """
        Channel Playback URL.
        """
        return pulumi.get(self, "playback_url")

    @property
    @pulumi.getter
    def preset(self) -> Optional['ChannelPreset']:
        """
        Optional transcode preset for the channel. This is selectable only for ADVANCED_HD and ADVANCED_SD channel types. For those channel types, the default preset is HIGHER_BANDWIDTH_DELIVERY. For other channel types (BASIC and STANDARD), preset is the empty string ("").
        """
        return pulumi.get(self, "preset")

    @property
    @pulumi.getter(name="recordingConfigurationArn")
    def recording_configuration_arn(self) -> Optional[str]:
        """
        Recording Configuration ARN. A value other than an empty string indicates that recording is enabled. Default: "" (recording is disabled).
        """
        return pulumi.get(self, "recording_configuration_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of key-value pairs that contain metadata for the asset model.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional['ChannelType']:
        """
        Channel type, which determines the allowable resolution and bitrate. If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.
        """
        return pulumi.get(self, "type")


class AwaitableGetChannelResult(GetChannelResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetChannelResult(
            arn=self.arn,
            authorized=self.authorized,
            ingest_endpoint=self.ingest_endpoint,
            insecure_ingest=self.insecure_ingest,
            latency_mode=self.latency_mode,
            name=self.name,
            playback_url=self.playback_url,
            preset=self.preset,
            recording_configuration_arn=self.recording_configuration_arn,
            tags=self.tags,
            type=self.type)


def get_channel(arn: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetChannelResult:
    """
    Resource Type definition for AWS::IVS::Channel


    :param str arn: Channel ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ivs:getChannel', __args__, opts=opts, typ=GetChannelResult).value

    return AwaitableGetChannelResult(
        arn=pulumi.get(__ret__, 'arn'),
        authorized=pulumi.get(__ret__, 'authorized'),
        ingest_endpoint=pulumi.get(__ret__, 'ingest_endpoint'),
        insecure_ingest=pulumi.get(__ret__, 'insecure_ingest'),
        latency_mode=pulumi.get(__ret__, 'latency_mode'),
        name=pulumi.get(__ret__, 'name'),
        playback_url=pulumi.get(__ret__, 'playback_url'),
        preset=pulumi.get(__ret__, 'preset'),
        recording_configuration_arn=pulumi.get(__ret__, 'recording_configuration_arn'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))
def get_channel_output(arn: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetChannelResult]:
    """
    Resource Type definition for AWS::IVS::Channel


    :param str arn: Channel ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ivs:getChannel', __args__, opts=opts, typ=GetChannelResult)
    return __ret__.apply(lambda __response__: GetChannelResult(
        arn=pulumi.get(__response__, 'arn'),
        authorized=pulumi.get(__response__, 'authorized'),
        ingest_endpoint=pulumi.get(__response__, 'ingest_endpoint'),
        insecure_ingest=pulumi.get(__response__, 'insecure_ingest'),
        latency_mode=pulumi.get(__response__, 'latency_mode'),
        name=pulumi.get(__response__, 'name'),
        playback_url=pulumi.get(__response__, 'playback_url'),
        preset=pulumi.get(__response__, 'preset'),
        recording_configuration_arn=pulumi.get(__response__, 'recording_configuration_arn'),
        tags=pulumi.get(__response__, 'tags'),
        type=pulumi.get(__response__, 'type')))
