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
    'GetDomainNameResult',
    'AwaitableGetDomainNameResult',
    'get_domain_name',
    'get_domain_name_output',
]

@pulumi.output_type
class GetDomainNameResult:
    def __init__(__self__, certificate_arn=None, distribution_domain_name=None, distribution_hosted_zone_id=None, endpoint_configuration=None, mutual_tls_authentication=None, ownership_verification_certificate_arn=None, regional_certificate_arn=None, regional_domain_name=None, regional_hosted_zone_id=None, security_policy=None, tags=None):
        if certificate_arn and not isinstance(certificate_arn, str):
            raise TypeError("Expected argument 'certificate_arn' to be a str")
        pulumi.set(__self__, "certificate_arn", certificate_arn)
        if distribution_domain_name and not isinstance(distribution_domain_name, str):
            raise TypeError("Expected argument 'distribution_domain_name' to be a str")
        pulumi.set(__self__, "distribution_domain_name", distribution_domain_name)
        if distribution_hosted_zone_id and not isinstance(distribution_hosted_zone_id, str):
            raise TypeError("Expected argument 'distribution_hosted_zone_id' to be a str")
        pulumi.set(__self__, "distribution_hosted_zone_id", distribution_hosted_zone_id)
        if endpoint_configuration and not isinstance(endpoint_configuration, dict):
            raise TypeError("Expected argument 'endpoint_configuration' to be a dict")
        pulumi.set(__self__, "endpoint_configuration", endpoint_configuration)
        if mutual_tls_authentication and not isinstance(mutual_tls_authentication, dict):
            raise TypeError("Expected argument 'mutual_tls_authentication' to be a dict")
        pulumi.set(__self__, "mutual_tls_authentication", mutual_tls_authentication)
        if ownership_verification_certificate_arn and not isinstance(ownership_verification_certificate_arn, str):
            raise TypeError("Expected argument 'ownership_verification_certificate_arn' to be a str")
        pulumi.set(__self__, "ownership_verification_certificate_arn", ownership_verification_certificate_arn)
        if regional_certificate_arn and not isinstance(regional_certificate_arn, str):
            raise TypeError("Expected argument 'regional_certificate_arn' to be a str")
        pulumi.set(__self__, "regional_certificate_arn", regional_certificate_arn)
        if regional_domain_name and not isinstance(regional_domain_name, str):
            raise TypeError("Expected argument 'regional_domain_name' to be a str")
        pulumi.set(__self__, "regional_domain_name", regional_domain_name)
        if regional_hosted_zone_id and not isinstance(regional_hosted_zone_id, str):
            raise TypeError("Expected argument 'regional_hosted_zone_id' to be a str")
        pulumi.set(__self__, "regional_hosted_zone_id", regional_hosted_zone_id)
        if security_policy and not isinstance(security_policy, str):
            raise TypeError("Expected argument 'security_policy' to be a str")
        pulumi.set(__self__, "security_policy", security_policy)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> Optional[str]:
        """
        The reference to an AWS -managed certificate that will be used by edge-optimized endpoint for this domain name. AWS Certificate Manager is the only supported source.
        """
        return pulumi.get(self, "certificate_arn")

    @property
    @pulumi.getter(name="distributionDomainName")
    def distribution_domain_name(self) -> Optional[str]:
        """
        The Amazon CloudFront distribution domain name that's mapped to the custom domain name. This is only applicable for endpoints whose type is `EDGE` .

        Example: `d111111abcdef8.cloudfront.net`
        """
        return pulumi.get(self, "distribution_domain_name")

    @property
    @pulumi.getter(name="distributionHostedZoneId")
    def distribution_hosted_zone_id(self) -> Optional[str]:
        """
        The region-agnostic Amazon Route 53 Hosted Zone ID of the edge-optimized endpoint. The only valid value is `Z2FDTNDATAQYW2` for all regions.
        """
        return pulumi.get(self, "distribution_hosted_zone_id")

    @property
    @pulumi.getter(name="endpointConfiguration")
    def endpoint_configuration(self) -> Optional['outputs.DomainNameEndpointConfiguration']:
        """
        The endpoint configuration of this DomainName showing the endpoint types of the domain name.
        """
        return pulumi.get(self, "endpoint_configuration")

    @property
    @pulumi.getter(name="mutualTlsAuthentication")
    def mutual_tls_authentication(self) -> Optional['outputs.DomainNameMutualTlsAuthentication']:
        """
        The mutual TLS authentication configuration for a custom domain name. If specified, API Gateway performs two-way authentication between the client and the server. Clients must present a trusted certificate to access your API.
        """
        return pulumi.get(self, "mutual_tls_authentication")

    @property
    @pulumi.getter(name="ownershipVerificationCertificateArn")
    def ownership_verification_certificate_arn(self) -> Optional[str]:
        """
        The ARN of the public certificate issued by ACM to validate ownership of your custom domain. Only required when configuring mutual TLS and using an ACM imported or private CA certificate ARN as the RegionalCertificateArn.
        """
        return pulumi.get(self, "ownership_verification_certificate_arn")

    @property
    @pulumi.getter(name="regionalCertificateArn")
    def regional_certificate_arn(self) -> Optional[str]:
        """
        The reference to an AWS -managed certificate that will be used for validating the regional domain name. AWS Certificate Manager is the only supported source.
        """
        return pulumi.get(self, "regional_certificate_arn")

    @property
    @pulumi.getter(name="regionalDomainName")
    def regional_domain_name(self) -> Optional[str]:
        """
        The domain name associated with the regional endpoint for this custom domain name. You set up this association by adding a DNS record that points the custom domain name to this regional domain name.
        """
        return pulumi.get(self, "regional_domain_name")

    @property
    @pulumi.getter(name="regionalHostedZoneId")
    def regional_hosted_zone_id(self) -> Optional[str]:
        """
        The region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.
        """
        return pulumi.get(self, "regional_hosted_zone_id")

    @property
    @pulumi.getter(name="securityPolicy")
    def security_policy(self) -> Optional[str]:
        """
        The Transport Layer Security (TLS) version + cipher suite for this DomainName. The valid values are `TLS_1_0` and `TLS_1_2` .
        """
        return pulumi.get(self, "security_policy")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The collection of tags. Each tag element is associated with a given resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDomainNameResult(GetDomainNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainNameResult(
            certificate_arn=self.certificate_arn,
            distribution_domain_name=self.distribution_domain_name,
            distribution_hosted_zone_id=self.distribution_hosted_zone_id,
            endpoint_configuration=self.endpoint_configuration,
            mutual_tls_authentication=self.mutual_tls_authentication,
            ownership_verification_certificate_arn=self.ownership_verification_certificate_arn,
            regional_certificate_arn=self.regional_certificate_arn,
            regional_domain_name=self.regional_domain_name,
            regional_hosted_zone_id=self.regional_hosted_zone_id,
            security_policy=self.security_policy,
            tags=self.tags)


def get_domain_name(domain_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainNameResult:
    """
    Resource Type definition for AWS::ApiGateway::DomainName.


    :param str domain_name: The custom domain name as an API host name, for example, `my-api.example.com` .
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigateway:getDomainName', __args__, opts=opts, typ=GetDomainNameResult).value

    return AwaitableGetDomainNameResult(
        certificate_arn=pulumi.get(__ret__, 'certificate_arn'),
        distribution_domain_name=pulumi.get(__ret__, 'distribution_domain_name'),
        distribution_hosted_zone_id=pulumi.get(__ret__, 'distribution_hosted_zone_id'),
        endpoint_configuration=pulumi.get(__ret__, 'endpoint_configuration'),
        mutual_tls_authentication=pulumi.get(__ret__, 'mutual_tls_authentication'),
        ownership_verification_certificate_arn=pulumi.get(__ret__, 'ownership_verification_certificate_arn'),
        regional_certificate_arn=pulumi.get(__ret__, 'regional_certificate_arn'),
        regional_domain_name=pulumi.get(__ret__, 'regional_domain_name'),
        regional_hosted_zone_id=pulumi.get(__ret__, 'regional_hosted_zone_id'),
        security_policy=pulumi.get(__ret__, 'security_policy'),
        tags=pulumi.get(__ret__, 'tags'))
def get_domain_name_output(domain_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDomainNameResult]:
    """
    Resource Type definition for AWS::ApiGateway::DomainName.


    :param str domain_name: The custom domain name as an API host name, for example, `my-api.example.com` .
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigateway:getDomainName', __args__, opts=opts, typ=GetDomainNameResult)
    return __ret__.apply(lambda __response__: GetDomainNameResult(
        certificate_arn=pulumi.get(__response__, 'certificate_arn'),
        distribution_domain_name=pulumi.get(__response__, 'distribution_domain_name'),
        distribution_hosted_zone_id=pulumi.get(__response__, 'distribution_hosted_zone_id'),
        endpoint_configuration=pulumi.get(__response__, 'endpoint_configuration'),
        mutual_tls_authentication=pulumi.get(__response__, 'mutual_tls_authentication'),
        ownership_verification_certificate_arn=pulumi.get(__response__, 'ownership_verification_certificate_arn'),
        regional_certificate_arn=pulumi.get(__response__, 'regional_certificate_arn'),
        regional_domain_name=pulumi.get(__response__, 'regional_domain_name'),
        regional_hosted_zone_id=pulumi.get(__response__, 'regional_hosted_zone_id'),
        security_policy=pulumi.get(__response__, 'security_policy'),
        tags=pulumi.get(__response__, 'tags')))
