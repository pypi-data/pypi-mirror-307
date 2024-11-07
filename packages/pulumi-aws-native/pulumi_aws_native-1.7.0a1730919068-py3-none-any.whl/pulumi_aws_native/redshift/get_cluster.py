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
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    def __init__(__self__, allow_version_upgrade=None, aqua_configuration_status=None, automated_snapshot_retention_period=None, availability_zone=None, availability_zone_relocation=None, availability_zone_relocation_status=None, cluster_namespace_arn=None, cluster_parameter_group_name=None, cluster_security_groups=None, cluster_type=None, cluster_version=None, defer_maintenance_end_time=None, defer_maintenance_identifier=None, defer_maintenance_start_time=None, destination_region=None, elastic_ip=None, encrypted=None, endpoint=None, enhanced_vpc_routing=None, hsm_client_certificate_identifier=None, hsm_configuration_identifier=None, iam_roles=None, kms_key_id=None, logging_properties=None, maintenance_track_name=None, manual_snapshot_retention_period=None, master_password_secret_arn=None, master_password_secret_kms_key_id=None, multi_az=None, namespace_resource_policy=None, node_type=None, number_of_nodes=None, port=None, preferred_maintenance_window=None, publicly_accessible=None, resource_action=None, revision_target=None, rotate_encryption_key=None, snapshot_copy_grant_name=None, snapshot_copy_manual=None, snapshot_copy_retention_period=None, tags=None, vpc_security_group_ids=None):
        if allow_version_upgrade and not isinstance(allow_version_upgrade, bool):
            raise TypeError("Expected argument 'allow_version_upgrade' to be a bool")
        pulumi.set(__self__, "allow_version_upgrade", allow_version_upgrade)
        if aqua_configuration_status and not isinstance(aqua_configuration_status, str):
            raise TypeError("Expected argument 'aqua_configuration_status' to be a str")
        pulumi.set(__self__, "aqua_configuration_status", aqua_configuration_status)
        if automated_snapshot_retention_period and not isinstance(automated_snapshot_retention_period, int):
            raise TypeError("Expected argument 'automated_snapshot_retention_period' to be a int")
        pulumi.set(__self__, "automated_snapshot_retention_period", automated_snapshot_retention_period)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if availability_zone_relocation and not isinstance(availability_zone_relocation, bool):
            raise TypeError("Expected argument 'availability_zone_relocation' to be a bool")
        pulumi.set(__self__, "availability_zone_relocation", availability_zone_relocation)
        if availability_zone_relocation_status and not isinstance(availability_zone_relocation_status, str):
            raise TypeError("Expected argument 'availability_zone_relocation_status' to be a str")
        pulumi.set(__self__, "availability_zone_relocation_status", availability_zone_relocation_status)
        if cluster_namespace_arn and not isinstance(cluster_namespace_arn, str):
            raise TypeError("Expected argument 'cluster_namespace_arn' to be a str")
        pulumi.set(__self__, "cluster_namespace_arn", cluster_namespace_arn)
        if cluster_parameter_group_name and not isinstance(cluster_parameter_group_name, str):
            raise TypeError("Expected argument 'cluster_parameter_group_name' to be a str")
        pulumi.set(__self__, "cluster_parameter_group_name", cluster_parameter_group_name)
        if cluster_security_groups and not isinstance(cluster_security_groups, list):
            raise TypeError("Expected argument 'cluster_security_groups' to be a list")
        pulumi.set(__self__, "cluster_security_groups", cluster_security_groups)
        if cluster_type and not isinstance(cluster_type, str):
            raise TypeError("Expected argument 'cluster_type' to be a str")
        pulumi.set(__self__, "cluster_type", cluster_type)
        if cluster_version and not isinstance(cluster_version, str):
            raise TypeError("Expected argument 'cluster_version' to be a str")
        pulumi.set(__self__, "cluster_version", cluster_version)
        if defer_maintenance_end_time and not isinstance(defer_maintenance_end_time, str):
            raise TypeError("Expected argument 'defer_maintenance_end_time' to be a str")
        pulumi.set(__self__, "defer_maintenance_end_time", defer_maintenance_end_time)
        if defer_maintenance_identifier and not isinstance(defer_maintenance_identifier, str):
            raise TypeError("Expected argument 'defer_maintenance_identifier' to be a str")
        pulumi.set(__self__, "defer_maintenance_identifier", defer_maintenance_identifier)
        if defer_maintenance_start_time and not isinstance(defer_maintenance_start_time, str):
            raise TypeError("Expected argument 'defer_maintenance_start_time' to be a str")
        pulumi.set(__self__, "defer_maintenance_start_time", defer_maintenance_start_time)
        if destination_region and not isinstance(destination_region, str):
            raise TypeError("Expected argument 'destination_region' to be a str")
        pulumi.set(__self__, "destination_region", destination_region)
        if elastic_ip and not isinstance(elastic_ip, str):
            raise TypeError("Expected argument 'elastic_ip' to be a str")
        pulumi.set(__self__, "elastic_ip", elastic_ip)
        if encrypted and not isinstance(encrypted, bool):
            raise TypeError("Expected argument 'encrypted' to be a bool")
        pulumi.set(__self__, "encrypted", encrypted)
        if endpoint and not isinstance(endpoint, dict):
            raise TypeError("Expected argument 'endpoint' to be a dict")
        pulumi.set(__self__, "endpoint", endpoint)
        if enhanced_vpc_routing and not isinstance(enhanced_vpc_routing, bool):
            raise TypeError("Expected argument 'enhanced_vpc_routing' to be a bool")
        pulumi.set(__self__, "enhanced_vpc_routing", enhanced_vpc_routing)
        if hsm_client_certificate_identifier and not isinstance(hsm_client_certificate_identifier, str):
            raise TypeError("Expected argument 'hsm_client_certificate_identifier' to be a str")
        pulumi.set(__self__, "hsm_client_certificate_identifier", hsm_client_certificate_identifier)
        if hsm_configuration_identifier and not isinstance(hsm_configuration_identifier, str):
            raise TypeError("Expected argument 'hsm_configuration_identifier' to be a str")
        pulumi.set(__self__, "hsm_configuration_identifier", hsm_configuration_identifier)
        if iam_roles and not isinstance(iam_roles, list):
            raise TypeError("Expected argument 'iam_roles' to be a list")
        pulumi.set(__self__, "iam_roles", iam_roles)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if logging_properties and not isinstance(logging_properties, dict):
            raise TypeError("Expected argument 'logging_properties' to be a dict")
        pulumi.set(__self__, "logging_properties", logging_properties)
        if maintenance_track_name and not isinstance(maintenance_track_name, str):
            raise TypeError("Expected argument 'maintenance_track_name' to be a str")
        pulumi.set(__self__, "maintenance_track_name", maintenance_track_name)
        if manual_snapshot_retention_period and not isinstance(manual_snapshot_retention_period, int):
            raise TypeError("Expected argument 'manual_snapshot_retention_period' to be a int")
        pulumi.set(__self__, "manual_snapshot_retention_period", manual_snapshot_retention_period)
        if master_password_secret_arn and not isinstance(master_password_secret_arn, str):
            raise TypeError("Expected argument 'master_password_secret_arn' to be a str")
        pulumi.set(__self__, "master_password_secret_arn", master_password_secret_arn)
        if master_password_secret_kms_key_id and not isinstance(master_password_secret_kms_key_id, str):
            raise TypeError("Expected argument 'master_password_secret_kms_key_id' to be a str")
        pulumi.set(__self__, "master_password_secret_kms_key_id", master_password_secret_kms_key_id)
        if multi_az and not isinstance(multi_az, bool):
            raise TypeError("Expected argument 'multi_az' to be a bool")
        pulumi.set(__self__, "multi_az", multi_az)
        if namespace_resource_policy and not isinstance(namespace_resource_policy, dict):
            raise TypeError("Expected argument 'namespace_resource_policy' to be a dict")
        pulumi.set(__self__, "namespace_resource_policy", namespace_resource_policy)
        if node_type and not isinstance(node_type, str):
            raise TypeError("Expected argument 'node_type' to be a str")
        pulumi.set(__self__, "node_type", node_type)
        if number_of_nodes and not isinstance(number_of_nodes, int):
            raise TypeError("Expected argument 'number_of_nodes' to be a int")
        pulumi.set(__self__, "number_of_nodes", number_of_nodes)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if preferred_maintenance_window and not isinstance(preferred_maintenance_window, str):
            raise TypeError("Expected argument 'preferred_maintenance_window' to be a str")
        pulumi.set(__self__, "preferred_maintenance_window", preferred_maintenance_window)
        if publicly_accessible and not isinstance(publicly_accessible, bool):
            raise TypeError("Expected argument 'publicly_accessible' to be a bool")
        pulumi.set(__self__, "publicly_accessible", publicly_accessible)
        if resource_action and not isinstance(resource_action, str):
            raise TypeError("Expected argument 'resource_action' to be a str")
        pulumi.set(__self__, "resource_action", resource_action)
        if revision_target and not isinstance(revision_target, str):
            raise TypeError("Expected argument 'revision_target' to be a str")
        pulumi.set(__self__, "revision_target", revision_target)
        if rotate_encryption_key and not isinstance(rotate_encryption_key, bool):
            raise TypeError("Expected argument 'rotate_encryption_key' to be a bool")
        pulumi.set(__self__, "rotate_encryption_key", rotate_encryption_key)
        if snapshot_copy_grant_name and not isinstance(snapshot_copy_grant_name, str):
            raise TypeError("Expected argument 'snapshot_copy_grant_name' to be a str")
        pulumi.set(__self__, "snapshot_copy_grant_name", snapshot_copy_grant_name)
        if snapshot_copy_manual and not isinstance(snapshot_copy_manual, bool):
            raise TypeError("Expected argument 'snapshot_copy_manual' to be a bool")
        pulumi.set(__self__, "snapshot_copy_manual", snapshot_copy_manual)
        if snapshot_copy_retention_period and not isinstance(snapshot_copy_retention_period, int):
            raise TypeError("Expected argument 'snapshot_copy_retention_period' to be a int")
        pulumi.set(__self__, "snapshot_copy_retention_period", snapshot_copy_retention_period)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError("Expected argument 'vpc_security_group_ids' to be a list")
        pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)

    @property
    @pulumi.getter(name="allowVersionUpgrade")
    def allow_version_upgrade(self) -> Optional[bool]:
        """
        Major version upgrades can be applied during the maintenance window to the Amazon Redshift engine that is running on the cluster. Default value is True
        """
        return pulumi.get(self, "allow_version_upgrade")

    @property
    @pulumi.getter(name="aquaConfigurationStatus")
    def aqua_configuration_status(self) -> Optional[str]:
        """
        The value represents how the cluster is configured to use AQUA (Advanced Query Accelerator) after the cluster is restored. Possible values include the following.

        enabled - Use AQUA if it is available for the current Region and Amazon Redshift node type.
        disabled - Don't use AQUA.
        auto - Amazon Redshift determines whether to use AQUA.
        """
        return pulumi.get(self, "aqua_configuration_status")

    @property
    @pulumi.getter(name="automatedSnapshotRetentionPeriod")
    def automated_snapshot_retention_period(self) -> Optional[int]:
        """
        The number of days that automated snapshots are retained. If the value is 0, automated snapshots are disabled. Default value is 1
        """
        return pulumi.get(self, "automated_snapshot_retention_period")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        The EC2 Availability Zone (AZ) in which you want Amazon Redshift to provision the cluster. Default: A random, system-chosen Availability Zone in the region that is specified by the endpoint
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="availabilityZoneRelocation")
    def availability_zone_relocation(self) -> Optional[bool]:
        """
        The option to enable relocation for an Amazon Redshift cluster between Availability Zones after the cluster modification is complete.
        """
        return pulumi.get(self, "availability_zone_relocation")

    @property
    @pulumi.getter(name="availabilityZoneRelocationStatus")
    def availability_zone_relocation_status(self) -> Optional[str]:
        """
        The availability zone relocation status of the cluster
        """
        return pulumi.get(self, "availability_zone_relocation_status")

    @property
    @pulumi.getter(name="clusterNamespaceArn")
    def cluster_namespace_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the cluster namespace.
        """
        return pulumi.get(self, "cluster_namespace_arn")

    @property
    @pulumi.getter(name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> Optional[str]:
        """
        The name of the parameter group to be associated with this cluster.
        """
        return pulumi.get(self, "cluster_parameter_group_name")

    @property
    @pulumi.getter(name="clusterSecurityGroups")
    def cluster_security_groups(self) -> Optional[Sequence[str]]:
        """
        A list of security groups to be associated with this cluster.
        """
        return pulumi.get(self, "cluster_security_groups")

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> Optional[str]:
        """
        The type of the cluster. When cluster type is specified as single-node, the NumberOfNodes parameter is not required and if multi-node, the NumberOfNodes parameter is required
        """
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="clusterVersion")
    def cluster_version(self) -> Optional[str]:
        """
        The version of the Amazon Redshift engine software that you want to deploy on the cluster.The version selected runs on all the nodes in the cluster.
        """
        return pulumi.get(self, "cluster_version")

    @property
    @pulumi.getter(name="deferMaintenanceEndTime")
    def defer_maintenance_end_time(self) -> Optional[str]:
        """
        A timestamp indicating end time for the deferred maintenance window. If you specify an end time, you can't specify a duration.
        """
        return pulumi.get(self, "defer_maintenance_end_time")

    @property
    @pulumi.getter(name="deferMaintenanceIdentifier")
    def defer_maintenance_identifier(self) -> Optional[str]:
        """
        A unique identifier for the deferred maintenance window.
        """
        return pulumi.get(self, "defer_maintenance_identifier")

    @property
    @pulumi.getter(name="deferMaintenanceStartTime")
    def defer_maintenance_start_time(self) -> Optional[str]:
        """
        A timestamp indicating the start time for the deferred maintenance window.
        """
        return pulumi.get(self, "defer_maintenance_start_time")

    @property
    @pulumi.getter(name="destinationRegion")
    def destination_region(self) -> Optional[str]:
        """
        The destination AWS Region that you want to copy snapshots to. Constraints: Must be the name of a valid AWS Region. For more information, see Regions and Endpoints in the Amazon Web Services [https://docs.aws.amazon.com/general/latest/gr/rande.html#redshift_region] General Reference
        """
        return pulumi.get(self, "destination_region")

    @property
    @pulumi.getter(name="elasticIp")
    def elastic_ip(self) -> Optional[str]:
        """
        The Elastic IP (EIP) address for the cluster.
        """
        return pulumi.get(self, "elastic_ip")

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[bool]:
        """
        If true, the data in the cluster is encrypted at rest.
        """
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter
    def endpoint(self) -> Optional['outputs.ClusterEndpoint']:
        """
        The connection endpoint.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="enhancedVpcRouting")
    def enhanced_vpc_routing(self) -> Optional[bool]:
        """
        An option that specifies whether to create the cluster with enhanced VPC routing enabled. To create a cluster that uses enhanced VPC routing, the cluster must be in a VPC. For more information, see Enhanced VPC Routing in the Amazon Redshift Cluster Management Guide.

        If this option is true , enhanced VPC routing is enabled.

        Default: false
        """
        return pulumi.get(self, "enhanced_vpc_routing")

    @property
    @pulumi.getter(name="hsmClientCertificateIdentifier")
    def hsm_client_certificate_identifier(self) -> Optional[str]:
        """
        Specifies the name of the HSM client certificate the Amazon Redshift cluster uses to retrieve the data encryption keys stored in an HSM
        """
        return pulumi.get(self, "hsm_client_certificate_identifier")

    @property
    @pulumi.getter(name="hsmConfigurationIdentifier")
    def hsm_configuration_identifier(self) -> Optional[str]:
        """
        Specifies the name of the HSM configuration that contains the information the Amazon Redshift cluster can use to retrieve and store keys in an HSM.
        """
        return pulumi.get(self, "hsm_configuration_identifier")

    @property
    @pulumi.getter(name="iamRoles")
    def iam_roles(self) -> Optional[Sequence[str]]:
        """
        A list of AWS Identity and Access Management (IAM) roles that can be used by the cluster to access other AWS services. You must supply the IAM roles in their Amazon Resource Name (ARN) format. You can supply up to 50 IAM roles in a single request
        """
        return pulumi.get(self, "iam_roles")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        """
        The AWS Key Management Service (KMS) key ID of the encryption key that you want to use to encrypt data in the cluster.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="loggingProperties")
    def logging_properties(self) -> Optional['outputs.ClusterLoggingProperties']:
        """
        Specifies logging information, such as queries and connection attempts, for the specified Amazon Redshift cluster.
        """
        return pulumi.get(self, "logging_properties")

    @property
    @pulumi.getter(name="maintenanceTrackName")
    def maintenance_track_name(self) -> Optional[str]:
        """
        The name for the maintenance track that you want to assign for the cluster. This name change is asynchronous. The new track name stays in the PendingModifiedValues for the cluster until the next maintenance window. When the maintenance track changes, the cluster is switched to the latest cluster release available for the maintenance track. At this point, the maintenance track name is applied.
        """
        return pulumi.get(self, "maintenance_track_name")

    @property
    @pulumi.getter(name="manualSnapshotRetentionPeriod")
    def manual_snapshot_retention_period(self) -> Optional[int]:
        """
        The number of days to retain newly copied snapshots in the destination AWS Region after they are copied from the source AWS Region. If the value is -1, the manual snapshot is retained indefinitely.

        The value must be either -1 or an integer between 1 and 3,653.
        """
        return pulumi.get(self, "manual_snapshot_retention_period")

    @property
    @pulumi.getter(name="masterPasswordSecretArn")
    def master_password_secret_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the cluster's admin user credentials secret.
        """
        return pulumi.get(self, "master_password_secret_arn")

    @property
    @pulumi.getter(name="masterPasswordSecretKmsKeyId")
    def master_password_secret_kms_key_id(self) -> Optional[str]:
        """
        The ID of the Key Management Service (KMS) key used to encrypt and store the cluster's admin user credentials secret.
        """
        return pulumi.get(self, "master_password_secret_kms_key_id")

    @property
    @pulumi.getter(name="multiAz")
    def multi_az(self) -> Optional[bool]:
        """
        A boolean indicating if the redshift cluster is multi-az or not. If you don't provide this parameter or set the value to false, the redshift cluster will be single-az.
        """
        return pulumi.get(self, "multi_az")

    @property
    @pulumi.getter(name="namespaceResourcePolicy")
    def namespace_resource_policy(self) -> Optional[Any]:
        """
        The namespace resource policy document that will be attached to a Redshift cluster.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Redshift::Cluster` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "namespace_resource_policy")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> Optional[str]:
        """
        The node type to be provisioned for the cluster.Valid Values: ds2.xlarge | ds2.8xlarge | dc1.large | dc1.8xlarge | dc2.large | dc2.8xlarge | ra3.4xlarge | ra3.16xlarge
        """
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="numberOfNodes")
    def number_of_nodes(self) -> Optional[int]:
        """
        The number of compute nodes in the cluster. This parameter is required when the ClusterType parameter is specified as multi-node.
        """
        return pulumi.get(self, "number_of_nodes")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        The port number on which the cluster accepts incoming connections. The cluster is accessible only via the JDBC and ODBC connection strings
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> Optional[str]:
        """
        The weekly time range (in UTC) during which automated cluster maintenance can occur.
        """
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="publiclyAccessible")
    def publicly_accessible(self) -> Optional[bool]:
        """
        If true, the cluster can be accessed from a public network.
        """
        return pulumi.get(self, "publicly_accessible")

    @property
    @pulumi.getter(name="resourceAction")
    def resource_action(self) -> Optional[str]:
        """
        The Redshift operation to be performed. Resource Action supports pause-cluster, resume-cluster, failover-primary-compute APIs
        """
        return pulumi.get(self, "resource_action")

    @property
    @pulumi.getter(name="revisionTarget")
    def revision_target(self) -> Optional[str]:
        """
        The identifier of the database revision. You can retrieve this value from the response to the DescribeClusterDbRevisions request.
        """
        return pulumi.get(self, "revision_target")

    @property
    @pulumi.getter(name="rotateEncryptionKey")
    def rotate_encryption_key(self) -> Optional[bool]:
        """
        A boolean indicating if we want to rotate Encryption Keys.
        """
        return pulumi.get(self, "rotate_encryption_key")

    @property
    @pulumi.getter(name="snapshotCopyGrantName")
    def snapshot_copy_grant_name(self) -> Optional[str]:
        """
        The name of the snapshot copy grant to use when snapshots of an AWS KMS-encrypted cluster are copied to the destination region.
        """
        return pulumi.get(self, "snapshot_copy_grant_name")

    @property
    @pulumi.getter(name="snapshotCopyManual")
    def snapshot_copy_manual(self) -> Optional[bool]:
        """
        Indicates whether to apply the snapshot retention period to newly copied manual snapshots instead of automated snapshots.
        """
        return pulumi.get(self, "snapshot_copy_manual")

    @property
    @pulumi.getter(name="snapshotCopyRetentionPeriod")
    def snapshot_copy_retention_period(self) -> Optional[int]:
        """
        The number of days to retain automated snapshots in the destination region after they are copied from the source region. 

         Default is 7. 

         Constraints: Must be at least 1 and no more than 35.
        """
        return pulumi.get(self, "snapshot_copy_retention_period")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The list of tags for the cluster parameter group.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Optional[Sequence[str]]:
        """
        A list of Virtual Private Cloud (VPC) security groups to be associated with the cluster.
        """
        return pulumi.get(self, "vpc_security_group_ids")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            allow_version_upgrade=self.allow_version_upgrade,
            aqua_configuration_status=self.aqua_configuration_status,
            automated_snapshot_retention_period=self.automated_snapshot_retention_period,
            availability_zone=self.availability_zone,
            availability_zone_relocation=self.availability_zone_relocation,
            availability_zone_relocation_status=self.availability_zone_relocation_status,
            cluster_namespace_arn=self.cluster_namespace_arn,
            cluster_parameter_group_name=self.cluster_parameter_group_name,
            cluster_security_groups=self.cluster_security_groups,
            cluster_type=self.cluster_type,
            cluster_version=self.cluster_version,
            defer_maintenance_end_time=self.defer_maintenance_end_time,
            defer_maintenance_identifier=self.defer_maintenance_identifier,
            defer_maintenance_start_time=self.defer_maintenance_start_time,
            destination_region=self.destination_region,
            elastic_ip=self.elastic_ip,
            encrypted=self.encrypted,
            endpoint=self.endpoint,
            enhanced_vpc_routing=self.enhanced_vpc_routing,
            hsm_client_certificate_identifier=self.hsm_client_certificate_identifier,
            hsm_configuration_identifier=self.hsm_configuration_identifier,
            iam_roles=self.iam_roles,
            kms_key_id=self.kms_key_id,
            logging_properties=self.logging_properties,
            maintenance_track_name=self.maintenance_track_name,
            manual_snapshot_retention_period=self.manual_snapshot_retention_period,
            master_password_secret_arn=self.master_password_secret_arn,
            master_password_secret_kms_key_id=self.master_password_secret_kms_key_id,
            multi_az=self.multi_az,
            namespace_resource_policy=self.namespace_resource_policy,
            node_type=self.node_type,
            number_of_nodes=self.number_of_nodes,
            port=self.port,
            preferred_maintenance_window=self.preferred_maintenance_window,
            publicly_accessible=self.publicly_accessible,
            resource_action=self.resource_action,
            revision_target=self.revision_target,
            rotate_encryption_key=self.rotate_encryption_key,
            snapshot_copy_grant_name=self.snapshot_copy_grant_name,
            snapshot_copy_manual=self.snapshot_copy_manual,
            snapshot_copy_retention_period=self.snapshot_copy_retention_period,
            tags=self.tags,
            vpc_security_group_ids=self.vpc_security_group_ids)


def get_cluster(cluster_identifier: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str cluster_identifier: A unique identifier for the cluster. You use this identifier to refer to the cluster for any subsequent cluster operations such as deleting or modifying. All alphabetical characters must be lower case, no hypens at the end, no two consecutive hyphens. Cluster name should be unique for all clusters within an AWS account
    """
    __args__ = dict()
    __args__['clusterIdentifier'] = cluster_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:redshift:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        allow_version_upgrade=pulumi.get(__ret__, 'allow_version_upgrade'),
        aqua_configuration_status=pulumi.get(__ret__, 'aqua_configuration_status'),
        automated_snapshot_retention_period=pulumi.get(__ret__, 'automated_snapshot_retention_period'),
        availability_zone=pulumi.get(__ret__, 'availability_zone'),
        availability_zone_relocation=pulumi.get(__ret__, 'availability_zone_relocation'),
        availability_zone_relocation_status=pulumi.get(__ret__, 'availability_zone_relocation_status'),
        cluster_namespace_arn=pulumi.get(__ret__, 'cluster_namespace_arn'),
        cluster_parameter_group_name=pulumi.get(__ret__, 'cluster_parameter_group_name'),
        cluster_security_groups=pulumi.get(__ret__, 'cluster_security_groups'),
        cluster_type=pulumi.get(__ret__, 'cluster_type'),
        cluster_version=pulumi.get(__ret__, 'cluster_version'),
        defer_maintenance_end_time=pulumi.get(__ret__, 'defer_maintenance_end_time'),
        defer_maintenance_identifier=pulumi.get(__ret__, 'defer_maintenance_identifier'),
        defer_maintenance_start_time=pulumi.get(__ret__, 'defer_maintenance_start_time'),
        destination_region=pulumi.get(__ret__, 'destination_region'),
        elastic_ip=pulumi.get(__ret__, 'elastic_ip'),
        encrypted=pulumi.get(__ret__, 'encrypted'),
        endpoint=pulumi.get(__ret__, 'endpoint'),
        enhanced_vpc_routing=pulumi.get(__ret__, 'enhanced_vpc_routing'),
        hsm_client_certificate_identifier=pulumi.get(__ret__, 'hsm_client_certificate_identifier'),
        hsm_configuration_identifier=pulumi.get(__ret__, 'hsm_configuration_identifier'),
        iam_roles=pulumi.get(__ret__, 'iam_roles'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        logging_properties=pulumi.get(__ret__, 'logging_properties'),
        maintenance_track_name=pulumi.get(__ret__, 'maintenance_track_name'),
        manual_snapshot_retention_period=pulumi.get(__ret__, 'manual_snapshot_retention_period'),
        master_password_secret_arn=pulumi.get(__ret__, 'master_password_secret_arn'),
        master_password_secret_kms_key_id=pulumi.get(__ret__, 'master_password_secret_kms_key_id'),
        multi_az=pulumi.get(__ret__, 'multi_az'),
        namespace_resource_policy=pulumi.get(__ret__, 'namespace_resource_policy'),
        node_type=pulumi.get(__ret__, 'node_type'),
        number_of_nodes=pulumi.get(__ret__, 'number_of_nodes'),
        port=pulumi.get(__ret__, 'port'),
        preferred_maintenance_window=pulumi.get(__ret__, 'preferred_maintenance_window'),
        publicly_accessible=pulumi.get(__ret__, 'publicly_accessible'),
        resource_action=pulumi.get(__ret__, 'resource_action'),
        revision_target=pulumi.get(__ret__, 'revision_target'),
        rotate_encryption_key=pulumi.get(__ret__, 'rotate_encryption_key'),
        snapshot_copy_grant_name=pulumi.get(__ret__, 'snapshot_copy_grant_name'),
        snapshot_copy_manual=pulumi.get(__ret__, 'snapshot_copy_manual'),
        snapshot_copy_retention_period=pulumi.get(__ret__, 'snapshot_copy_retention_period'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_security_group_ids=pulumi.get(__ret__, 'vpc_security_group_ids'))
def get_cluster_output(cluster_identifier: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str cluster_identifier: A unique identifier for the cluster. You use this identifier to refer to the cluster for any subsequent cluster operations such as deleting or modifying. All alphabetical characters must be lower case, no hypens at the end, no two consecutive hyphens. Cluster name should be unique for all clusters within an AWS account
    """
    __args__ = dict()
    __args__['clusterIdentifier'] = cluster_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:redshift:getCluster', __args__, opts=opts, typ=GetClusterResult)
    return __ret__.apply(lambda __response__: GetClusterResult(
        allow_version_upgrade=pulumi.get(__response__, 'allow_version_upgrade'),
        aqua_configuration_status=pulumi.get(__response__, 'aqua_configuration_status'),
        automated_snapshot_retention_period=pulumi.get(__response__, 'automated_snapshot_retention_period'),
        availability_zone=pulumi.get(__response__, 'availability_zone'),
        availability_zone_relocation=pulumi.get(__response__, 'availability_zone_relocation'),
        availability_zone_relocation_status=pulumi.get(__response__, 'availability_zone_relocation_status'),
        cluster_namespace_arn=pulumi.get(__response__, 'cluster_namespace_arn'),
        cluster_parameter_group_name=pulumi.get(__response__, 'cluster_parameter_group_name'),
        cluster_security_groups=pulumi.get(__response__, 'cluster_security_groups'),
        cluster_type=pulumi.get(__response__, 'cluster_type'),
        cluster_version=pulumi.get(__response__, 'cluster_version'),
        defer_maintenance_end_time=pulumi.get(__response__, 'defer_maintenance_end_time'),
        defer_maintenance_identifier=pulumi.get(__response__, 'defer_maintenance_identifier'),
        defer_maintenance_start_time=pulumi.get(__response__, 'defer_maintenance_start_time'),
        destination_region=pulumi.get(__response__, 'destination_region'),
        elastic_ip=pulumi.get(__response__, 'elastic_ip'),
        encrypted=pulumi.get(__response__, 'encrypted'),
        endpoint=pulumi.get(__response__, 'endpoint'),
        enhanced_vpc_routing=pulumi.get(__response__, 'enhanced_vpc_routing'),
        hsm_client_certificate_identifier=pulumi.get(__response__, 'hsm_client_certificate_identifier'),
        hsm_configuration_identifier=pulumi.get(__response__, 'hsm_configuration_identifier'),
        iam_roles=pulumi.get(__response__, 'iam_roles'),
        kms_key_id=pulumi.get(__response__, 'kms_key_id'),
        logging_properties=pulumi.get(__response__, 'logging_properties'),
        maintenance_track_name=pulumi.get(__response__, 'maintenance_track_name'),
        manual_snapshot_retention_period=pulumi.get(__response__, 'manual_snapshot_retention_period'),
        master_password_secret_arn=pulumi.get(__response__, 'master_password_secret_arn'),
        master_password_secret_kms_key_id=pulumi.get(__response__, 'master_password_secret_kms_key_id'),
        multi_az=pulumi.get(__response__, 'multi_az'),
        namespace_resource_policy=pulumi.get(__response__, 'namespace_resource_policy'),
        node_type=pulumi.get(__response__, 'node_type'),
        number_of_nodes=pulumi.get(__response__, 'number_of_nodes'),
        port=pulumi.get(__response__, 'port'),
        preferred_maintenance_window=pulumi.get(__response__, 'preferred_maintenance_window'),
        publicly_accessible=pulumi.get(__response__, 'publicly_accessible'),
        resource_action=pulumi.get(__response__, 'resource_action'),
        revision_target=pulumi.get(__response__, 'revision_target'),
        rotate_encryption_key=pulumi.get(__response__, 'rotate_encryption_key'),
        snapshot_copy_grant_name=pulumi.get(__response__, 'snapshot_copy_grant_name'),
        snapshot_copy_manual=pulumi.get(__response__, 'snapshot_copy_manual'),
        snapshot_copy_retention_period=pulumi.get(__response__, 'snapshot_copy_retention_period'),
        tags=pulumi.get(__response__, 'tags'),
        vpc_security_group_ids=pulumi.get(__response__, 'vpc_security_group_ids')))
