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
    'GetDomainResult',
    'AwaitableGetDomainResult',
    'get_domain',
    'get_domain_output',
]

@pulumi.output_type
class GetDomainResult:
    def __init__(__self__, access_policies=None, advanced_options=None, advanced_security_options=None, arn=None, cluster_config=None, cognito_options=None, domain_arn=None, domain_endpoint=None, domain_endpoint_options=None, domain_endpoint_v2=None, domain_endpoints=None, ebs_options=None, encryption_at_rest_options=None, engine_version=None, id=None, identity_center_options=None, ip_address_type=None, log_publishing_options=None, node_to_node_encryption_options=None, off_peak_window_options=None, service_software_options=None, skip_shard_migration_wait=None, snapshot_options=None, software_update_options=None, tags=None, vpc_options=None):
        if access_policies and not isinstance(access_policies, dict):
            raise TypeError("Expected argument 'access_policies' to be a dict")
        pulumi.set(__self__, "access_policies", access_policies)
        if advanced_options and not isinstance(advanced_options, dict):
            raise TypeError("Expected argument 'advanced_options' to be a dict")
        pulumi.set(__self__, "advanced_options", advanced_options)
        if advanced_security_options and not isinstance(advanced_security_options, dict):
            raise TypeError("Expected argument 'advanced_security_options' to be a dict")
        pulumi.set(__self__, "advanced_security_options", advanced_security_options)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cluster_config and not isinstance(cluster_config, dict):
            raise TypeError("Expected argument 'cluster_config' to be a dict")
        pulumi.set(__self__, "cluster_config", cluster_config)
        if cognito_options and not isinstance(cognito_options, dict):
            raise TypeError("Expected argument 'cognito_options' to be a dict")
        pulumi.set(__self__, "cognito_options", cognito_options)
        if domain_arn and not isinstance(domain_arn, str):
            raise TypeError("Expected argument 'domain_arn' to be a str")
        pulumi.set(__self__, "domain_arn", domain_arn)
        if domain_endpoint and not isinstance(domain_endpoint, str):
            raise TypeError("Expected argument 'domain_endpoint' to be a str")
        pulumi.set(__self__, "domain_endpoint", domain_endpoint)
        if domain_endpoint_options and not isinstance(domain_endpoint_options, dict):
            raise TypeError("Expected argument 'domain_endpoint_options' to be a dict")
        pulumi.set(__self__, "domain_endpoint_options", domain_endpoint_options)
        if domain_endpoint_v2 and not isinstance(domain_endpoint_v2, str):
            raise TypeError("Expected argument 'domain_endpoint_v2' to be a str")
        pulumi.set(__self__, "domain_endpoint_v2", domain_endpoint_v2)
        if domain_endpoints and not isinstance(domain_endpoints, dict):
            raise TypeError("Expected argument 'domain_endpoints' to be a dict")
        pulumi.set(__self__, "domain_endpoints", domain_endpoints)
        if ebs_options and not isinstance(ebs_options, dict):
            raise TypeError("Expected argument 'ebs_options' to be a dict")
        pulumi.set(__self__, "ebs_options", ebs_options)
        if encryption_at_rest_options and not isinstance(encryption_at_rest_options, dict):
            raise TypeError("Expected argument 'encryption_at_rest_options' to be a dict")
        pulumi.set(__self__, "encryption_at_rest_options", encryption_at_rest_options)
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        pulumi.set(__self__, "engine_version", engine_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity_center_options and not isinstance(identity_center_options, dict):
            raise TypeError("Expected argument 'identity_center_options' to be a dict")
        pulumi.set(__self__, "identity_center_options", identity_center_options)
        if ip_address_type and not isinstance(ip_address_type, str):
            raise TypeError("Expected argument 'ip_address_type' to be a str")
        pulumi.set(__self__, "ip_address_type", ip_address_type)
        if log_publishing_options and not isinstance(log_publishing_options, dict):
            raise TypeError("Expected argument 'log_publishing_options' to be a dict")
        pulumi.set(__self__, "log_publishing_options", log_publishing_options)
        if node_to_node_encryption_options and not isinstance(node_to_node_encryption_options, dict):
            raise TypeError("Expected argument 'node_to_node_encryption_options' to be a dict")
        pulumi.set(__self__, "node_to_node_encryption_options", node_to_node_encryption_options)
        if off_peak_window_options and not isinstance(off_peak_window_options, dict):
            raise TypeError("Expected argument 'off_peak_window_options' to be a dict")
        pulumi.set(__self__, "off_peak_window_options", off_peak_window_options)
        if service_software_options and not isinstance(service_software_options, dict):
            raise TypeError("Expected argument 'service_software_options' to be a dict")
        pulumi.set(__self__, "service_software_options", service_software_options)
        if skip_shard_migration_wait and not isinstance(skip_shard_migration_wait, bool):
            raise TypeError("Expected argument 'skip_shard_migration_wait' to be a bool")
        pulumi.set(__self__, "skip_shard_migration_wait", skip_shard_migration_wait)
        if snapshot_options and not isinstance(snapshot_options, dict):
            raise TypeError("Expected argument 'snapshot_options' to be a dict")
        pulumi.set(__self__, "snapshot_options", snapshot_options)
        if software_update_options and not isinstance(software_update_options, dict):
            raise TypeError("Expected argument 'software_update_options' to be a dict")
        pulumi.set(__self__, "software_update_options", software_update_options)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_options and not isinstance(vpc_options, dict):
            raise TypeError("Expected argument 'vpc_options' to be a dict")
        pulumi.set(__self__, "vpc_options", vpc_options)

    @property
    @pulumi.getter(name="accessPolicies")
    def access_policies(self) -> Optional[Any]:
        """
        An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions. For more information, see [Configuring access policies](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating) in the *Amazon OpenSearch Service Developer Guide* .

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::OpenSearchService::Domain` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "access_policies")

    @property
    @pulumi.getter(name="advancedOptions")
    def advanced_options(self) -> Optional[Mapping[str, str]]:
        """
        Additional options to specify for the OpenSearch Service domain. For more information, see [AdvancedOptions](https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody) in the OpenSearch Service API reference.
        """
        return pulumi.get(self, "advanced_options")

    @property
    @pulumi.getter(name="advancedSecurityOptions")
    def advanced_security_options(self) -> Optional['outputs.DomainAdvancedSecurityOptionsInput']:
        """
        Specifies options for fine-grained access control and SAML authentication.

        If you specify advanced security options, you must also enable node-to-node encryption ( [NodeToNodeEncryptionOptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html) ) and encryption at rest ( [EncryptionAtRestOptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html) ). You must also enable `EnforceHTTPS` within [DomainEndpointOptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html) , which requires HTTPS for all traffic to the domain.
        """
        return pulumi.get(self, "advanced_security_options")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the CloudFormation stack.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="clusterConfig")
    def cluster_config(self) -> Optional['outputs.DomainClusterConfig']:
        """
        Container for the cluster configuration of a domain.
        """
        return pulumi.get(self, "cluster_config")

    @property
    @pulumi.getter(name="cognitoOptions")
    def cognito_options(self) -> Optional['outputs.DomainCognitoOptions']:
        """
        Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
        """
        return pulumi.get(self, "cognito_options")

    @property
    @pulumi.getter(name="domainArn")
    def domain_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the domain. See [Identifiers for IAM Entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/index.html) in *Using AWS Identity and Access Management* for more information.
        """
        return pulumi.get(self, "domain_arn")

    @property
    @pulumi.getter(name="domainEndpoint")
    def domain_endpoint(self) -> Optional[str]:
        """
        The domain-specific endpoint used for requests to the OpenSearch APIs, such as `search-mystack-1ab2cdefghij-ab1c2deckoyb3hofw7wpqa3cm.us-west-1.es.amazonaws.com` .
        """
        return pulumi.get(self, "domain_endpoint")

    @property
    @pulumi.getter(name="domainEndpointOptions")
    def domain_endpoint_options(self) -> Optional['outputs.DomainEndpointOptions']:
        """
        Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
        """
        return pulumi.get(self, "domain_endpoint_options")

    @property
    @pulumi.getter(name="domainEndpointV2")
    def domain_endpoint_v2(self) -> Optional[str]:
        """
        If `IPAddressType` to set to `dualstack` , a version 2 domain endpoint is provisioned. This endpoint functions like a normal endpoint, except that it works with both IPv4 and IPv6 IP addresses. Normal endpoints work only with IPv4 IP addresses.
        """
        return pulumi.get(self, "domain_endpoint_v2")

    @property
    @pulumi.getter(name="domainEndpoints")
    def domain_endpoints(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "domain_endpoints")

    @property
    @pulumi.getter(name="ebsOptions")
    def ebs_options(self) -> Optional['outputs.DomainEbsOptions']:
        """
        The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain. For more information, see [EBS volume size limits](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource) in the *Amazon OpenSearch Service Developer Guide* .
        """
        return pulumi.get(self, "ebs_options")

    @property
    @pulumi.getter(name="encryptionAtRestOptions")
    def encryption_at_rest_options(self) -> Optional['outputs.DomainEncryptionAtRestOptions']:
        """
        Whether the domain should encrypt data at rest, and if so, the AWS KMS key to use. See [Encryption of data at rest for Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html) .

        If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.
        """
        return pulumi.get(self, "encryption_at_rest_options")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> Optional[str]:
        """
        The version of OpenSearch to use. The value must be in the format `OpenSearch_X.Y` or `Elasticsearch_X.Y` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see [Supported versions of OpenSearch and Elasticsearch](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version) in the *Amazon OpenSearch Service Developer Guide* .

        If you set the [EnableVersionUpgrade](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain) update policy to `true` , you can update `EngineVersion` without interruption. When `EnableVersionUpgrade` is set to `false` , or is not specified, updating `EngineVersion` results in [replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement) .
        """
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The resource ID. For example, `123456789012/my-domain` .
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="identityCenterOptions")
    def identity_center_options(self) -> Optional['outputs.DomainIdentityCenterOptions']:
        """
        Container for IAM Identity Center Option control for the domain.
        """
        return pulumi.get(self, "identity_center_options")

    @property
    @pulumi.getter(name="ipAddressType")
    def ip_address_type(self) -> Optional[str]:
        """
        Choose either dual stack or IPv4 as your IP address type. Dual stack allows you to share domain resources across IPv4 and IPv6 address types, and is the recommended option. If you set your IP address type to dual stack, you can't change your address type later.
        """
        return pulumi.get(self, "ip_address_type")

    @property
    @pulumi.getter(name="logPublishingOptions")
    def log_publishing_options(self) -> Optional[Mapping[str, 'outputs.DomainLogPublishingOption']]:
        """
        An object with one or more of the following keys: `SEARCH_SLOW_LOGS` , `ES_APPLICATION_LOGS` , `INDEX_SLOW_LOGS` , `AUDIT_LOGS` , depending on the types of logs you want to publish. Each key needs a valid `LogPublishingOption` value. For the full syntax, see the [examples](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples) .
        """
        return pulumi.get(self, "log_publishing_options")

    @property
    @pulumi.getter(name="nodeToNodeEncryptionOptions")
    def node_to_node_encryption_options(self) -> Optional['outputs.DomainNodeToNodeEncryptionOptions']:
        """
        Specifies whether node-to-node encryption is enabled. See [Node-to-node encryption for Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html) .
        """
        return pulumi.get(self, "node_to_node_encryption_options")

    @property
    @pulumi.getter(name="offPeakWindowOptions")
    def off_peak_window_options(self) -> Optional['outputs.DomainOffPeakWindowOptions']:
        """
        Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.
        """
        return pulumi.get(self, "off_peak_window_options")

    @property
    @pulumi.getter(name="serviceSoftwareOptions")
    def service_software_options(self) -> Optional['outputs.DomainServiceSoftwareOptions']:
        return pulumi.get(self, "service_software_options")

    @property
    @pulumi.getter(name="skipShardMigrationWait")
    def skip_shard_migration_wait(self) -> Optional[bool]:
        return pulumi.get(self, "skip_shard_migration_wait")

    @property
    @pulumi.getter(name="snapshotOptions")
    def snapshot_options(self) -> Optional['outputs.DomainSnapshotOptions']:
        """
        *DEPRECATED* . The automated snapshot configuration for the OpenSearch Service domain indexes.
        """
        return pulumi.get(self, "snapshot_options")

    @property
    @pulumi.getter(name="softwareUpdateOptions")
    def software_update_options(self) -> Optional['outputs.DomainSoftwareUpdateOptions']:
        """
        Service software update options for the domain.
        """
        return pulumi.get(self, "software_update_options")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An arbitrary set of tags (key-value pairs) for this Domain.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcOptions")
    def vpc_options(self) -> Optional['outputs.DomainVpcOptions']:
        """
        The virtual private cloud (VPC) configuration for the OpenSearch Service domain. For more information, see [Launching your Amazon OpenSearch Service domains within a VPC](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html) in the *Amazon OpenSearch Service Developer Guide* .

        If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.
        """
        return pulumi.get(self, "vpc_options")


