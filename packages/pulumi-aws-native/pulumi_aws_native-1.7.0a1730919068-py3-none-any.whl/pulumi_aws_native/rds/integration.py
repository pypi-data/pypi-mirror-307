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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs

__all__ = ['IntegrationArgs', 'Integration']

@pulumi.input_type
class IntegrationArgs:
    def __init__(__self__, *,
                 source_arn: pulumi.Input[str],
                 target_arn: pulumi.Input[str],
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 data_filter: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 integration_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Integration resource.
        :param pulumi.Input[str] source_arn: The Amazon Resource Name (ARN) of the database to use as the source for replication.
        :param pulumi.Input[str] target_arn: The ARN of the Redshift data warehouse to use as the target for replication.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] additional_encryption_context: An optional set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context) in the *Key Management Service Developer Guide*.
                You can only include this parameter if you specify the ``KMSKeyId`` parameter.
        :param pulumi.Input[str] data_filter: Data filters for the integration. These filters determine which tables from the source database are sent to the target Amazon Redshift data warehouse.
        :param pulumi.Input[str] description: A description of the integration.
        :param pulumi.Input[str] integration_name: The name of the integration.
        :param pulumi.Input[str] kms_key_id: The AWS Key Management System (AWS KMS) key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: A list of tags. For more information, see [Tagging Amazon RDS Resources](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html) in the *Amazon RDS User Guide.*.
        """
        pulumi.set(__self__, "source_arn", source_arn)
        pulumi.set(__self__, "target_arn", target_arn)
        if additional_encryption_context is not None:
            pulumi.set(__self__, "additional_encryption_context", additional_encryption_context)
        if data_filter is not None:
            pulumi.set(__self__, "data_filter", data_filter)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if integration_name is not None:
            pulumi.set(__self__, "integration_name", integration_name)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the database to use as the source for replication.
        """
        return pulumi.get(self, "source_arn")

    @source_arn.setter
    def source_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_arn", value)

    @property
    @pulumi.getter(name="targetArn")
    def target_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the Redshift data warehouse to use as the target for replication.
        """
        return pulumi.get(self, "target_arn")

    @target_arn.setter
    def target_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_arn", value)

    @property
    @pulumi.getter(name="additionalEncryptionContext")
    def additional_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        An optional set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context) in the *Key Management Service Developer Guide*.
         You can only include this parameter if you specify the ``KMSKeyId`` parameter.
        """
        return pulumi.get(self, "additional_encryption_context")

    @additional_encryption_context.setter
    def additional_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "additional_encryption_context", value)

    @property
    @pulumi.getter(name="dataFilter")
    def data_filter(self) -> Optional[pulumi.Input[str]]:
        """
        Data filters for the integration. These filters determine which tables from the source database are sent to the target Amazon Redshift data warehouse.
        """
        return pulumi.get(self, "data_filter")

    @data_filter.setter
    def data_filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_filter", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the integration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="integrationName")
    def integration_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the integration.
        """
        return pulumi.get(self, "integration_name")

    @integration_name.setter
    def integration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_name", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS Key Management System (AWS KMS) key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        A list of tags. For more information, see [Tagging Amazon RDS Resources](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html) in the *Amazon RDS User Guide.*.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Integration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 data_filter: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 integration_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 target_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A zero-ETL integration with Amazon Redshift.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] additional_encryption_context: An optional set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context) in the *Key Management Service Developer Guide*.
                You can only include this parameter if you specify the ``KMSKeyId`` parameter.
        :param pulumi.Input[str] data_filter: Data filters for the integration. These filters determine which tables from the source database are sent to the target Amazon Redshift data warehouse.
        :param pulumi.Input[str] description: A description of the integration.
        :param pulumi.Input[str] integration_name: The name of the integration.
        :param pulumi.Input[str] kms_key_id: The AWS Key Management System (AWS KMS) key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key.
        :param pulumi.Input[str] source_arn: The Amazon Resource Name (ARN) of the database to use as the source for replication.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: A list of tags. For more information, see [Tagging Amazon RDS Resources](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html) in the *Amazon RDS User Guide.*.
        :param pulumi.Input[str] target_arn: The ARN of the Redshift data warehouse to use as the target for replication.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IntegrationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A zero-ETL integration with Amazon Redshift.

        :param str resource_name: The name of the resource.
        :param IntegrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 additional_encryption_context: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 data_filter: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 integration_name: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 target_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationArgs.__new__(IntegrationArgs)

            __props__.__dict__["additional_encryption_context"] = additional_encryption_context
            __props__.__dict__["data_filter"] = data_filter
            __props__.__dict__["description"] = description
            __props__.__dict__["integration_name"] = integration_name
            __props__.__dict__["kms_key_id"] = kms_key_id
            if source_arn is None and not opts.urn:
                raise TypeError("Missing required property 'source_arn'")
            __props__.__dict__["source_arn"] = source_arn
            __props__.__dict__["tags"] = tags
            if target_arn is None and not opts.urn:
                raise TypeError("Missing required property 'target_arn'")
            __props__.__dict__["target_arn"] = target_arn
            __props__.__dict__["create_time"] = None
            __props__.__dict__["integration_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["additionalEncryptionContext.*", "kmsKeyId", "sourceArn", "targetArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Integration, __self__).__init__(
            'aws-native:rds:Integration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Integration':
        """
        Get an existing Integration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IntegrationArgs.__new__(IntegrationArgs)

        __props__.__dict__["additional_encryption_context"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["data_filter"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["integration_arn"] = None
        __props__.__dict__["integration_name"] = None
        __props__.__dict__["kms_key_id"] = None
        __props__.__dict__["source_arn"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["target_arn"] = None
        return Integration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="additionalEncryptionContext")
    def additional_encryption_context(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        An optional set of non-secret key–value pairs that contains additional contextual information about the data. For more information, see [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#encrypt_context) in the *Key Management Service Developer Guide*.
         You can only include this parameter if you specify the ``KMSKeyId`` parameter.
        """
        return pulumi.get(self, "additional_encryption_context")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the integration was created, in Universal Coordinated Time (UTC).
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="dataFilter")
    def data_filter(self) -> pulumi.Output[Optional[str]]:
        """
        Data filters for the integration. These filters determine which tables from the source database are sent to the target Amazon Redshift data warehouse.
        """
        return pulumi.get(self, "data_filter")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the integration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="integrationArn")
    def integration_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the integration.
        """
        return pulumi.get(self, "integration_arn")

    @property
    @pulumi.getter(name="integrationName")
    def integration_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the integration.
        """
        return pulumi.get(self, "integration_name")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        """
        The AWS Key Management System (AWS KMS) key identifier for the key to use to encrypt the integration. If you don't specify an encryption key, RDS uses a default AWS owned key.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the database to use as the source for replication.
        """
        return pulumi.get(self, "source_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        A list of tags. For more information, see [Tagging Amazon RDS Resources](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Tagging.html) in the *Amazon RDS User Guide.*.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetArn")
    def target_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Redshift data warehouse to use as the target for replication.
        """
        return pulumi.get(self, "target_arn")

