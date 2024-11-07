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
    'GetMigrationProjectResult',
    'AwaitableGetMigrationProjectResult',
    'get_migration_project',
    'get_migration_project_output',
]

@pulumi.output_type
class GetMigrationProjectResult:
    def __init__(__self__, description=None, instance_profile_arn=None, instance_profile_name=None, migration_project_arn=None, migration_project_creation_time=None, migration_project_name=None, schema_conversion_application_attributes=None, source_data_provider_descriptors=None, tags=None, target_data_provider_descriptors=None, transformation_rules=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if instance_profile_arn and not isinstance(instance_profile_arn, str):
            raise TypeError("Expected argument 'instance_profile_arn' to be a str")
        pulumi.set(__self__, "instance_profile_arn", instance_profile_arn)
        if instance_profile_name and not isinstance(instance_profile_name, str):
            raise TypeError("Expected argument 'instance_profile_name' to be a str")
        pulumi.set(__self__, "instance_profile_name", instance_profile_name)
        if migration_project_arn and not isinstance(migration_project_arn, str):
            raise TypeError("Expected argument 'migration_project_arn' to be a str")
        pulumi.set(__self__, "migration_project_arn", migration_project_arn)
        if migration_project_creation_time and not isinstance(migration_project_creation_time, str):
            raise TypeError("Expected argument 'migration_project_creation_time' to be a str")
        pulumi.set(__self__, "migration_project_creation_time", migration_project_creation_time)
        if migration_project_name and not isinstance(migration_project_name, str):
            raise TypeError("Expected argument 'migration_project_name' to be a str")
        pulumi.set(__self__, "migration_project_name", migration_project_name)
        if schema_conversion_application_attributes and not isinstance(schema_conversion_application_attributes, dict):
            raise TypeError("Expected argument 'schema_conversion_application_attributes' to be a dict")
        pulumi.set(__self__, "schema_conversion_application_attributes", schema_conversion_application_attributes)
        if source_data_provider_descriptors and not isinstance(source_data_provider_descriptors, list):
            raise TypeError("Expected argument 'source_data_provider_descriptors' to be a list")
        pulumi.set(__self__, "source_data_provider_descriptors", source_data_provider_descriptors)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if target_data_provider_descriptors and not isinstance(target_data_provider_descriptors, list):
            raise TypeError("Expected argument 'target_data_provider_descriptors' to be a list")
        pulumi.set(__self__, "target_data_provider_descriptors", target_data_provider_descriptors)
        if transformation_rules and not isinstance(transformation_rules, str):
            raise TypeError("Expected argument 'transformation_rules' to be a str")
        pulumi.set(__self__, "transformation_rules", transformation_rules)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The optional description of the migration project.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="instanceProfileArn")
    def instance_profile_arn(self) -> Optional[str]:
        """
        The property describes an instance profile arn for the migration project. For read
        """
        return pulumi.get(self, "instance_profile_arn")

    @property
    @pulumi.getter(name="instanceProfileName")
    def instance_profile_name(self) -> Optional[str]:
        """
        The property describes an instance profile name for the migration project. For read
        """
        return pulumi.get(self, "instance_profile_name")

    @property
    @pulumi.getter(name="migrationProjectArn")
    def migration_project_arn(self) -> Optional[str]:
        """
        The property describes an ARN of the migration project.
        """
        return pulumi.get(self, "migration_project_arn")

    @property
    @pulumi.getter(name="migrationProjectCreationTime")
    def migration_project_creation_time(self) -> Optional[str]:
        """
        The property describes a creating time of the migration project.
        """
        return pulumi.get(self, "migration_project_creation_time")

    @property
    @pulumi.getter(name="migrationProjectName")
    def migration_project_name(self) -> Optional[str]:
        """
        The property describes a name to identify the migration project.
        """
        return pulumi.get(self, "migration_project_name")

    @property
    @pulumi.getter(name="schemaConversionApplicationAttributes")
    def schema_conversion_application_attributes(self) -> Optional['outputs.SchemaConversionApplicationAttributesProperties']:
        """
        The property describes schema conversion application attributes for the migration project.
        """
        return pulumi.get(self, "schema_conversion_application_attributes")

    @property
    @pulumi.getter(name="sourceDataProviderDescriptors")
    def source_data_provider_descriptors(self) -> Optional[Sequence['outputs.MigrationProjectDataProviderDescriptor']]:
        """
        The property describes source data provider descriptors for the migration project.
        """
        return pulumi.get(self, "source_data_provider_descriptors")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetDataProviderDescriptors")
    def target_data_provider_descriptors(self) -> Optional[Sequence['outputs.MigrationProjectDataProviderDescriptor']]:
        """
        The property describes target data provider descriptors for the migration project.
        """
        return pulumi.get(self, "target_data_provider_descriptors")

    @property
    @pulumi.getter(name="transformationRules")
    def transformation_rules(self) -> Optional[str]:
        """
        The property describes transformation rules for the migration project.
        """
        return pulumi.get(self, "transformation_rules")


