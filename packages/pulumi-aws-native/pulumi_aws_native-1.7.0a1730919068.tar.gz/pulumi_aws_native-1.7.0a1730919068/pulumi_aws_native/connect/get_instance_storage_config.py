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
    'GetInstanceStorageConfigResult',
    'AwaitableGetInstanceStorageConfigResult',
    'get_instance_storage_config',
    'get_instance_storage_config_output',
]

@pulumi.output_type
class GetInstanceStorageConfigResult:
    def __init__(__self__, association_id=None, kinesis_firehose_config=None, kinesis_stream_config=None, kinesis_video_stream_config=None, s3_config=None, storage_type=None):
        if association_id and not isinstance(association_id, str):
            raise TypeError("Expected argument 'association_id' to be a str")
        pulumi.set(__self__, "association_id", association_id)
        if kinesis_firehose_config and not isinstance(kinesis_firehose_config, dict):
            raise TypeError("Expected argument 'kinesis_firehose_config' to be a dict")
        pulumi.set(__self__, "kinesis_firehose_config", kinesis_firehose_config)
        if kinesis_stream_config and not isinstance(kinesis_stream_config, dict):
            raise TypeError("Expected argument 'kinesis_stream_config' to be a dict")
        pulumi.set(__self__, "kinesis_stream_config", kinesis_stream_config)
        if kinesis_video_stream_config and not isinstance(kinesis_video_stream_config, dict):
            raise TypeError("Expected argument 'kinesis_video_stream_config' to be a dict")
        pulumi.set(__self__, "kinesis_video_stream_config", kinesis_video_stream_config)
        if s3_config and not isinstance(s3_config, dict):
            raise TypeError("Expected argument 's3_config' to be a dict")
        pulumi.set(__self__, "s3_config", s3_config)
        if storage_type and not isinstance(storage_type, str):
            raise TypeError("Expected argument 'storage_type' to be a str")
        pulumi.set(__self__, "storage_type", storage_type)

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> Optional[str]:
        """
        The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
        """
        return pulumi.get(self, "association_id")

    @property
    @pulumi.getter(name="kinesisFirehoseConfig")
    def kinesis_firehose_config(self) -> Optional['outputs.InstanceStorageConfigKinesisFirehoseConfig']:
        """
        The configuration of the Kinesis Firehose delivery stream.
        """
        return pulumi.get(self, "kinesis_firehose_config")

    @property
    @pulumi.getter(name="kinesisStreamConfig")
    def kinesis_stream_config(self) -> Optional['outputs.InstanceStorageConfigKinesisStreamConfig']:
        """
        The configuration of the Kinesis data stream.
        """
        return pulumi.get(self, "kinesis_stream_config")

    @property
    @pulumi.getter(name="kinesisVideoStreamConfig")
    def kinesis_video_stream_config(self) -> Optional['outputs.InstanceStorageConfigKinesisVideoStreamConfig']:
        """
        The configuration of the Kinesis video stream.
        """
        return pulumi.get(self, "kinesis_video_stream_config")

    @property
    @pulumi.getter(name="s3Config")
    def s3_config(self) -> Optional['outputs.InstanceStorageConfigS3Config']:
        """
        The S3 bucket configuration.
        """
        return pulumi.get(self, "s3_config")

    @property
    @pulumi.getter(name="storageType")
    def storage_type(self) -> Optional['InstanceStorageConfigStorageType']:
        """
        A valid storage type.
        """
        return pulumi.get(self, "storage_type")


class AwaitableGetInstanceStorageConfigResult(GetInstanceStorageConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceStorageConfigResult(
            association_id=self.association_id,
            kinesis_firehose_config=self.kinesis_firehose_config,
            kinesis_stream_config=self.kinesis_stream_config,
            kinesis_video_stream_config=self.kinesis_video_stream_config,
            s3_config=self.s3_config,
            storage_type=self.storage_type)


def get_instance_storage_config(association_id: Optional[str] = None,
                                instance_arn: Optional[str] = None,
                                resource_type: Optional['InstanceStorageConfigInstanceStorageResourceType'] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceStorageConfigResult:
    """
    Resource Type definition for AWS::Connect::InstanceStorageConfig


    :param str association_id: The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
    :param str instance_arn: Connect Instance ID with which the storage config will be associated
    :param 'InstanceStorageConfigInstanceStorageResourceType' resource_type: A valid resource type. Following are the valid resource types: `CHAT_TRANSCRIPTS` | `CALL_RECORDINGS` | `SCHEDULED_REPORTS` | `MEDIA_STREAMS` | `CONTACT_TRACE_RECORDS` | `AGENT_EVENTS`
    """
    __args__ = dict()
    __args__['associationId'] = association_id
    __args__['instanceArn'] = instance_arn
    __args__['resourceType'] = resource_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:connect:getInstanceStorageConfig', __args__, opts=opts, typ=GetInstanceStorageConfigResult).value

    return AwaitableGetInstanceStorageConfigResult(
        association_id=pulumi.get(__ret__, 'association_id'),
        kinesis_firehose_config=pulumi.get(__ret__, 'kinesis_firehose_config'),
        kinesis_stream_config=pulumi.get(__ret__, 'kinesis_stream_config'),
        kinesis_video_stream_config=pulumi.get(__ret__, 'kinesis_video_stream_config'),
        s3_config=pulumi.get(__ret__, 's3_config'),
        storage_type=pulumi.get(__ret__, 'storage_type'))
def get_instance_storage_config_output(association_id: Optional[pulumi.Input[str]] = None,
                                       instance_arn: Optional[pulumi.Input[str]] = None,
                                       resource_type: Optional[pulumi.Input['InstanceStorageConfigInstanceStorageResourceType']] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceStorageConfigResult]:
    """
    Resource Type definition for AWS::Connect::InstanceStorageConfig


    :param str association_id: The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.
    :param str instance_arn: Connect Instance ID with which the storage config will be associated
    :param 'InstanceStorageConfigInstanceStorageResourceType' resource_type: A valid resource type. Following are the valid resource types: `CHAT_TRANSCRIPTS` | `CALL_RECORDINGS` | `SCHEDULED_REPORTS` | `MEDIA_STREAMS` | `CONTACT_TRACE_RECORDS` | `AGENT_EVENTS`
    """
    __args__ = dict()
    __args__['associationId'] = association_id
    __args__['instanceArn'] = instance_arn
    __args__['resourceType'] = resource_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:connect:getInstanceStorageConfig', __args__, opts=opts, typ=GetInstanceStorageConfigResult)
    return __ret__.apply(lambda __response__: GetInstanceStorageConfigResult(
        association_id=pulumi.get(__response__, 'association_id'),
        kinesis_firehose_config=pulumi.get(__response__, 'kinesis_firehose_config'),
        kinesis_stream_config=pulumi.get(__response__, 'kinesis_stream_config'),
        kinesis_video_stream_config=pulumi.get(__response__, 'kinesis_video_stream_config'),
        s3_config=pulumi.get(__response__, 's3_config'),
        storage_type=pulumi.get(__response__, 'storage_type')))
