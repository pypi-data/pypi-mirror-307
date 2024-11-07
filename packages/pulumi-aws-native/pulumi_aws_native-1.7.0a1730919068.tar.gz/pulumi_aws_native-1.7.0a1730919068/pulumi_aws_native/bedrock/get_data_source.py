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
    'GetDataSourceResult',
    'AwaitableGetDataSourceResult',
    'get_data_source',
    'get_data_source_output',
]

@pulumi.output_type
class GetDataSourceResult:
    def __init__(__self__, created_at=None, data_deletion_policy=None, data_source_configuration=None, data_source_id=None, data_source_status=None, description=None, failure_reasons=None, name=None, server_side_encryption_configuration=None, updated_at=None, vector_ingestion_configuration=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if data_deletion_policy and not isinstance(data_deletion_policy, str):
            raise TypeError("Expected argument 'data_deletion_policy' to be a str")
        pulumi.set(__self__, "data_deletion_policy", data_deletion_policy)
        if data_source_configuration and not isinstance(data_source_configuration, dict):
            raise TypeError("Expected argument 'data_source_configuration' to be a dict")
        pulumi.set(__self__, "data_source_configuration", data_source_configuration)
        if data_source_id and not isinstance(data_source_id, str):
            raise TypeError("Expected argument 'data_source_id' to be a str")
        pulumi.set(__self__, "data_source_id", data_source_id)
        if data_source_status and not isinstance(data_source_status, str):
            raise TypeError("Expected argument 'data_source_status' to be a str")
        pulumi.set(__self__, "data_source_status", data_source_status)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if failure_reasons and not isinstance(failure_reasons, list):
            raise TypeError("Expected argument 'failure_reasons' to be a list")
        pulumi.set(__self__, "failure_reasons", failure_reasons)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if server_side_encryption_configuration and not isinstance(server_side_encryption_configuration, dict):
            raise TypeError("Expected argument 'server_side_encryption_configuration' to be a dict")
        pulumi.set(__self__, "server_side_encryption_configuration", server_side_encryption_configuration)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if vector_ingestion_configuration and not isinstance(vector_ingestion_configuration, dict):
            raise TypeError("Expected argument 'vector_ingestion_configuration' to be a dict")
        pulumi.set(__self__, "vector_ingestion_configuration", vector_ingestion_configuration)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The time at which the data source was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="dataDeletionPolicy")
    def data_deletion_policy(self) -> Optional['DataSourceDataDeletionPolicy']:
        """
        The data deletion policy for the data source.
        """
        return pulumi.get(self, "data_deletion_policy")

    @property
    @pulumi.getter(name="dataSourceConfiguration")
    def data_source_configuration(self) -> Optional['outputs.DataSourceConfiguration']:
        """
        The connection configuration for the data source.
        """
        return pulumi.get(self, "data_source_configuration")

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> Optional[str]:
        """
        Identifier for a resource.
        """
        return pulumi.get(self, "data_source_id")

    @property
    @pulumi.getter(name="dataSourceStatus")
    def data_source_status(self) -> Optional['DataSourceStatus']:
        """
        The status of the data source. The following statuses are possible:

        - Available – The data source has been created and is ready for ingestion into the knowledge base.
        - Deleting – The data source is being deleted.
        """
        return pulumi.get(self, "data_source_status")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the Resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="failureReasons")
    def failure_reasons(self) -> Optional[Sequence[str]]:
        """
        The details of the failure reasons related to the data source.
        """
        return pulumi.get(self, "failure_reasons")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the data source.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> Optional['outputs.DataSourceServerSideEncryptionConfiguration']:
        """
        Contains details about the configuration of the server-side encryption.
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        The time at which the knowledge base was last updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(self) -> Optional['outputs.DataSourceVectorIngestionConfiguration']:
        """
        Contains details about how to ingest the documents in the data source.
        """
        return pulumi.get(self, "vector_ingestion_configuration")


class AwaitableGetDataSourceResult(GetDataSourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataSourceResult(
            created_at=self.created_at,
            data_deletion_policy=self.data_deletion_policy,
            data_source_configuration=self.data_source_configuration,
            data_source_id=self.data_source_id,
            data_source_status=self.data_source_status,
            description=self.description,
            failure_reasons=self.failure_reasons,
            name=self.name,
            server_side_encryption_configuration=self.server_side_encryption_configuration,
            updated_at=self.updated_at,
            vector_ingestion_configuration=self.vector_ingestion_configuration)


def get_data_source(data_source_id: Optional[str] = None,
                    knowledge_base_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataSourceResult:
    """
    Definition of AWS::Bedrock::DataSource Resource Type


    :param str data_source_id: Identifier for a resource.
    :param str knowledge_base_id: The unique identifier of the knowledge base to which to add the data source.
    """
    __args__ = dict()
    __args__['dataSourceId'] = data_source_id
    __args__['knowledgeBaseId'] = knowledge_base_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:bedrock:getDataSource', __args__, opts=opts, typ=GetDataSourceResult).value

    return AwaitableGetDataSourceResult(
        created_at=pulumi.get(__ret__, 'created_at'),
        data_deletion_policy=pulumi.get(__ret__, 'data_deletion_policy'),
        data_source_configuration=pulumi.get(__ret__, 'data_source_configuration'),
        data_source_id=pulumi.get(__ret__, 'data_source_id'),
        data_source_status=pulumi.get(__ret__, 'data_source_status'),
        description=pulumi.get(__ret__, 'description'),
        failure_reasons=pulumi.get(__ret__, 'failure_reasons'),
        name=pulumi.get(__ret__, 'name'),
        server_side_encryption_configuration=pulumi.get(__ret__, 'server_side_encryption_configuration'),
        updated_at=pulumi.get(__ret__, 'updated_at'),
        vector_ingestion_configuration=pulumi.get(__ret__, 'vector_ingestion_configuration'))
def get_data_source_output(data_source_id: Optional[pulumi.Input[str]] = None,
                           knowledge_base_id: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDataSourceResult]:
    """
    Definition of AWS::Bedrock::DataSource Resource Type


    :param str data_source_id: Identifier for a resource.
    :param str knowledge_base_id: The unique identifier of the knowledge base to which to add the data source.
    """
    __args__ = dict()
    __args__['dataSourceId'] = data_source_id
    __args__['knowledgeBaseId'] = knowledge_base_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:bedrock:getDataSource', __args__, opts=opts, typ=GetDataSourceResult)
    return __ret__.apply(lambda __response__: GetDataSourceResult(
        created_at=pulumi.get(__response__, 'created_at'),
        data_deletion_policy=pulumi.get(__response__, 'data_deletion_policy'),
        data_source_configuration=pulumi.get(__response__, 'data_source_configuration'),
        data_source_id=pulumi.get(__response__, 'data_source_id'),
        data_source_status=pulumi.get(__response__, 'data_source_status'),
        description=pulumi.get(__response__, 'description'),
        failure_reasons=pulumi.get(__response__, 'failure_reasons'),
        name=pulumi.get(__response__, 'name'),
        server_side_encryption_configuration=pulumi.get(__response__, 'server_side_encryption_configuration'),
        updated_at=pulumi.get(__response__, 'updated_at'),
        vector_ingestion_configuration=pulumi.get(__response__, 'vector_ingestion_configuration')))
