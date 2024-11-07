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

__all__ = ['QueueInlinePolicyArgs', 'QueueInlinePolicy']

@pulumi.input_type
class QueueInlinePolicyArgs:
    def __init__(__self__, *,
                 policy_document: Any,
                 queue: pulumi.Input[str]):
        """
        The set of arguments for constructing a QueueInlinePolicy resource.
        :param Any policy_document: A policy document that contains permissions to add to the specified SQS queue
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SQS::QueueInlinePolicy` for more information about the expected schema for this property.
        :param pulumi.Input[str] queue: The URL of the SQS queue.
        """
        pulumi.set(__self__, "policy_document", policy_document)
        pulumi.set(__self__, "queue", queue)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Any:
        """
        A policy document that contains permissions to add to the specified SQS queue

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SQS::QueueInlinePolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Any):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter
    def queue(self) -> pulumi.Input[str]:
        """
        The URL of the SQS queue.
        """
        return pulumi.get(self, "queue")

    @queue.setter
    def queue(self, value: pulumi.Input[str]):
        pulumi.set(self, "queue", value)


class QueueInlinePolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_document: Optional[Any] = None,
                 queue: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Schema for SQS QueueInlinePolicy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param Any policy_document: A policy document that contains permissions to add to the specified SQS queue
               
               Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SQS::QueueInlinePolicy` for more information about the expected schema for this property.
        :param pulumi.Input[str] queue: The URL of the SQS queue.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueueInlinePolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schema for SQS QueueInlinePolicy

        :param str resource_name: The name of the resource.
        :param QueueInlinePolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueueInlinePolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_document: Optional[Any] = None,
                 queue: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueueInlinePolicyArgs.__new__(QueueInlinePolicyArgs)

            if policy_document is None and not opts.urn:
                raise TypeError("Missing required property 'policy_document'")
            __props__.__dict__["policy_document"] = policy_document
            if queue is None and not opts.urn:
                raise TypeError("Missing required property 'queue'")
            __props__.__dict__["queue"] = queue
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["queue"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(QueueInlinePolicy, __self__).__init__(
            'aws-native:sqs:QueueInlinePolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'QueueInlinePolicy':
        """
        Get an existing QueueInlinePolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = QueueInlinePolicyArgs.__new__(QueueInlinePolicyArgs)

        __props__.__dict__["policy_document"] = None
        __props__.__dict__["queue"] = None
        return QueueInlinePolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> pulumi.Output[Any]:
        """
        A policy document that contains permissions to add to the specified SQS queue

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SQS::QueueInlinePolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_document")

    @property
    @pulumi.getter
    def queue(self) -> pulumi.Output[str]:
        """
        The URL of the SQS queue.
        """
        return pulumi.get(self, "queue")

