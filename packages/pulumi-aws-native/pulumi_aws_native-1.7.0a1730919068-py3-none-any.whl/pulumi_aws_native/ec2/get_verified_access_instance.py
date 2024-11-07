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
    'GetVerifiedAccessInstanceResult',
    'AwaitableGetVerifiedAccessInstanceResult',
    'get_verified_access_instance',
    'get_verified_access_instance_output',
]

@pulumi.output_type
class GetVerifiedAccessInstanceResult:
    def __init__(__self__, creation_time=None, description=None, fips_enabled=None, last_updated_time=None, logging_configurations=None, tags=None, verified_access_instance_id=None, verified_access_trust_provider_ids=None, verified_access_trust_providers=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if fips_enabled and not isinstance(fips_enabled, bool):
            raise TypeError("Expected argument 'fips_enabled' to be a bool")
        pulumi.set(__self__, "fips_enabled", fips_enabled)
        if last_updated_time and not isinstance(last_updated_time, str):
            raise TypeError("Expected argument 'last_updated_time' to be a str")
        pulumi.set(__self__, "last_updated_time", last_updated_time)
        if logging_configurations and not isinstance(logging_configurations, dict):
            raise TypeError("Expected argument 'logging_configurations' to be a dict")
        pulumi.set(__self__, "logging_configurations", logging_configurations)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if verified_access_instance_id and not isinstance(verified_access_instance_id, str):
            raise TypeError("Expected argument 'verified_access_instance_id' to be a str")
        pulumi.set(__self__, "verified_access_instance_id", verified_access_instance_id)
        if verified_access_trust_provider_ids and not isinstance(verified_access_trust_provider_ids, list):
            raise TypeError("Expected argument 'verified_access_trust_provider_ids' to be a list")
        pulumi.set(__self__, "verified_access_trust_provider_ids", verified_access_trust_provider_ids)
        if verified_access_trust_providers and not isinstance(verified_access_trust_providers, list):
            raise TypeError("Expected argument 'verified_access_trust_providers' to be a list")
        pulumi.set(__self__, "verified_access_trust_providers", verified_access_trust_providers)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        Time this Verified Access Instance was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the AWS Verified Access instance.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fipsEnabled")
    def fips_enabled(self) -> Optional[bool]:
        """
        Indicates whether FIPS is enabled
        """
        return pulumi.get(self, "fips_enabled")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> Optional[str]:
        """
        Time this Verified Access Instance was last updated.
        """
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter(name="loggingConfigurations")
    def logging_configurations(self) -> Optional['outputs.VerifiedAccessInstanceVerifiedAccessLogs']:
        """
        The configuration options for AWS Verified Access instances.
        """
        return pulumi.get(self, "logging_configurations")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="verifiedAccessInstanceId")
    def verified_access_instance_id(self) -> Optional[str]:
        """
        The ID of the AWS Verified Access instance.
        """
        return pulumi.get(self, "verified_access_instance_id")

    @property
    @pulumi.getter(name="verifiedAccessTrustProviderIds")
    def verified_access_trust_provider_ids(self) -> Optional[Sequence[str]]:
        """
        The IDs of the AWS Verified Access trust providers.
        """
        return pulumi.get(self, "verified_access_trust_provider_ids")

    @property
    @pulumi.getter(name="verifiedAccessTrustProviders")
    def verified_access_trust_providers(self) -> Optional[Sequence['outputs.VerifiedAccessInstanceVerifiedAccessTrustProvider']]:
        """
        AWS Verified Access trust providers.
        """
        return pulumi.get(self, "verified_access_trust_providers")


class AwaitableGetVerifiedAccessInstanceResult(GetVerifiedAccessInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVerifiedAccessInstanceResult(
            creation_time=self.creation_time,
            description=self.description,
            fips_enabled=self.fips_enabled,
            last_updated_time=self.last_updated_time,
            logging_configurations=self.logging_configurations,
            tags=self.tags,
            verified_access_instance_id=self.verified_access_instance_id,
            verified_access_trust_provider_ids=self.verified_access_trust_provider_ids,
            verified_access_trust_providers=self.verified_access_trust_providers)


def get_verified_access_instance(verified_access_instance_id: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVerifiedAccessInstanceResult:
    """
    The AWS::EC2::VerifiedAccessInstance resource creates an AWS EC2 Verified Access Instance.


    :param str verified_access_instance_id: The ID of the AWS Verified Access instance.
    """
    __args__ = dict()
    __args__['verifiedAccessInstanceId'] = verified_access_instance_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getVerifiedAccessInstance', __args__, opts=opts, typ=GetVerifiedAccessInstanceResult).value

    return AwaitableGetVerifiedAccessInstanceResult(
        creation_time=pulumi.get(__ret__, 'creation_time'),
        description=pulumi.get(__ret__, 'description'),
        fips_enabled=pulumi.get(__ret__, 'fips_enabled'),
        last_updated_time=pulumi.get(__ret__, 'last_updated_time'),
        logging_configurations=pulumi.get(__ret__, 'logging_configurations'),
        tags=pulumi.get(__ret__, 'tags'),
        verified_access_instance_id=pulumi.get(__ret__, 'verified_access_instance_id'),
        verified_access_trust_provider_ids=pulumi.get(__ret__, 'verified_access_trust_provider_ids'),
        verified_access_trust_providers=pulumi.get(__ret__, 'verified_access_trust_providers'))
def get_verified_access_instance_output(verified_access_instance_id: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVerifiedAccessInstanceResult]:
    """
    The AWS::EC2::VerifiedAccessInstance resource creates an AWS EC2 Verified Access Instance.


    :param str verified_access_instance_id: The ID of the AWS Verified Access instance.
    """
    __args__ = dict()
    __args__['verifiedAccessInstanceId'] = verified_access_instance_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getVerifiedAccessInstance', __args__, opts=opts, typ=GetVerifiedAccessInstanceResult)
    return __ret__.apply(lambda __response__: GetVerifiedAccessInstanceResult(
        creation_time=pulumi.get(__response__, 'creation_time'),
        description=pulumi.get(__response__, 'description'),
        fips_enabled=pulumi.get(__response__, 'fips_enabled'),
        last_updated_time=pulumi.get(__response__, 'last_updated_time'),
        logging_configurations=pulumi.get(__response__, 'logging_configurations'),
        tags=pulumi.get(__response__, 'tags'),
        verified_access_instance_id=pulumi.get(__response__, 'verified_access_instance_id'),
        verified_access_trust_provider_ids=pulumi.get(__response__, 'verified_access_trust_provider_ids'),
        verified_access_trust_providers=pulumi.get(__response__, 'verified_access_trust_providers')))