class AwaitableGetMigrationProjectResult(GetMigrationProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMigrationProjectResult(
            description=self.description,
            instance_profile_arn=self.instance_profile_arn,
            instance_profile_name=self.instance_profile_name,
            migration_project_arn=self.migration_project_arn,
            migration_project_creation_time=self.migration_project_creation_time,
            migration_project_name=self.migration_project_name,
            schema_conversion_application_attributes=self.schema_conversion_application_attributes,
            source_data_provider_descriptors=self.source_data_provider_descriptors,
            tags=self.tags,
            target_data_provider_descriptors=self.target_data_provider_descriptors,
            transformation_rules=self.transformation_rules)


def get_migration_project(migration_project_arn: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMigrationProjectResult:
    """
    Resource schema for AWS::DMS::MigrationProject


    :param str migration_project_arn: The property describes an ARN of the migration project.
    """
    __args__ = dict()
    __args__['migrationProjectArn'] = migration_project_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:dms:getMigrationProject', __args__, opts=opts, typ=GetMigrationProjectResult).value

    return AwaitableGetMigrationProjectResult(
        description=pulumi.get(__ret__, 'description'),
        instance_profile_arn=pulumi.get(__ret__, 'instance_profile_arn'),
        instance_profile_name=pulumi.get(__ret__, 'instance_profile_name'),
        migration_project_arn=pulumi.get(__ret__, 'migration_project_arn'),
        migration_project_creation_time=pulumi.get(__ret__, 'migration_project_creation_time'),
        migration_project_name=pulumi.get(__ret__, 'migration_project_name'),
        schema_conversion_application_attributes=pulumi.get(__ret__, 'schema_conversion_application_attributes'),
        source_data_provider_descriptors=pulumi.get(__ret__, 'source_data_provider_descriptors'),
        tags=pulumi.get(__ret__, 'tags'),
        target_data_provider_descriptors=pulumi.get(__ret__, 'target_data_provider_descriptors'),
        transformation_rules=pulumi.get(__ret__, 'transformation_rules'))
def get_migration_project_output(migration_project_arn: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMigrationProjectResult]:
    """
    Resource schema for AWS::DMS::MigrationProject


    :param str migration_project_arn: The property describes an ARN of the migration project.
    """
    __args__ = dict()
    __args__['migrationProjectArn'] = migration_project_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:dms:getMigrationProject', __args__, opts=opts, typ=GetMigrationProjectResult)
    return __ret__.apply(lambda __response__: GetMigrationProjectResult(
        description=pulumi.get(__response__, 'description'),
        instance_profile_arn=pulumi.get(__response__, 'instance_profile_arn'),
        instance_profile_name=pulumi.get(__response__, 'instance_profile_name'),
        migration_project_arn=pulumi.get(__response__, 'migration_project_arn'),
        migration_project_creation_time=pulumi.get(__response__, 'migration_project_creation_time'),
        migration_project_name=pulumi.get(__response__, 'migration_project_name'),
        schema_conversion_application_attributes=pulumi.get(__response__, 'schema_conversion_application_attributes'),
        source_data_provider_descriptors=pulumi.get(__response__, 'source_data_provider_descriptors'),
        tags=pulumi.get(__response__, 'tags'),
        target_data_provider_descriptors=pulumi.get(__response__, 'target_data_provider_descriptors'),
        transformation_rules=pulumi.get(__response__, 'transformation_rules')))