class AwaitableGetDomainResult(GetDomainResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainResult(
            access_policies=self.access_policies,
            advanced_options=self.advanced_options,
            advanced_security_options=self.advanced_security_options,
            arn=self.arn,
            cluster_config=self.cluster_config,
            cognito_options=self.cognito_options,
            domain_arn=self.domain_arn,
            domain_endpoint=self.domain_endpoint,
            domain_endpoint_options=self.domain_endpoint_options,
            domain_endpoint_v2=self.domain_endpoint_v2,
            domain_endpoints=self.domain_endpoints,
            ebs_options=self.ebs_options,
            encryption_at_rest_options=self.encryption_at_rest_options,
            engine_version=self.engine_version,
            id=self.id,
            identity_center_options=self.identity_center_options,
            ip_address_type=self.ip_address_type,
            log_publishing_options=self.log_publishing_options,
            node_to_node_encryption_options=self.node_to_node_encryption_options,
            off_peak_window_options=self.off_peak_window_options,
            service_software_options=self.service_software_options,
            skip_shard_migration_wait=self.skip_shard_migration_wait,
            snapshot_options=self.snapshot_options,
            software_update_options=self.software_update_options,
            tags=self.tags,
            vpc_options=self.vpc_options)


def get_domain(domain_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainResult:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str domain_name: A name for the OpenSearch Service domain. The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see [Name Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html) .
           
           Required when creating a new domain.
           
           > If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:opensearchservice:getDomain', __args__, opts=opts, typ=GetDomainResult).value

    return AwaitableGetDomainResult(
        access_policies=pulumi.get(__ret__, 'access_policies'),
        advanced_options=pulumi.get(__ret__, 'advanced_options'),
        advanced_security_options=pulumi.get(__ret__, 'advanced_security_options'),
        arn=pulumi.get(__ret__, 'arn'),
        cluster_config=pulumi.get(__ret__, 'cluster_config'),
        cognito_options=pulumi.get(__ret__, 'cognito_options'),
        domain_arn=pulumi.get(__ret__, 'domain_arn'),
        domain_endpoint=pulumi.get(__ret__, 'domain_endpoint'),
        domain_endpoint_options=pulumi.get(__ret__, 'domain_endpoint_options'),
        domain_endpoint_v2=pulumi.get(__ret__, 'domain_endpoint_v2'),
        domain_endpoints=pulumi.get(__ret__, 'domain_endpoints'),
        ebs_options=pulumi.get(__ret__, 'ebs_options'),
        encryption_at_rest_options=pulumi.get(__ret__, 'encryption_at_rest_options'),
        engine_version=pulumi.get(__ret__, 'engine_version'),
        id=pulumi.get(__ret__, 'id'),
        identity_center_options=pulumi.get(__ret__, 'identity_center_options'),
        ip_address_type=pulumi.get(__ret__, 'ip_address_type'),
        log_publishing_options=pulumi.get(__ret__, 'log_publishing_options'),
        node_to_node_encryption_options=pulumi.get(__ret__, 'node_to_node_encryption_options'),
        off_peak_window_options=pulumi.get(__ret__, 'off_peak_window_options'),
        service_software_options=pulumi.get(__ret__, 'service_software_options'),
        skip_shard_migration_wait=pulumi.get(__ret__, 'skip_shard_migration_wait'),
        snapshot_options=pulumi.get(__ret__, 'snapshot_options'),
        software_update_options=pulumi.get(__ret__, 'software_update_options'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_options=pulumi.get(__ret__, 'vpc_options'))
def get_domain_output(domain_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDomainResult]:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str domain_name: A name for the OpenSearch Service domain. The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see [Name Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html) .
           
           Required when creating a new domain.
           
           > If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:opensearchservice:getDomain', __args__, opts=opts, typ=GetDomainResult)
    return __ret__.apply(lambda __response__: GetDomainResult(
        access_policies=pulumi.get(__response__, 'access_policies'),
        advanced_options=pulumi.get(__response__, 'advanced_options'),
        advanced_security_options=pulumi.get(__response__, 'advanced_security_options'),
        arn=pulumi.get(__response__, 'arn'),
        cluster_config=pulumi.get(__response__, 'cluster_config'),
        cognito_options=pulumi.get(__response__, 'cognito_options'),
        domain_arn=pulumi.get(__response__, 'domain_arn'),
        domain_endpoint=pulumi.get(__response__, 'domain_endpoint'),
        domain_endpoint_options=pulumi.get(__response__, 'domain_endpoint_options'),
        domain_endpoint_v2=pulumi.get(__response__, 'domain_endpoint_v2'),
        domain_endpoints=pulumi.get(__response__, 'domain_endpoints'),
        ebs_options=pulumi.get(__response__, 'ebs_options'),
        encryption_at_rest_options=pulumi.get(__response__, 'encryption_at_rest_options'),
        engine_version=pulumi.get(__response__, 'engine_version'),
        id=pulumi.get(__response__, 'id'),
        identity_center_options=pulumi.get(__response__, 'identity_center_options'),
        ip_address_type=pulumi.get(__response__, 'ip_address_type'),
        log_publishing_options=pulumi.get(__response__, 'log_publishing_options'),
        node_to_node_encryption_options=pulumi.get(__response__, 'node_to_node_encryption_options'),
        off_peak_window_options=pulumi.get(__response__, 'off_peak_window_options'),
        service_software_options=pulumi.get(__response__, 'service_software_options'),
        skip_shard_migration_wait=pulumi.get(__response__, 'skip_shard_migration_wait'),
        snapshot_options=pulumi.get(__response__, 'snapshot_options'),
        software_update_options=pulumi.get(__response__, 'software_update_options'),
        tags=pulumi.get(__response__, 'tags'),
        vpc_options=pulumi.get(__response__, 'vpc_options')))
