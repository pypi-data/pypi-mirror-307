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
    def __init__(__self__, acl_name=None, arn=None, auto_minor_version_upgrade=None, cluster_endpoint=None, description=None, engine=None, engine_version=None, maintenance_window=None, node_type=None, num_replicas_per_shard=None, num_shards=None, parameter_group_name=None, parameter_group_status=None, security_group_ids=None, snapshot_retention_limit=None, snapshot_window=None, sns_topic_arn=None, sns_topic_status=None, status=None, tags=None):
        if acl_name and not isinstance(acl_name, str):
            raise TypeError("Expected argument 'acl_name' to be a str")
        pulumi.set(__self__, "acl_name", acl_name)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auto_minor_version_upgrade and not isinstance(auto_minor_version_upgrade, bool):
            raise TypeError("Expected argument 'auto_minor_version_upgrade' to be a bool")
        pulumi.set(__self__, "auto_minor_version_upgrade", auto_minor_version_upgrade)
        if cluster_endpoint and not isinstance(cluster_endpoint, dict):
            raise TypeError("Expected argument 'cluster_endpoint' to be a dict")
        pulumi.set(__self__, "cluster_endpoint", cluster_endpoint)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        pulumi.set(__self__, "engine", engine)
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        pulumi.set(__self__, "engine_version", engine_version)
        if maintenance_window and not isinstance(maintenance_window, str):
            raise TypeError("Expected argument 'maintenance_window' to be a str")
        pulumi.set(__self__, "maintenance_window", maintenance_window)
        if node_type and not isinstance(node_type, str):
            raise TypeError("Expected argument 'node_type' to be a str")
        pulumi.set(__self__, "node_type", node_type)
        if num_replicas_per_shard and not isinstance(num_replicas_per_shard, int):
            raise TypeError("Expected argument 'num_replicas_per_shard' to be a int")
        pulumi.set(__self__, "num_replicas_per_shard", num_replicas_per_shard)
        if num_shards and not isinstance(num_shards, int):
            raise TypeError("Expected argument 'num_shards' to be a int")
        pulumi.set(__self__, "num_shards", num_shards)
        if parameter_group_name and not isinstance(parameter_group_name, str):
            raise TypeError("Expected argument 'parameter_group_name' to be a str")
        pulumi.set(__self__, "parameter_group_name", parameter_group_name)
        if parameter_group_status and not isinstance(parameter_group_status, str):
            raise TypeError("Expected argument 'parameter_group_status' to be a str")
        pulumi.set(__self__, "parameter_group_status", parameter_group_status)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if snapshot_retention_limit and not isinstance(snapshot_retention_limit, int):
            raise TypeError("Expected argument 'snapshot_retention_limit' to be a int")
        pulumi.set(__self__, "snapshot_retention_limit", snapshot_retention_limit)
        if snapshot_window and not isinstance(snapshot_window, str):
            raise TypeError("Expected argument 'snapshot_window' to be a str")
        pulumi.set(__self__, "snapshot_window", snapshot_window)
        if sns_topic_arn and not isinstance(sns_topic_arn, str):
            raise TypeError("Expected argument 'sns_topic_arn' to be a str")
        pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)
        if sns_topic_status and not isinstance(sns_topic_status, str):
            raise TypeError("Expected argument 'sns_topic_status' to be a str")
        pulumi.set(__self__, "sns_topic_status", sns_topic_status)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="aclName")
    def acl_name(self) -> Optional[str]:
        """
        The name of the Access Control List to associate with the cluster.
        """
        return pulumi.get(self, "acl_name")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the cluster.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(self) -> Optional[bool]:
        """
        A flag that enables automatic minor version upgrade when set to true.

        You cannot modify the value of AutoMinorVersionUpgrade after the cluster is created. To enable AutoMinorVersionUpgrade on a cluster you must set AutoMinorVersionUpgrade to true when you create a cluster.
        """
        return pulumi.get(self, "auto_minor_version_upgrade")

    @property
    @pulumi.getter(name="clusterEndpoint")
    def cluster_endpoint(self) -> Optional['outputs.ClusterEndpoint']:
        """
        The cluster endpoint.
        """
        return pulumi.get(self, "cluster_endpoint")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the cluster.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def engine(self) -> Optional[str]:
        """
        The engine type used by the cluster.
        """
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> Optional[str]:
        """
        The Redis engine version used by the cluster.
        """
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> Optional[str]:
        """
        Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.
        """
        return pulumi.get(self, "maintenance_window")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> Optional[str]:
        """
        The compute and memory capacity of the nodes in the cluster.
        """
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="numReplicasPerShard")
    def num_replicas_per_shard(self) -> Optional[int]:
        """
        The number of replicas to apply to each shard. The limit is 5.
        """
        return pulumi.get(self, "num_replicas_per_shard")

    @property
    @pulumi.getter(name="numShards")
    def num_shards(self) -> Optional[int]:
        """
        The number of shards the cluster will contain.
        """
        return pulumi.get(self, "num_shards")

    @property
    @pulumi.getter(name="parameterGroupName")
    def parameter_group_name(self) -> Optional[str]:
        """
        The name of the parameter group associated with the cluster.
        """
        return pulumi.get(self, "parameter_group_name")

    @property
    @pulumi.getter(name="parameterGroupStatus")
    def parameter_group_status(self) -> Optional[str]:
        """
        The status of the parameter group used by the cluster.
        """
        return pulumi.get(self, "parameter_group_status")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        """
        One or more Amazon VPC security groups associated with this cluster.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> Optional[int]:
        """
        The number of days for which MemoryDB retains automatic snapshots before deleting them. For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.
        """
        return pulumi.get(self, "snapshot_retention_limit")

    @property
    @pulumi.getter(name="snapshotWindow")
    def snapshot_window(self) -> Optional[str]:
        """
        The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your cluster.
        """
        return pulumi.get(self, "snapshot_window")

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.
        """
        return pulumi.get(self, "sns_topic_arn")

    @property
    @pulumi.getter(name="snsTopicStatus")
    def sns_topic_status(self) -> Optional[str]:
        """
        The status of the Amazon SNS notification topic. Notifications are sent only if the status is enabled.
        """
        return pulumi.get(self, "sns_topic_status")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the cluster. For example, Available, Updating, Creating.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this cluster.
        """
        return pulumi.get(self, "tags")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            acl_name=self.acl_name,
            arn=self.arn,
            auto_minor_version_upgrade=self.auto_minor_version_upgrade,
            cluster_endpoint=self.cluster_endpoint,
            description=self.description,
            engine=self.engine,
            engine_version=self.engine_version,
            maintenance_window=self.maintenance_window,
            node_type=self.node_type,
            num_replicas_per_shard=self.num_replicas_per_shard,
            num_shards=self.num_shards,
            parameter_group_name=self.parameter_group_name,
            parameter_group_status=self.parameter_group_status,
            security_group_ids=self.security_group_ids,
            snapshot_retention_limit=self.snapshot_retention_limit,
            snapshot_window=self.snapshot_window,
            sns_topic_arn=self.sns_topic_arn,
            sns_topic_status=self.sns_topic_status,
            status=self.status,
            tags=self.tags)


def get_cluster(cluster_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    The AWS::MemoryDB::Cluster resource creates an Amazon MemoryDB Cluster.


    :param str cluster_name: The name of the cluster. This value must be unique as it also serves as the cluster identifier.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:memorydb:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        acl_name=pulumi.get(__ret__, 'acl_name'),
        arn=pulumi.get(__ret__, 'arn'),
        auto_minor_version_upgrade=pulumi.get(__ret__, 'auto_minor_version_upgrade'),
        cluster_endpoint=pulumi.get(__ret__, 'cluster_endpoint'),
        description=pulumi.get(__ret__, 'description'),
        engine=pulumi.get(__ret__, 'engine'),
        engine_version=pulumi.get(__ret__, 'engine_version'),
        maintenance_window=pulumi.get(__ret__, 'maintenance_window'),
        node_type=pulumi.get(__ret__, 'node_type'),
        num_replicas_per_shard=pulumi.get(__ret__, 'num_replicas_per_shard'),
        num_shards=pulumi.get(__ret__, 'num_shards'),
        parameter_group_name=pulumi.get(__ret__, 'parameter_group_name'),
        parameter_group_status=pulumi.get(__ret__, 'parameter_group_status'),
        security_group_ids=pulumi.get(__ret__, 'security_group_ids'),
        snapshot_retention_limit=pulumi.get(__ret__, 'snapshot_retention_limit'),
        snapshot_window=pulumi.get(__ret__, 'snapshot_window'),
        sns_topic_arn=pulumi.get(__ret__, 'sns_topic_arn'),
        sns_topic_status=pulumi.get(__ret__, 'sns_topic_status'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))
def get_cluster_output(cluster_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    The AWS::MemoryDB::Cluster resource creates an Amazon MemoryDB Cluster.


    :param str cluster_name: The name of the cluster. This value must be unique as it also serves as the cluster identifier.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:memorydb:getCluster', __args__, opts=opts, typ=GetClusterResult)
    return __ret__.apply(lambda __response__: GetClusterResult(
        acl_name=pulumi.get(__response__, 'acl_name'),
        arn=pulumi.get(__response__, 'arn'),
        auto_minor_version_upgrade=pulumi.get(__response__, 'auto_minor_version_upgrade'),
        cluster_endpoint=pulumi.get(__response__, 'cluster_endpoint'),
        description=pulumi.get(__response__, 'description'),
        engine=pulumi.get(__response__, 'engine'),
        engine_version=pulumi.get(__response__, 'engine_version'),
        maintenance_window=pulumi.get(__response__, 'maintenance_window'),
        node_type=pulumi.get(__response__, 'node_type'),
        num_replicas_per_shard=pulumi.get(__response__, 'num_replicas_per_shard'),
        num_shards=pulumi.get(__response__, 'num_shards'),
        parameter_group_name=pulumi.get(__response__, 'parameter_group_name'),
        parameter_group_status=pulumi.get(__response__, 'parameter_group_status'),
        security_group_ids=pulumi.get(__response__, 'security_group_ids'),
        snapshot_retention_limit=pulumi.get(__response__, 'snapshot_retention_limit'),
        snapshot_window=pulumi.get(__response__, 'snapshot_window'),
        sns_topic_arn=pulumi.get(__response__, 'sns_topic_arn'),
        sns_topic_status=pulumi.get(__response__, 'sns_topic_status'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags')))
