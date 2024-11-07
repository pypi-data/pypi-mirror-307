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

__all__ = ['EnclaveCertificateIamRoleAssociationArgs', 'EnclaveCertificateIamRoleAssociation']

@pulumi.input_type
class EnclaveCertificateIamRoleAssociationArgs:
    def __init__(__self__, *,
                 certificate_arn: pulumi.Input[str],
                 role_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a EnclaveCertificateIamRoleAssociation resource.
        :param pulumi.Input[str] certificate_arn: The Amazon Resource Name (ARN) of the ACM certificate with which to associate the IAM role.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the ACM certificate. You can associate up to 16 IAM roles with an ACM certificate.
        """
        pulumi.set(__self__, "certificate_arn", certificate_arn)
        pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the ACM certificate with which to associate the IAM role.
        """
        return pulumi.get(self, "certificate_arn")

    @certificate_arn.setter
    def certificate_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_arn", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to associate with the ACM certificate. You can associate up to 16 IAM roles with an ACM certificate.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)


class EnclaveCertificateIamRoleAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_arn: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates an AWS Identity and Access Management (IAM) role with an AWS Certificate Manager (ACM) certificate. This association is based on Amazon Resource Names and it enables the certificate to be used by the ACM for Nitro Enclaves application inside an enclave.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_enclave_certificate_iam_role_association = aws_native.ec2.EnclaveCertificateIamRoleAssociation("myEnclaveCertificateIamRoleAssociation",
            certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/123abcde-cdef-abcd-1234-123abEXAMPLE",
            role_arn="arn:aws:iam::123456789012:role/my-acm-role")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_cert_association = aws_native.ec2.EnclaveCertificateIamRoleAssociation("myCertAssociation",
            certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/123abcde-cdef-abcd-1234-123abEXAMPLE",
            role_arn="arn:aws:iam::123456789012:role/my-acm-role")

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_arn: The Amazon Resource Name (ARN) of the ACM certificate with which to associate the IAM role.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the ACM certificate. You can associate up to 16 IAM roles with an ACM certificate.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnclaveCertificateIamRoleAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates an AWS Identity and Access Management (IAM) role with an AWS Certificate Manager (ACM) certificate. This association is based on Amazon Resource Names and it enables the certificate to be used by the ACM for Nitro Enclaves application inside an enclave.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_enclave_certificate_iam_role_association = aws_native.ec2.EnclaveCertificateIamRoleAssociation("myEnclaveCertificateIamRoleAssociation",
            certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/123abcde-cdef-abcd-1234-123abEXAMPLE",
            role_arn="arn:aws:iam::123456789012:role/my-acm-role")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        my_cert_association = aws_native.ec2.EnclaveCertificateIamRoleAssociation("myCertAssociation",
            certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/123abcde-cdef-abcd-1234-123abEXAMPLE",
            role_arn="arn:aws:iam::123456789012:role/my-acm-role")

        ```

        :param str resource_name: The name of the resource.
        :param EnclaveCertificateIamRoleAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnclaveCertificateIamRoleAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_arn: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnclaveCertificateIamRoleAssociationArgs.__new__(EnclaveCertificateIamRoleAssociationArgs)

            if certificate_arn is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_arn'")
            __props__.__dict__["certificate_arn"] = certificate_arn
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["certificate_s3_bucket_name"] = None
            __props__.__dict__["certificate_s3_object_key"] = None
            __props__.__dict__["encryption_kms_key_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["certificateArn", "roleArn"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(EnclaveCertificateIamRoleAssociation, __self__).__init__(
            'aws-native:ec2:EnclaveCertificateIamRoleAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EnclaveCertificateIamRoleAssociation':
        """
        Get an existing EnclaveCertificateIamRoleAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EnclaveCertificateIamRoleAssociationArgs.__new__(EnclaveCertificateIamRoleAssociationArgs)

        __props__.__dict__["certificate_arn"] = None
        __props__.__dict__["certificate_s3_bucket_name"] = None
        __props__.__dict__["certificate_s3_object_key"] = None
        __props__.__dict__["encryption_kms_key_id"] = None
        __props__.__dict__["role_arn"] = None
        return EnclaveCertificateIamRoleAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the ACM certificate with which to associate the IAM role.
        """
        return pulumi.get(self, "certificate_arn")

    @property
    @pulumi.getter(name="certificateS3BucketName")
    def certificate_s3_bucket_name(self) -> pulumi.Output[str]:
        """
        The name of the Amazon S3 bucket to which the certificate was uploaded.
        """
        return pulumi.get(self, "certificate_s3_bucket_name")

    @property
    @pulumi.getter(name="certificateS3ObjectKey")
    def certificate_s3_object_key(self) -> pulumi.Output[str]:
        """
        The Amazon S3 object key where the certificate, certificate chain, and encrypted private key bundle are stored.
        """
        return pulumi.get(self, "certificate_s3_object_key")

    @property
    @pulumi.getter(name="encryptionKmsKeyId")
    def encryption_kms_key_id(self) -> pulumi.Output[str]:
        """
        The ID of the AWS KMS CMK used to encrypt the private key of the certificate.
        """
        return pulumi.get(self, "encryption_kms_key_id")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to associate with the ACM certificate. You can associate up to 16 IAM roles with an ACM certificate.
        """
        return pulumi.get(self, "role_arn")

