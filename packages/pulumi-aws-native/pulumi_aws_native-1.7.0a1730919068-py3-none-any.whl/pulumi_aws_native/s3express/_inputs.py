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

__all__ = [
    'DirectoryBucketBucketEncryptionArgs',
    'DirectoryBucketBucketEncryptionArgsDict',
    'DirectoryBucketServerSideEncryptionByDefaultArgs',
    'DirectoryBucketServerSideEncryptionByDefaultArgsDict',
    'DirectoryBucketServerSideEncryptionRuleArgs',
    'DirectoryBucketServerSideEncryptionRuleArgsDict',
]

MYPY = False

if not MYPY:
    class DirectoryBucketBucketEncryptionArgsDict(TypedDict):
        """
        Specifies default encryption for a bucket using server-side encryption with Amazon S3 managed keys (SSE-S3) or AWS KMS keys (SSE-KMS).
        """
        server_side_encryption_configuration: pulumi.Input[Sequence[pulumi.Input['DirectoryBucketServerSideEncryptionRuleArgsDict']]]
        """
        Specifies the default server-side-encryption configuration.
        """
elif False:
    DirectoryBucketBucketEncryptionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DirectoryBucketBucketEncryptionArgs:
    def __init__(__self__, *,
                 server_side_encryption_configuration: pulumi.Input[Sequence[pulumi.Input['DirectoryBucketServerSideEncryptionRuleArgs']]]):
        """
        Specifies default encryption for a bucket using server-side encryption with Amazon S3 managed keys (SSE-S3) or AWS KMS keys (SSE-KMS).
        :param pulumi.Input[Sequence[pulumi.Input['DirectoryBucketServerSideEncryptionRuleArgs']]] server_side_encryption_configuration: Specifies the default server-side-encryption configuration.
        """
        pulumi.set(__self__, "server_side_encryption_configuration", server_side_encryption_configuration)

    @property
    @pulumi.getter(name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(self) -> pulumi.Input[Sequence[pulumi.Input['DirectoryBucketServerSideEncryptionRuleArgs']]]:
        """
        Specifies the default server-side-encryption configuration.
        """
        return pulumi.get(self, "server_side_encryption_configuration")

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(self, value: pulumi.Input[Sequence[pulumi.Input['DirectoryBucketServerSideEncryptionRuleArgs']]]):
        pulumi.set(self, "server_side_encryption_configuration", value)


if not MYPY:
    class DirectoryBucketServerSideEncryptionByDefaultArgsDict(TypedDict):
        """
        Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.
        """
        sse_algorithm: pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultSseAlgorithm']
        """
        Server-side encryption algorithm to use for the default encryption.

        > For directory buckets, there are only two supported values for server-side encryption: `AES256` and `aws:kms` .
        """
        kms_master_key_id: NotRequired[pulumi.Input[str]]
        """
        AWS Key Management Service (KMS) customer managed key ID to use for the default encryption. This parameter is allowed only if SSEAlgorithm is set to aws:kms. You can specify this parameter with the key ID or the Amazon Resource Name (ARN) of the KMS key
        """
elif False:
    DirectoryBucketServerSideEncryptionByDefaultArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DirectoryBucketServerSideEncryptionByDefaultArgs:
    def __init__(__self__, *,
                 sse_algorithm: pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultSseAlgorithm'],
                 kms_master_key_id: Optional[pulumi.Input[str]] = None):
        """
        Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.
        :param pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultSseAlgorithm'] sse_algorithm: Server-side encryption algorithm to use for the default encryption.
               
               > For directory buckets, there are only two supported values for server-side encryption: `AES256` and `aws:kms` .
        :param pulumi.Input[str] kms_master_key_id: AWS Key Management Service (KMS) customer managed key ID to use for the default encryption. This parameter is allowed only if SSEAlgorithm is set to aws:kms. You can specify this parameter with the key ID or the Amazon Resource Name (ARN) of the KMS key
        """
        pulumi.set(__self__, "sse_algorithm", sse_algorithm)
        if kms_master_key_id is not None:
            pulumi.set(__self__, "kms_master_key_id", kms_master_key_id)

    @property
    @pulumi.getter(name="sseAlgorithm")
    def sse_algorithm(self) -> pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultSseAlgorithm']:
        """
        Server-side encryption algorithm to use for the default encryption.

        > For directory buckets, there are only two supported values for server-side encryption: `AES256` and `aws:kms` .
        """
        return pulumi.get(self, "sse_algorithm")

    @sse_algorithm.setter
    def sse_algorithm(self, value: pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultSseAlgorithm']):
        pulumi.set(self, "sse_algorithm", value)

    @property
    @pulumi.getter(name="kmsMasterKeyId")
    def kms_master_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS Key Management Service (KMS) customer managed key ID to use for the default encryption. This parameter is allowed only if SSEAlgorithm is set to aws:kms. You can specify this parameter with the key ID or the Amazon Resource Name (ARN) of the KMS key
        """
        return pulumi.get(self, "kms_master_key_id")

    @kms_master_key_id.setter
    def kms_master_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_master_key_id", value)


if not MYPY:
    class DirectoryBucketServerSideEncryptionRuleArgsDict(TypedDict):
        """
        Specifies the default server-side encryption configuration.
        """
        bucket_key_enabled: NotRequired[pulumi.Input[bool]]
        """
        Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Existing objects are not affected. Amazon S3 Express One Zone uses an S3 Bucket Key with SSE-KMS and S3 Bucket Key cannot be disabled. It's only allowed to set the BucketKeyEnabled element to true.
        """
        server_side_encryption_by_default: NotRequired[pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultArgsDict']]
        """
        Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.
        """
elif False:
    DirectoryBucketServerSideEncryptionRuleArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class DirectoryBucketServerSideEncryptionRuleArgs:
    def __init__(__self__, *,
                 bucket_key_enabled: Optional[pulumi.Input[bool]] = None,
                 server_side_encryption_by_default: Optional[pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultArgs']] = None):
        """
        Specifies the default server-side encryption configuration.
        :param pulumi.Input[bool] bucket_key_enabled: Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Existing objects are not affected. Amazon S3 Express One Zone uses an S3 Bucket Key with SSE-KMS and S3 Bucket Key cannot be disabled. It's only allowed to set the BucketKeyEnabled element to true.
        :param pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultArgs'] server_side_encryption_by_default: Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.
        """
        if bucket_key_enabled is not None:
            pulumi.set(__self__, "bucket_key_enabled", bucket_key_enabled)
        if server_side_encryption_by_default is not None:
            pulumi.set(__self__, "server_side_encryption_by_default", server_side_encryption_by_default)

    @property
    @pulumi.getter(name="bucketKeyEnabled")
    def bucket_key_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Existing objects are not affected. Amazon S3 Express One Zone uses an S3 Bucket Key with SSE-KMS and S3 Bucket Key cannot be disabled. It's only allowed to set the BucketKeyEnabled element to true.
        """
        return pulumi.get(self, "bucket_key_enabled")

    @bucket_key_enabled.setter
    def bucket_key_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bucket_key_enabled", value)

    @property
    @pulumi.getter(name="serverSideEncryptionByDefault")
    def server_side_encryption_by_default(self) -> Optional[pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultArgs']]:
        """
        Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.
        """
        return pulumi.get(self, "server_side_encryption_by_default")

    @server_side_encryption_by_default.setter
    def server_side_encryption_by_default(self, value: Optional[pulumi.Input['DirectoryBucketServerSideEncryptionByDefaultArgs']]):
        pulumi.set(self, "server_side_encryption_by_default", value)


