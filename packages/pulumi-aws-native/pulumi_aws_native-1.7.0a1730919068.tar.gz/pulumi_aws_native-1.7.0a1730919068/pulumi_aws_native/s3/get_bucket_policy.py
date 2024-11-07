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

__all__ = [
    'GetBucketPolicyResult',
    'AwaitableGetBucketPolicyResult',
    'get_bucket_policy',
    'get_bucket_policy_output',
]

@pulumi.output_type
class GetBucketPolicyResult:
    def __init__(__self__, policy_document=None):
        if policy_document and not isinstance(policy_document, dict):
            raise TypeError("Expected argument 'policy_document' to be a dict")
        pulumi.set(__self__, "policy_document", policy_document)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[Any]:
        """
        A policy document containing permissions to add to the specified bucket. In IAM, you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy [PolicyDocument](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument) resource description in this guide and [Access Policy Language Overview](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-policy-language-overview.html) in the *Amazon S3 User Guide*.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::S3::BucketPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_document")


class AwaitableGetBucketPolicyResult(GetBucketPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBucketPolicyResult(
            policy_document=self.policy_document)


def get_bucket_policy(bucket: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBucketPolicyResult:
    """
    Applies an Amazon S3 bucket policy to an Amazon S3 bucket. If you are using an identity other than the root user of the AWS-account that owns the bucket, the calling identity must have the ``PutBucketPolicy`` permissions on the specified bucket and belong to the bucket owner's account in order to use this operation.
     If you don't have ``PutBucketPolicy`` permissions, Amazon S3 returns a ``403 Access Denied`` error. If you have the correct permissions, but you're not using an identity that belongs to the bucket owner's account, Amazon S3 returns a ``405 Method Not Allowed`` error.
       As a security precaution, the root user of the AWS-account that owns a bucket can always use this operation, even if the policy explicitly denies the root user the ability to perform this action.
      For more information, see [Bucket policy examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html).
     The following operations are related to ``PutBucketPolicy``:
      +   [CreateBucket](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucket.html)
      +   [DeleteBucket](https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucket.html)


    :param str bucket: The name of the Amazon S3 bucket to which the policy applies.
    """
    __args__ = dict()
    __args__['bucket'] = bucket
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:s3:getBucketPolicy', __args__, opts=opts, typ=GetBucketPolicyResult).value

    return AwaitableGetBucketPolicyResult(
        policy_document=pulumi.get(__ret__, 'policy_document'))
def get_bucket_policy_output(bucket: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBucketPolicyResult]:
    """
    Applies an Amazon S3 bucket policy to an Amazon S3 bucket. If you are using an identity other than the root user of the AWS-account that owns the bucket, the calling identity must have the ``PutBucketPolicy`` permissions on the specified bucket and belong to the bucket owner's account in order to use this operation.
     If you don't have ``PutBucketPolicy`` permissions, Amazon S3 returns a ``403 Access Denied`` error. If you have the correct permissions, but you're not using an identity that belongs to the bucket owner's account, Amazon S3 returns a ``405 Method Not Allowed`` error.
       As a security precaution, the root user of the AWS-account that owns a bucket can always use this operation, even if the policy explicitly denies the root user the ability to perform this action.
      For more information, see [Bucket policy examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html).
     The following operations are related to ``PutBucketPolicy``:
      +   [CreateBucket](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucket.html)
      +   [DeleteBucket](https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucket.html)


    :param str bucket: The name of the Amazon S3 bucket to which the policy applies.
    """
    __args__ = dict()
    __args__['bucket'] = bucket
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:s3:getBucketPolicy', __args__, opts=opts, typ=GetBucketPolicyResult)
    return __ret__.apply(lambda __response__: GetBucketPolicyResult(
        policy_document=pulumi.get(__response__, 'policy_document')))
