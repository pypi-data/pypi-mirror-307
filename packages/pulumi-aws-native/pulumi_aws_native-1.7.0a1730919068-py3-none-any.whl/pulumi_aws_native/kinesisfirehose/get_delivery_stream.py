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
    'GetDeliveryStreamResult',
    'AwaitableGetDeliveryStreamResult',
    'get_delivery_stream',
    'get_delivery_stream_output',
]

@pulumi.output_type
class GetDeliveryStreamResult:
    def __init__(__self__, amazon_open_search_serverless_destination_configuration=None, amazonopensearchservice_destination_configuration=None, arn=None, delivery_stream_encryption_configuration_input=None, elasticsearch_destination_configuration=None, extended_s3_destination_configuration=None, http_endpoint_destination_configuration=None, redshift_destination_configuration=None, s3_destination_configuration=None, snowflake_destination_configuration=None, splunk_destination_configuration=None, tags=None):
        if amazon_open_search_serverless_destination_configuration and not isinstance(amazon_open_search_serverless_destination_configuration, dict):
            raise TypeError("Expected argument 'amazon_open_search_serverless_destination_configuration' to be a dict")
        pulumi.set(__self__, "amazon_open_search_serverless_destination_configuration", amazon_open_search_serverless_destination_configuration)
        if amazonopensearchservice_destination_configuration and not isinstance(amazonopensearchservice_destination_configuration, dict):
            raise TypeError("Expected argument 'amazonopensearchservice_destination_configuration' to be a dict")
        pulumi.set(__self__, "amazonopensearchservice_destination_configuration", amazonopensearchservice_destination_configuration)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if delivery_stream_encryption_configuration_input and not isinstance(delivery_stream_encryption_configuration_input, dict):
            raise TypeError("Expected argument 'delivery_stream_encryption_configuration_input' to be a dict")
        pulumi.set(__self__, "delivery_stream_encryption_configuration_input", delivery_stream_encryption_configuration_input)
        if elasticsearch_destination_configuration and not isinstance(elasticsearch_destination_configuration, dict):
            raise TypeError("Expected argument 'elasticsearch_destination_configuration' to be a dict")
        pulumi.set(__self__, "elasticsearch_destination_configuration", elasticsearch_destination_configuration)
        if extended_s3_destination_configuration and not isinstance(extended_s3_destination_configuration, dict):
            raise TypeError("Expected argument 'extended_s3_destination_configuration' to be a dict")
        pulumi.set(__self__, "extended_s3_destination_configuration", extended_s3_destination_configuration)
        if http_endpoint_destination_configuration and not isinstance(http_endpoint_destination_configuration, dict):
            raise TypeError("Expected argument 'http_endpoint_destination_configuration' to be a dict")
        pulumi.set(__self__, "http_endpoint_destination_configuration", http_endpoint_destination_configuration)
        if redshift_destination_configuration and not isinstance(redshift_destination_configuration, dict):
            raise TypeError("Expected argument 'redshift_destination_configuration' to be a dict")
        pulumi.set(__self__, "redshift_destination_configuration", redshift_destination_configuration)
        if s3_destination_configuration and not isinstance(s3_destination_configuration, dict):
            raise TypeError("Expected argument 's3_destination_configuration' to be a dict")
        pulumi.set(__self__, "s3_destination_configuration", s3_destination_configuration)
        if snowflake_destination_configuration and not isinstance(snowflake_destination_configuration, dict):
            raise TypeError("Expected argument 'snowflake_destination_configuration' to be a dict")
        pulumi.set(__self__, "snowflake_destination_configuration", snowflake_destination_configuration)
        if splunk_destination_configuration and not isinstance(splunk_destination_configuration, dict):
            raise TypeError("Expected argument 'splunk_destination_configuration' to be a dict")
        pulumi.set(__self__, "splunk_destination_configuration", splunk_destination_configuration)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="amazonOpenSearchServerlessDestinationConfiguration")
    def amazon_open_search_serverless_destination_configuration(self) -> Optional['outputs.DeliveryStreamAmazonOpenSearchServerlessDestinationConfiguration']:
        """
        Describes the configuration of a destination in the Serverless offering for Amazon OpenSearch Service.
        """
        return pulumi.get(self, "amazon_open_search_serverless_destination_configuration")

    @property
    @pulumi.getter(name="amazonopensearchserviceDestinationConfiguration")
    def amazonopensearchservice_destination_configuration(self) -> Optional['outputs.DeliveryStreamAmazonopensearchserviceDestinationConfiguration']:
        """
        The destination in Amazon OpenSearch Service. You can specify only one destination.
        """
        return pulumi.get(self, "amazonopensearchservice_destination_configuration")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the delivery stream, such as `arn:aws:firehose:us-east-2:123456789012:deliverystream/delivery-stream-name` .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deliveryStreamEncryptionConfigurationInput")
    def delivery_stream_encryption_configuration_input(self) -> Optional['outputs.DeliveryStreamEncryptionConfigurationInput']:
        """
        Specifies the type and Amazon Resource Name (ARN) of the CMK to use for Server-Side Encryption (SSE).
        """
        return pulumi.get(self, "delivery_stream_encryption_configuration_input")

    @property
    @pulumi.getter(name="elasticsearchDestinationConfiguration")
    def elasticsearch_destination_configuration(self) -> Optional['outputs.DeliveryStreamElasticsearchDestinationConfiguration']:
        """
        An Amazon ES destination for the delivery stream.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon ES destination to an Amazon S3 or Amazon Redshift destination, update requires [some interruptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt) .
        """
        return pulumi.get(self, "elasticsearch_destination_configuration")

    @property
    @pulumi.getter(name="extendedS3DestinationConfiguration")
    def extended_s3_destination_configuration(self) -> Optional['outputs.DeliveryStreamExtendedS3DestinationConfiguration']:
        """
        An Amazon S3 destination for the delivery stream.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon Extended S3 destination to an Amazon ES destination, update requires [some interruptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt) .
        """
        return pulumi.get(self, "extended_s3_destination_configuration")

    @property
    @pulumi.getter(name="httpEndpointDestinationConfiguration")
    def http_endpoint_destination_configuration(self) -> Optional['outputs.DeliveryStreamHttpEndpointDestinationConfiguration']:
        """
        Enables configuring Kinesis Firehose to deliver data to any HTTP endpoint destination. You can specify only one destination.
        """
        return pulumi.get(self, "http_endpoint_destination_configuration")

    @property
    @pulumi.getter(name="redshiftDestinationConfiguration")
    def redshift_destination_configuration(self) -> Optional['outputs.DeliveryStreamRedshiftDestinationConfiguration']:
        """
        An Amazon Redshift destination for the delivery stream.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon Redshift destination to an Amazon ES destination, update requires [some interruptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt) .
        """
        return pulumi.get(self, "redshift_destination_configuration")

    @property
    @pulumi.getter(name="s3DestinationConfiguration")
    def s3_destination_configuration(self) -> Optional['outputs.DeliveryStreamS3DestinationConfiguration']:
        """
        The `S3DestinationConfiguration` property type specifies an Amazon Simple Storage Service (Amazon S3) destination to which Amazon Kinesis Data Firehose (Kinesis Data Firehose) delivers data.

        Conditional. You must specify only one destination configuration.

        If you change the delivery stream destination from an Amazon S3 destination to an Amazon ES destination, update requires [some interruptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-some-interrupt) .
        """
        return pulumi.get(self, "s3_destination_configuration")

    @property
    @pulumi.getter(name="snowflakeDestinationConfiguration")
    def snowflake_destination_configuration(self) -> Optional['outputs.DeliveryStreamSnowflakeDestinationConfiguration']:
        """
        Configure Snowflake destination
        """
        return pulumi.get(self, "snowflake_destination_configuration")

    @property
    @pulumi.getter(name="splunkDestinationConfiguration")
    def splunk_destination_configuration(self) -> Optional['outputs.DeliveryStreamSplunkDestinationConfiguration']:
        """
        The configuration of a destination in Splunk for the delivery stream.
        """
        return pulumi.get(self, "splunk_destination_configuration")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A set of tags to assign to the Firehose stream. A tag is a key-value pair that you can define and assign to AWS resources. Tags are metadata. For example, you can add friendly names and descriptions or other types of information that can help you distinguish the Firehose stream. For more information about tags, see [Using Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) in the AWS Billing and Cost Management User Guide.

        You can specify up to 50 tags when creating a Firehose stream.

        If you specify tags in the `CreateDeliveryStream` action, Amazon Data Firehose performs an additional authorization on the `firehose:TagDeliveryStream` action to verify if users have permissions to create tags. If you do not provide this permission, requests to create new Firehose Firehose streams with IAM resource tags will fail with an `AccessDeniedException` such as following.

        *AccessDeniedException*

        User: arn:aws:sts::x:assumed-role/x/x is not authorized to perform: firehose:TagDeliveryStream on resource: arn:aws:firehose:us-east-1:x:deliverystream/x with an explicit deny in an identity-based policy.

        For an example IAM policy, see [Tag example.](https://docs.aws.amazon.com/firehose/latest/APIReference/API_CreateDeliveryStream.html#API_CreateDeliveryStream_Examples)
        """
        return pulumi.get(self, "tags")


class AwaitableGetDeliveryStreamResult(GetDeliveryStreamResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeliveryStreamResult(
            amazon_open_search_serverless_destination_configuration=self.amazon_open_search_serverless_destination_configuration,
            amazonopensearchservice_destination_configuration=self.amazonopensearchservice_destination_configuration,
            arn=self.arn,
            delivery_stream_encryption_configuration_input=self.delivery_stream_encryption_configuration_input,
            elasticsearch_destination_configuration=self.elasticsearch_destination_configuration,
            extended_s3_destination_configuration=self.extended_s3_destination_configuration,
            http_endpoint_destination_configuration=self.http_endpoint_destination_configuration,
            redshift_destination_configuration=self.redshift_destination_configuration,
            s3_destination_configuration=self.s3_destination_configuration,
            snowflake_destination_configuration=self.snowflake_destination_configuration,
            splunk_destination_configuration=self.splunk_destination_configuration,
            tags=self.tags)


def get_delivery_stream(delivery_stream_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeliveryStreamResult:
    """
    Resource Type definition for AWS::KinesisFirehose::DeliveryStream


    :param str delivery_stream_name: The name of the Firehose stream.
    """
    __args__ = dict()
    __args__['deliveryStreamName'] = delivery_stream_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kinesisfirehose:getDeliveryStream', __args__, opts=opts, typ=GetDeliveryStreamResult).value

    return AwaitableGetDeliveryStreamResult(
        amazon_open_search_serverless_destination_configuration=pulumi.get(__ret__, 'amazon_open_search_serverless_destination_configuration'),
        amazonopensearchservice_destination_configuration=pulumi.get(__ret__, 'amazonopensearchservice_destination_configuration'),
        arn=pulumi.get(__ret__, 'arn'),
        delivery_stream_encryption_configuration_input=pulumi.get(__ret__, 'delivery_stream_encryption_configuration_input'),
        elasticsearch_destination_configuration=pulumi.get(__ret__, 'elasticsearch_destination_configuration'),
        extended_s3_destination_configuration=pulumi.get(__ret__, 'extended_s3_destination_configuration'),
        http_endpoint_destination_configuration=pulumi.get(__ret__, 'http_endpoint_destination_configuration'),
        redshift_destination_configuration=pulumi.get(__ret__, 'redshift_destination_configuration'),
        s3_destination_configuration=pulumi.get(__ret__, 's3_destination_configuration'),
        snowflake_destination_configuration=pulumi.get(__ret__, 'snowflake_destination_configuration'),
        splunk_destination_configuration=pulumi.get(__ret__, 'splunk_destination_configuration'),
        tags=pulumi.get(__ret__, 'tags'))
def get_delivery_stream_output(delivery_stream_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDeliveryStreamResult]:
    """
    Resource Type definition for AWS::KinesisFirehose::DeliveryStream


    :param str delivery_stream_name: The name of the Firehose stream.
    """
    __args__ = dict()
    __args__['deliveryStreamName'] = delivery_stream_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:kinesisfirehose:getDeliveryStream', __args__, opts=opts, typ=GetDeliveryStreamResult)
    return __ret__.apply(lambda __response__: GetDeliveryStreamResult(
        amazon_open_search_serverless_destination_configuration=pulumi.get(__response__, 'amazon_open_search_serverless_destination_configuration'),
        amazonopensearchservice_destination_configuration=pulumi.get(__response__, 'amazonopensearchservice_destination_configuration'),
        arn=pulumi.get(__response__, 'arn'),
        delivery_stream_encryption_configuration_input=pulumi.get(__response__, 'delivery_stream_encryption_configuration_input'),
        elasticsearch_destination_configuration=pulumi.get(__response__, 'elasticsearch_destination_configuration'),
        extended_s3_destination_configuration=pulumi.get(__response__, 'extended_s3_destination_configuration'),
        http_endpoint_destination_configuration=pulumi.get(__response__, 'http_endpoint_destination_configuration'),
        redshift_destination_configuration=pulumi.get(__response__, 'redshift_destination_configuration'),
        s3_destination_configuration=pulumi.get(__response__, 's3_destination_configuration'),
        snowflake_destination_configuration=pulumi.get(__response__, 'snowflake_destination_configuration'),
        splunk_destination_configuration=pulumi.get(__response__, 'splunk_destination_configuration'),
        tags=pulumi.get(__response__, 'tags')))
