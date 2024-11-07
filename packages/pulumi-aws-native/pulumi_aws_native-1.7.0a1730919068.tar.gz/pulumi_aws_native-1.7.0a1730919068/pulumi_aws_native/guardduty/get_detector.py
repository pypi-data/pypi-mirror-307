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
    'GetDetectorResult',
    'AwaitableGetDetectorResult',
    'get_detector',
    'get_detector_output',
]

@pulumi.output_type
class GetDetectorResult:
    def __init__(__self__, data_sources=None, enable=None, features=None, finding_publishing_frequency=None, id=None, tags=None):
        if data_sources and not isinstance(data_sources, dict):
            raise TypeError("Expected argument 'data_sources' to be a dict")
        pulumi.set(__self__, "data_sources", data_sources)
        if enable and not isinstance(enable, bool):
            raise TypeError("Expected argument 'enable' to be a bool")
        pulumi.set(__self__, "enable", enable)
        if features and not isinstance(features, list):
            raise TypeError("Expected argument 'features' to be a list")
        pulumi.set(__self__, "features", features)
        if finding_publishing_frequency and not isinstance(finding_publishing_frequency, str):
            raise TypeError("Expected argument 'finding_publishing_frequency' to be a str")
        pulumi.set(__self__, "finding_publishing_frequency", finding_publishing_frequency)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="dataSources")
    def data_sources(self) -> Optional['outputs.DetectorCfnDataSourceConfigurations']:
        """
        Describes which data sources will be enabled for the detector.
        """
        return pulumi.get(self, "data_sources")

    @property
    @pulumi.getter
    def enable(self) -> Optional[bool]:
        """
        Specifies whether the detector is to be enabled on creation.
        """
        return pulumi.get(self, "enable")

    @property
    @pulumi.getter
    def features(self) -> Optional[Sequence['outputs.DetectorCfnFeatureConfiguration']]:
        """
        A list of features that will be configured for the detector.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter(name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> Optional[str]:
        """
        Specifies how frequently updated findings are exported.
        """
        return pulumi.get(self, "finding_publishing_frequency")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique ID of the detector.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Specifies tags added to a new detector resource. Each tag consists of a key and an optional value, both of which you define.

        Currently, support is available only for creating and deleting a tag. No support exists for updating the tags.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")


class AwaitableGetDetectorResult(GetDetectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDetectorResult(
            data_sources=self.data_sources,
            enable=self.enable,
            features=self.features,
            finding_publishing_frequency=self.finding_publishing_frequency,
            id=self.id,
            tags=self.tags)


def get_detector(id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDetectorResult:
    """
    Resource Type definition for AWS::GuardDuty::Detector


    :param str id: The unique ID of the detector.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:guardduty:getDetector', __args__, opts=opts, typ=GetDetectorResult).value

    return AwaitableGetDetectorResult(
        data_sources=pulumi.get(__ret__, 'data_sources'),
        enable=pulumi.get(__ret__, 'enable'),
        features=pulumi.get(__ret__, 'features'),
        finding_publishing_frequency=pulumi.get(__ret__, 'finding_publishing_frequency'),
        id=pulumi.get(__ret__, 'id'),
        tags=pulumi.get(__ret__, 'tags'))
def get_detector_output(id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDetectorResult]:
    """
    Resource Type definition for AWS::GuardDuty::Detector


    :param str id: The unique ID of the detector.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:guardduty:getDetector', __args__, opts=opts, typ=GetDetectorResult)
    return __ret__.apply(lambda __response__: GetDetectorResult(
        data_sources=pulumi.get(__response__, 'data_sources'),
        enable=pulumi.get(__response__, 'enable'),
        features=pulumi.get(__response__, 'features'),
        finding_publishing_frequency=pulumi.get(__response__, 'finding_publishing_frequency'),
        id=pulumi.get(__response__, 'id'),
        tags=pulumi.get(__response__, 'tags')))
