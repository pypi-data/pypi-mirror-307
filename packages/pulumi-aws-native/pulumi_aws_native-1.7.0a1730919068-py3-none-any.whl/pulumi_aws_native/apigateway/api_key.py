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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._inputs import *

__all__ = ['ApiKeyArgs', 'ApiKey']

@pulumi.input_type
class ApiKeyArgs:
    def __init__(__self__, *,
                 customer_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 generate_distinct_id: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 stage_keys: Optional[pulumi.Input[Sequence[pulumi.Input['ApiKeyStageKeyArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApiKey resource.
        :param pulumi.Input[str] customer_id: An AWS Marketplace customer identifier, when integrating with the AWS SaaS Marketplace.
        :param pulumi.Input[str] description: The description of the ApiKey.
        :param pulumi.Input[bool] enabled: Specifies whether the ApiKey can be used by callers.
        :param pulumi.Input[bool] generate_distinct_id: Specifies whether ( `true` ) or not ( `false` ) the key identifier is distinct from the created API key value. This parameter is deprecated and should not be used.
        :param pulumi.Input[str] name: A name for the API key. If you don't specify a name, CFN generates a unique physical ID and uses that ID for the API key name. For more information, see [Name Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html).
                If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param pulumi.Input[Sequence[pulumi.Input['ApiKeyStageKeyArgs']]] stage_keys: DEPRECATED FOR USAGE PLANS - Specifies stages associated with the API key.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with `aws:` . The tag value can be up to 256 characters.
        :param pulumi.Input[str] value: Specifies a value of the API key.
        """
        if customer_id is not None:
            pulumi.set(__self__, "customer_id", customer_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if generate_distinct_id is not None:
            pulumi.set(__self__, "generate_distinct_id", generate_distinct_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if stage_keys is not None:
            pulumi.set(__self__, "stage_keys", stage_keys)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="customerId")
    def customer_id(self) -> Optional[pulumi.Input[str]]:
        """
        An AWS Marketplace customer identifier, when integrating with the AWS SaaS Marketplace.
        """
        return pulumi.get(self, "customer_id")

    @customer_id.setter
    def customer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "customer_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the ApiKey.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the ApiKey can be used by callers.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="generateDistinctId")
    def generate_distinct_id(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether ( `true` ) or not ( `false` ) the key identifier is distinct from the created API key value. This parameter is deprecated and should not be used.
        """
        return pulumi.get(self, "generate_distinct_id")

    @generate_distinct_id.setter
    def generate_distinct_id(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "generate_distinct_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the API key. If you don't specify a name, CFN generates a unique physical ID and uses that ID for the API key name. For more information, see [Name Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html).
         If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="stageKeys")
    def stage_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApiKeyStageKeyArgs']]]]:
        """
        DEPRECATED FOR USAGE PLANS - Specifies stages associated with the API key.
        """
        return pulumi.get(self, "stage_keys")

    @stage_keys.setter
    def stage_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApiKeyStageKeyArgs']]]]):
        pulumi.set(self, "stage_keys", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with `aws:` . The tag value can be up to 256 characters.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a value of the API key.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


class ApiKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 customer_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 generate_distinct_id: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 stage_keys: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ApiKeyStageKeyArgs', 'ApiKeyStageKeyArgsDict']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``AWS::ApiGateway::ApiKey`` resource creates a unique key that you can distribute to clients who are executing API Gateway ``Method`` resources that require an API key. To specify which API key clients must use, map the API key with the ``RestApi`` and ``Stage`` resources that include the methods that require a key.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        api_key_name = config.require("apiKeyName")
        customer_id = config.require("customerId")
        generate_distinct_id = config.require("generateDistinctId")
        api_key = aws_native.apigateway.ApiKey("apiKey",
            customer_id=customer_id,
            generate_distinct_id=generate_distinct_id,
            name=api_key_name)

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        api_key_name = config.require("apiKeyName")
        customer_id = config.require("customerId")
        generate_distinct_id = config.require("generateDistinctId")
        api_key = aws_native.apigateway.ApiKey("apiKey",
            customer_id=customer_id,
            generate_distinct_id=generate_distinct_id,
            name=api_key_name)

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] customer_id: An AWS Marketplace customer identifier, when integrating with the AWS SaaS Marketplace.
        :param pulumi.Input[str] description: The description of the ApiKey.
        :param pulumi.Input[bool] enabled: Specifies whether the ApiKey can be used by callers.
        :param pulumi.Input[bool] generate_distinct_id: Specifies whether ( `true` ) or not ( `false` ) the key identifier is distinct from the created API key value. This parameter is deprecated and should not be used.
        :param pulumi.Input[str] name: A name for the API key. If you don't specify a name, CFN generates a unique physical ID and uses that ID for the API key name. For more information, see [Name Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html).
                If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param pulumi.Input[Sequence[pulumi.Input[Union['ApiKeyStageKeyArgs', 'ApiKeyStageKeyArgsDict']]]] stage_keys: DEPRECATED FOR USAGE PLANS - Specifies stages associated with the API key.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with `aws:` . The tag value can be up to 256 characters.
        :param pulumi.Input[str] value: Specifies a value of the API key.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ApiKeyArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``AWS::ApiGateway::ApiKey`` resource creates a unique key that you can distribute to clients who are executing API Gateway ``Method`` resources that require an API key. To specify which API key clients must use, map the API key with the ``RestApi`` and ``Stage`` resources that include the methods that require a key.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        api_key_name = config.require("apiKeyName")
        customer_id = config.require("customerId")
        generate_distinct_id = config.require("generateDistinctId")
        api_key = aws_native.apigateway.ApiKey("apiKey",
            customer_id=customer_id,
            generate_distinct_id=generate_distinct_id,
            name=api_key_name)

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        config = pulumi.Config()
        api_key_name = config.require("apiKeyName")
        customer_id = config.require("customerId")
        generate_distinct_id = config.require("generateDistinctId")
        api_key = aws_native.apigateway.ApiKey("apiKey",
            customer_id=customer_id,
            generate_distinct_id=generate_distinct_id,
            name=api_key_name)

        ```

        :param str resource_name: The name of the resource.
        :param ApiKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApiKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 customer_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 generate_distinct_id: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 stage_keys: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ApiKeyStageKeyArgs', 'ApiKeyStageKeyArgsDict']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiKeyArgs.__new__(ApiKeyArgs)

            __props__.__dict__["customer_id"] = customer_id
            __props__.__dict__["description"] = description
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["generate_distinct_id"] = generate_distinct_id
            __props__.__dict__["name"] = name
            __props__.__dict__["stage_keys"] = stage_keys
            __props__.__dict__["tags"] = tags
            __props__.__dict__["value"] = value
            __props__.__dict__["api_key_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["generateDistinctId", "name", "value"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ApiKey, __self__).__init__(
            'aws-native:apigateway:ApiKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApiKey':
        """
        Get an existing ApiKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApiKeyArgs.__new__(ApiKeyArgs)

        __props__.__dict__["api_key_id"] = None
        __props__.__dict__["customer_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["generate_distinct_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["stage_keys"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["value"] = None
        return ApiKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKeyId")
    def api_key_id(self) -> pulumi.Output[str]:
        """
        The ID for the API key. For example: `abc123` .
        """
        return pulumi.get(self, "api_key_id")

    @property
    @pulumi.getter(name="customerId")
    def customer_id(self) -> pulumi.Output[Optional[str]]:
        """
        An AWS Marketplace customer identifier, when integrating with the AWS SaaS Marketplace.
        """
        return pulumi.get(self, "customer_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the ApiKey.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the ApiKey can be used by callers.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="generateDistinctId")
    def generate_distinct_id(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether ( `true` ) or not ( `false` ) the key identifier is distinct from the created API key value. This parameter is deprecated and should not be used.
        """
        return pulumi.get(self, "generate_distinct_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        A name for the API key. If you don't specify a name, CFN generates a unique physical ID and uses that ID for the API key name. For more information, see [Name Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html).
         If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="stageKeys")
    def stage_keys(self) -> pulumi.Output[Optional[Sequence['outputs.ApiKeyStageKey']]]:
        """
        DEPRECATED FOR USAGE PLANS - Specifies stages associated with the API key.
        """
        return pulumi.get(self, "stage_keys")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with `aws:` . The tag value can be up to 256 characters.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a value of the API key.
        """
        return pulumi.get(self, "value")

