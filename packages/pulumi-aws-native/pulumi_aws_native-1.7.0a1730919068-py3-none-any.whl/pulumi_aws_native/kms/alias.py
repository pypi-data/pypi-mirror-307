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

__all__ = ['AliasArgs', 'Alias']

@pulumi.input_type
class AliasArgs:
    def __init__(__self__, *,
                 target_key_id: pulumi.Input[str],
                 alias_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Alias resource.
        :param pulumi.Input[str] target_key_id: Associates the alias with the specified [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk). The KMS key must be in the same AWS-account and Region.
                A valid key ID is required. If you supply a null or empty string value, this operation returns an error.
                For help finding the key ID and ARN, see [Finding the key ID and ARN](https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn) in the *Developer Guide*.
                Specify the key ID or the key ARN of the KMS key.
                For example:
                 +  Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` 
                 +  Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` 
                 
                To get the key ID and key ARN for a KMS key, use [ListKeys](https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html) or [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html).
        :param pulumi.Input[str] alias_name: Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias``. 
                 If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).
                 The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/``. The ``alias/aws/`` prefix is reserved for [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk).
        """
        pulumi.set(__self__, "target_key_id", target_key_id)
        if alias_name is not None:
            pulumi.set(__self__, "alias_name", alias_name)

    @property
    @pulumi.getter(name="targetKeyId")
    def target_key_id(self) -> pulumi.Input[str]:
        """
        Associates the alias with the specified [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk). The KMS key must be in the same AWS-account and Region.
         A valid key ID is required. If you supply a null or empty string value, this operation returns an error.
         For help finding the key ID and ARN, see [Finding the key ID and ARN](https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn) in the *Developer Guide*.
         Specify the key ID or the key ARN of the KMS key.
         For example:
          +  Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` 
          +  Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` 
          
         To get the key ID and key ARN for a KMS key, use [ListKeys](https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html) or [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html).
        """
        return pulumi.get(self, "target_key_id")

    @target_key_id.setter
    def target_key_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_key_id", value)

    @property
    @pulumi.getter(name="aliasName")
    def alias_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias``. 
          If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).
          The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/``. The ``alias/aws/`` prefix is reserved for [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk).
        """
        return pulumi.get(self, "alias_name")

    @alias_name.setter
    def alias_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alias_name", value)


class Alias(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alias_name: Optional[pulumi.Input[str]] = None,
                 target_key_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``AWS::KMS::Alias`` resource specifies a display name for a [KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys). You can use an alias to identify a KMS key in the KMS console, in the [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) operation, and in [cryptographic operations](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations), such as [Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html) and [GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html).
          Adding, deleting, or updating an alias can allow or deny permission to the KMS key. For details, see [ABAC for](https://docs.aws.amazon.com/kms/latest/developerguide/abac.html) in the *Developer Guide*.
          Using an alias to refer to a KMS key can help you simplify key management. For example, an alias in your code can be associated with different KMS keys in different AWS-Regions. For more information, see [Using aliases](https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html) in the *Developer Guide*.
         When specifying an alias, observe the following rules.
          +  Each alias is associated with one KMS key, but multiple aliases can be associated with the same KMS key.
          +  The alias and its associated KMS key must be in the same AWS-account and Region.
          +  The alias name must be unique in the AWS-account and Region. However, you can create aliases with the same name in different AWS-Regions. For example, you can have an ``alias/projectKey`` in multiple Regions, each of which is associated with a KMS key in its Region.
          +  Each alias name must begin with ``alias/`` followed by a name, such as ``alias/exampleKey``. The alias name can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). Alias names cannot begin with ``alias/aws/``. That alias name prefix is reserved for [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk).

          *Regions*
          KMS CloudFormation resources are available in all AWS-Regions in which KMS and CFN are supported.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alias_name: Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias``. 
                 If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).
                 The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/``. The ``alias/aws/`` prefix is reserved for [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk).
        :param pulumi.Input[str] target_key_id: Associates the alias with the specified [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk). The KMS key must be in the same AWS-account and Region.
                A valid key ID is required. If you supply a null or empty string value, this operation returns an error.
                For help finding the key ID and ARN, see [Finding the key ID and ARN](https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn) in the *Developer Guide*.
                Specify the key ID or the key ARN of the KMS key.
                For example:
                 +  Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` 
                 +  Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` 
                 
                To get the key ID and key ARN for a KMS key, use [ListKeys](https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html) or [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AliasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``AWS::KMS::Alias`` resource specifies a display name for a [KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys). You can use an alias to identify a KMS key in the KMS console, in the [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) operation, and in [cryptographic operations](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations), such as [Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html) and [GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html).
          Adding, deleting, or updating an alias can allow or deny permission to the KMS key. For details, see [ABAC for](https://docs.aws.amazon.com/kms/latest/developerguide/abac.html) in the *Developer Guide*.
          Using an alias to refer to a KMS key can help you simplify key management. For example, an alias in your code can be associated with different KMS keys in different AWS-Regions. For more information, see [Using aliases](https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html) in the *Developer Guide*.
         When specifying an alias, observe the following rules.
          +  Each alias is associated with one KMS key, but multiple aliases can be associated with the same KMS key.
          +  The alias and its associated KMS key must be in the same AWS-account and Region.
          +  The alias name must be unique in the AWS-account and Region. However, you can create aliases with the same name in different AWS-Regions. For example, you can have an ``alias/projectKey`` in multiple Regions, each of which is associated with a KMS key in its Region.
          +  Each alias name must begin with ``alias/`` followed by a name, such as ``alias/exampleKey``. The alias name can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). Alias names cannot begin with ``alias/aws/``. That alias name prefix is reserved for [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk).

          *Regions*
          KMS CloudFormation resources are available in all AWS-Regions in which KMS and CFN are supported.

        :param str resource_name: The name of the resource.
        :param AliasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AliasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alias_name: Optional[pulumi.Input[str]] = None,
                 target_key_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AliasArgs.__new__(AliasArgs)

            __props__.__dict__["alias_name"] = alias_name
            if target_key_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_key_id'")
            __props__.__dict__["target_key_id"] = target_key_id
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["aliasName"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Alias, __self__).__init__(
            'aws-native:kms:Alias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Alias':
        """
        Get an existing Alias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AliasArgs.__new__(AliasArgs)

        __props__.__dict__["alias_name"] = None
        __props__.__dict__["target_key_id"] = None
        return Alias(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aliasName")
    def alias_name(self) -> pulumi.Output[str]:
        """
        Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias``. 
          If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).
          The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/``. The ``alias/aws/`` prefix is reserved for [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk).
        """
        return pulumi.get(self, "alias_name")

    @property
    @pulumi.getter(name="targetKeyId")
    def target_key_id(self) -> pulumi.Output[str]:
        """
        Associates the alias with the specified [](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk). The KMS key must be in the same AWS-account and Region.
         A valid key ID is required. If you supply a null or empty string value, this operation returns an error.
         For help finding the key ID and ARN, see [Finding the key ID and ARN](https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn) in the *Developer Guide*.
         Specify the key ID or the key ARN of the KMS key.
         For example:
          +  Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` 
          +  Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` 
          
         To get the key ID and key ARN for a KMS key, use [ListKeys](https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html) or [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html).
        """
        return pulumi.get(self, "target_key_id")

