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
    'GetIndexResult',
    'AwaitableGetIndexResult',
    'get_index',
    'get_index_output',
]

@pulumi.output_type
class GetIndexResult:
    def __init__(__self__, arn=None, capacity_units=None, description=None, document_metadata_configurations=None, id=None, name=None, role_arn=None, tags=None, user_context_policy=None, user_token_configurations=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if capacity_units and not isinstance(capacity_units, dict):
            raise TypeError("Expected argument 'capacity_units' to be a dict")
        pulumi.set(__self__, "capacity_units", capacity_units)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if document_metadata_configurations and not isinstance(document_metadata_configurations, list):
            raise TypeError("Expected argument 'document_metadata_configurations' to be a list")
        pulumi.set(__self__, "document_metadata_configurations", document_metadata_configurations)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if user_context_policy and not isinstance(user_context_policy, str):
            raise TypeError("Expected argument 'user_context_policy' to be a str")
        pulumi.set(__self__, "user_context_policy", user_context_policy)
        if user_token_configurations and not isinstance(user_token_configurations, list):
            raise TypeError("Expected argument 'user_token_configurations' to be a list")
        pulumi.set(__self__, "user_token_configurations", user_token_configurations)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the index. For example: `arn:aws:kendra:us-west-2:111122223333:index/0123456789abcdef` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="capacityUnits")
    def capacity_units(self) -> Optional['outputs.IndexCapacityUnitsConfiguration']:
        """
        Capacity units
        """
        return pulumi.get(self, "capacity_units")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the index
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentMetadataConfigurations")
    def document_metadata_configurations(self) -> Optional[Sequence['outputs.IndexDocumentMetadataConfiguration']]:
        """
        Document metadata configurations
        """
        return pulumi.get(self, "document_metadata_configurations")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The identifier for the index. For example: `f4aeaa10-8056-4b2c-a343-522ca0f41234` .
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the index.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        """
        An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics. This is also the role used when you use the [BatchPutDocument](https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html) operation to index documents from an Amazon S3 bucket.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Tags for labeling the index
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="userContextPolicy")
    def user_context_policy(self) -> Optional['IndexUserContextPolicy']:
        """
        The user context policy.

        ATTRIBUTE_FILTER

        - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of `_user_id` and `_group_ids` or you can provide user and group information in `UserContext` .

        USER_TOKEN

        - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.
        """
        return pulumi.get(self, "user_context_policy")

    @property
    @pulumi.getter(name="userTokenConfigurations")
    def user_token_configurations(self) -> Optional[Sequence['outputs.IndexUserTokenConfiguration']]:
        """
        Defines the type of user token used for the index.
        """
        return pulumi.get(self, "user_token_configurations")


class AwaitableGetIndexResult(GetIndexResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIndexResult(
            arn=self.arn,
            capacity_units=self.capacity_units,
            description=self.description,
            document_metadata_configurations=self.document_metadata_configurations,
            id=self.id,
            name=self.name,
            role_arn=self.role_arn,
            tags=self.tags,
            user_context_policy=self.user_context_policy,
            user_token_configurations=self.user_token_configurations)


def get_index(id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIndexResult:
    """
    A Kendra index


    :param str id: The identifier for the index. For example: `f4aeaa10-8056-4b2c-a343-522ca0f41234` .
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kendra:getIndex', __args__, opts=opts, typ=GetIndexResult).value

    return AwaitableGetIndexResult(
        arn=pulumi.get(__ret__, 'arn'),
        capacity_units=pulumi.get(__ret__, 'capacity_units'),
        description=pulumi.get(__ret__, 'description'),
        document_metadata_configurations=pulumi.get(__ret__, 'document_metadata_configurations'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        tags=pulumi.get(__ret__, 'tags'),
        user_context_policy=pulumi.get(__ret__, 'user_context_policy'),
        user_token_configurations=pulumi.get(__ret__, 'user_token_configurations'))
def get_index_output(id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIndexResult]:
    """
    A Kendra index


    :param str id: The identifier for the index. For example: `f4aeaa10-8056-4b2c-a343-522ca0f41234` .
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:kendra:getIndex', __args__, opts=opts, typ=GetIndexResult)
    return __ret__.apply(lambda __response__: GetIndexResult(
        arn=pulumi.get(__response__, 'arn'),
        capacity_units=pulumi.get(__response__, 'capacity_units'),
        description=pulumi.get(__response__, 'description'),
        document_metadata_configurations=pulumi.get(__response__, 'document_metadata_configurations'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        role_arn=pulumi.get(__response__, 'role_arn'),
        tags=pulumi.get(__response__, 'tags'),
        user_context_policy=pulumi.get(__response__, 'user_context_policy'),
        user_token_configurations=pulumi.get(__response__, 'user_token_configurations')))
