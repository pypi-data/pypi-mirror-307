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
from ._enums import *

__all__ = ['SyncConfigurationArgs', 'SyncConfiguration']

@pulumi.input_type
class SyncConfigurationArgs:
    def __init__(__self__, *,
                 branch: pulumi.Input[str],
                 config_file: pulumi.Input[str],
                 repository_link_id: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 role_arn: pulumi.Input[str],
                 sync_type: pulumi.Input[str],
                 publish_deployment_status: Optional[pulumi.Input['SyncConfigurationPublishDeploymentStatus']] = None,
                 trigger_resource_update_on: Optional[pulumi.Input['SyncConfigurationTriggerResourceUpdateOn']] = None):
        """
        The set of arguments for constructing a SyncConfiguration resource.
        :param pulumi.Input[str] branch: The name of the branch of the repository from which resources are to be synchronized,
        :param pulumi.Input[str] config_file: The source provider repository path of the sync configuration file of the respective SyncType.
        :param pulumi.Input[str] repository_link_id: A UUID that uniquely identifies the RepositoryLink that the SyncConfig is associated with.
        :param pulumi.Input[str] resource_name: The name of the resource that is being synchronized to the repository.
        :param pulumi.Input[str] role_arn: The IAM Role that allows AWS to update CloudFormation stacks based on content in the specified repository.
        :param pulumi.Input[str] sync_type: The type of resource synchronization service that is to be configured, for example, CFN_STACK_SYNC.
        :param pulumi.Input['SyncConfigurationPublishDeploymentStatus'] publish_deployment_status: Whether to enable or disable publishing of deployment status to source providers.
        :param pulumi.Input['SyncConfigurationTriggerResourceUpdateOn'] trigger_resource_update_on: When to trigger Git sync to begin the stack update.
        """
        pulumi.set(__self__, "branch", branch)
        pulumi.set(__self__, "config_file", config_file)
        pulumi.set(__self__, "repository_link_id", repository_link_id)
        pulumi.set(__self__, "resource_name", resource_name)
        pulumi.set(__self__, "role_arn", role_arn)
        pulumi.set(__self__, "sync_type", sync_type)
        if publish_deployment_status is not None:
            pulumi.set(__self__, "publish_deployment_status", publish_deployment_status)
        if trigger_resource_update_on is not None:
            pulumi.set(__self__, "trigger_resource_update_on", trigger_resource_update_on)

    @property
    @pulumi.getter
    def branch(self) -> pulumi.Input[str]:
        """
        The name of the branch of the repository from which resources are to be synchronized,
        """
        return pulumi.get(self, "branch")

    @branch.setter
    def branch(self, value: pulumi.Input[str]):
        pulumi.set(self, "branch", value)

    @property
    @pulumi.getter(name="configFile")
    def config_file(self) -> pulumi.Input[str]:
        """
        The source provider repository path of the sync configuration file of the respective SyncType.
        """
        return pulumi.get(self, "config_file")

    @config_file.setter
    def config_file(self, value: pulumi.Input[str]):
        pulumi.set(self, "config_file", value)

    @property
    @pulumi.getter(name="repositoryLinkId")
    def repository_link_id(self) -> pulumi.Input[str]:
        """
        A UUID that uniquely identifies the RepositoryLink that the SyncConfig is associated with.
        """
        return pulumi.get(self, "repository_link_id")

    @repository_link_id.setter
    def repository_link_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "repository_link_id", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the resource that is being synchronized to the repository.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The IAM Role that allows AWS to update CloudFormation stacks based on content in the specified repository.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="syncType")
    def sync_type(self) -> pulumi.Input[str]:
        """
        The type of resource synchronization service that is to be configured, for example, CFN_STACK_SYNC.
        """
        return pulumi.get(self, "sync_type")

    @sync_type.setter
    def sync_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "sync_type", value)

    @property
    @pulumi.getter(name="publishDeploymentStatus")
    def publish_deployment_status(self) -> Optional[pulumi.Input['SyncConfigurationPublishDeploymentStatus']]:
        """
        Whether to enable or disable publishing of deployment status to source providers.
        """
        return pulumi.get(self, "publish_deployment_status")

    @publish_deployment_status.setter
    def publish_deployment_status(self, value: Optional[pulumi.Input['SyncConfigurationPublishDeploymentStatus']]):
        pulumi.set(self, "publish_deployment_status", value)

    @property
    @pulumi.getter(name="triggerResourceUpdateOn")
    def trigger_resource_update_on(self) -> Optional[pulumi.Input['SyncConfigurationTriggerResourceUpdateOn']]:
        """
        When to trigger Git sync to begin the stack update.
        """
        return pulumi.get(self, "trigger_resource_update_on")

    @trigger_resource_update_on.setter
    def trigger_resource_update_on(self, value: Optional[pulumi.Input['SyncConfigurationTriggerResourceUpdateOn']]):
        pulumi.set(self, "trigger_resource_update_on", value)


class SyncConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 branch: Optional[pulumi.Input[str]] = None,
                 config_file: Optional[pulumi.Input[str]] = None,
                 publish_deployment_status: Optional[pulumi.Input['SyncConfigurationPublishDeploymentStatus']] = None,
                 repository_link_id: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 sync_type: Optional[pulumi.Input[str]] = None,
                 trigger_resource_update_on: Optional[pulumi.Input['SyncConfigurationTriggerResourceUpdateOn']] = None,
                 __props__=None):
        """
        Schema for AWS::CodeStarConnections::SyncConfiguration resource which is used to enables an AWS resource to be synchronized from a source-provider.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] branch: The name of the branch of the repository from which resources are to be synchronized,
        :param pulumi.Input[str] config_file: The source provider repository path of the sync configuration file of the respective SyncType.
        :param pulumi.Input['SyncConfigurationPublishDeploymentStatus'] publish_deployment_status: Whether to enable or disable publishing of deployment status to source providers.
        :param pulumi.Input[str] repository_link_id: A UUID that uniquely identifies the RepositoryLink that the SyncConfig is associated with.
        :param pulumi.Input[str] resource_name_: The name of the resource that is being synchronized to the repository.
        :param pulumi.Input[str] role_arn: The IAM Role that allows AWS to update CloudFormation stacks based on content in the specified repository.
        :param pulumi.Input[str] sync_type: The type of resource synchronization service that is to be configured, for example, CFN_STACK_SYNC.
        :param pulumi.Input['SyncConfigurationTriggerResourceUpdateOn'] trigger_resource_update_on: When to trigger Git sync to begin the stack update.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SyncConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schema for AWS::CodeStarConnections::SyncConfiguration resource which is used to enables an AWS resource to be synchronized from a source-provider.

        :param str resource_name: The name of the resource.
        :param SyncConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SyncConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 branch: Optional[pulumi.Input[str]] = None,
                 config_file: Optional[pulumi.Input[str]] = None,
                 publish_deployment_status: Optional[pulumi.Input['SyncConfigurationPublishDeploymentStatus']] = None,
                 repository_link_id: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 sync_type: Optional[pulumi.Input[str]] = None,
                 trigger_resource_update_on: Optional[pulumi.Input['SyncConfigurationTriggerResourceUpdateOn']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SyncConfigurationArgs.__new__(SyncConfigurationArgs)

            if branch is None and not opts.urn:
                raise TypeError("Missing required property 'branch'")
            __props__.__dict__["branch"] = branch
            if config_file is None and not opts.urn:
                raise TypeError("Missing required property 'config_file'")
            __props__.__dict__["config_file"] = config_file
            __props__.__dict__["publish_deployment_status"] = publish_deployment_status
            if repository_link_id is None and not opts.urn:
                raise TypeError("Missing required property 'repository_link_id'")
            __props__.__dict__["repository_link_id"] = repository_link_id
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            if sync_type is None and not opts.urn:
                raise TypeError("Missing required property 'sync_type'")
            __props__.__dict__["sync_type"] = sync_type
            __props__.__dict__["trigger_resource_update_on"] = trigger_resource_update_on
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["provider_type"] = None
            __props__.__dict__["repository_name"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["resourceName", "syncType"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(SyncConfiguration, __self__).__init__(
            'aws-native:codestarconnections:SyncConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SyncConfiguration':
        """
        Get an existing SyncConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SyncConfigurationArgs.__new__(SyncConfigurationArgs)

        __props__.__dict__["branch"] = None
        __props__.__dict__["config_file"] = None
        __props__.__dict__["owner_id"] = None
        __props__.__dict__["provider_type"] = None
        __props__.__dict__["publish_deployment_status"] = None
        __props__.__dict__["repository_link_id"] = None
        __props__.__dict__["repository_name"] = None
        __props__.__dict__["resource_name"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["sync_type"] = None
        __props__.__dict__["trigger_resource_update_on"] = None
        return SyncConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def branch(self) -> pulumi.Output[str]:
        """
        The name of the branch of the repository from which resources are to be synchronized,
        """
        return pulumi.get(self, "branch")

    @property
    @pulumi.getter(name="configFile")
    def config_file(self) -> pulumi.Output[str]:
        """
        The source provider repository path of the sync configuration file of the respective SyncType.
        """
        return pulumi.get(self, "config_file")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        the ID of the entity that owns the repository.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="providerType")
    def provider_type(self) -> pulumi.Output['SyncConfigurationProviderType']:
        """
        The name of the external provider where your third-party code repository is configured.
        """
        return pulumi.get(self, "provider_type")

    @property
    @pulumi.getter(name="publishDeploymentStatus")
    def publish_deployment_status(self) -> pulumi.Output[Optional['SyncConfigurationPublishDeploymentStatus']]:
        """
        Whether to enable or disable publishing of deployment status to source providers.
        """
        return pulumi.get(self, "publish_deployment_status")

    @property
    @pulumi.getter(name="repositoryLinkId")
    def repository_link_id(self) -> pulumi.Output[str]:
        """
        A UUID that uniquely identifies the RepositoryLink that the SyncConfig is associated with.
        """
        return pulumi.get(self, "repository_link_id")

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> pulumi.Output[str]:
        """
        The name of the repository that is being synced to.
        """
        return pulumi.get(self, "repository_name")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Output[str]:
        """
        The name of the resource that is being synchronized to the repository.
        """
        return pulumi.get(self, "resource_name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The IAM Role that allows AWS to update CloudFormation stacks based on content in the specified repository.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="syncType")
    def sync_type(self) -> pulumi.Output[str]:
        """
        The type of resource synchronization service that is to be configured, for example, CFN_STACK_SYNC.
        """
        return pulumi.get(self, "sync_type")

    @property
    @pulumi.getter(name="triggerResourceUpdateOn")
    def trigger_resource_update_on(self) -> pulumi.Output[Optional['SyncConfigurationTriggerResourceUpdateOn']]:
        """
        When to trigger Git sync to begin the stack update.
        """
        return pulumi.get(self, "trigger_resource_update_on")

