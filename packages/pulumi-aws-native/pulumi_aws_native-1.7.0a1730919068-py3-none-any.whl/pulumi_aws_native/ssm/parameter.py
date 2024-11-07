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

__all__ = ['ParameterArgs', 'Parameter']

@pulumi.input_type
class ParameterArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['ParameterType'],
                 value: pulumi.Input[str],
                 allowed_pattern: Optional[pulumi.Input[str]] = None,
                 data_type: Optional[pulumi.Input['ParameterDataType']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tier: Optional[pulumi.Input['ParameterTier']] = None):
        """
        The set of arguments for constructing a Parameter resource.
        :param pulumi.Input['ParameterType'] type: The type of parameter.
        :param pulumi.Input[str] value: The parameter value.
                 If type is ``StringList``, the system returns a comma-separated string with no spaces between commas in the ``Value`` field.
        :param pulumi.Input[str] allowed_pattern: A regular expression used to validate the parameter value. For example, for ``String`` types with values restricted to numbers, you can specify the following: ``AllowedPattern=^\\d+$``
        :param pulumi.Input['ParameterDataType'] data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The default is ``text``.
        :param pulumi.Input[str] description: Information about the parameter.
        :param pulumi.Input[str] name: The name of the parameter.
                 The maximum length constraint listed below includes capacity for additional system attributes that aren't part of the name. The maximum length for a parameter name, including the full length of the parameter Amazon Resource Name (ARN), is 1011 characters. For example, the length of the following parameter name is 65 characters, not 20 characters: ``arn:aws:ssm:us-east-2:111222333444:parameter/ExampleParameterName``
        :param pulumi.Input[str] policies: Information about the policies assigned to a parameter.
                 [Assigning parameter policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html) in the *User Guide*.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs). Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a SYS parameter to identify the type of resource to which it applies, the environment, or the type of configuration data referenced by the parameter.
        :param pulumi.Input['ParameterTier'] tier: The parameter tier.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)
        if allowed_pattern is not None:
            pulumi.set(__self__, "allowed_pattern", allowed_pattern)
        if data_type is not None:
            pulumi.set(__self__, "data_type", data_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policies is not None:
            pulumi.set(__self__, "policies", policies)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['ParameterType']:
        """
        The type of parameter.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['ParameterType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The parameter value.
          If type is ``StringList``, the system returns a comma-separated string with no spaces between commas in the ``Value`` field.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="allowedPattern")
    def allowed_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        A regular expression used to validate the parameter value. For example, for ``String`` types with values restricted to numbers, you can specify the following: ``AllowedPattern=^\\d+$``
        """
        return pulumi.get(self, "allowed_pattern")

    @allowed_pattern.setter
    def allowed_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allowed_pattern", value)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> Optional[pulumi.Input['ParameterDataType']]:
        """
        The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The default is ``text``.
        """
        return pulumi.get(self, "data_type")

    @data_type.setter
    def data_type(self, value: Optional[pulumi.Input['ParameterDataType']]):
        pulumi.set(self, "data_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Information about the parameter.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the parameter.
          The maximum length constraint listed below includes capacity for additional system attributes that aren't part of the name. The maximum length for a parameter name, including the full length of the parameter Amazon Resource Name (ARN), is 1011 characters. For example, the length of the following parameter name is 65 characters, not 20 characters: ``arn:aws:ssm:us-east-2:111222333444:parameter/ExampleParameterName``
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def policies(self) -> Optional[pulumi.Input[str]]:
        """
        Information about the policies assigned to a parameter.
          [Assigning parameter policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html) in the *User Guide*.
        """
        return pulumi.get(self, "policies")

    @policies.setter
    def policies(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policies", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs). Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a SYS parameter to identify the type of resource to which it applies, the environment, or the type of configuration data referenced by the parameter.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input['ParameterTier']]:
        """
        The parameter tier.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input['ParameterTier']]):
        pulumi.set(self, "tier", value)


class Parameter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_pattern: Optional[pulumi.Input[str]] = None,
                 data_type: Optional[pulumi.Input['ParameterDataType']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tier: Optional[pulumi.Input['ParameterTier']] = None,
                 type: Optional[pulumi.Input['ParameterType']] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``AWS::SSM::Parameter`` resource creates an SSM parameter in SYSlong Parameter Store.
          To create an SSM parameter, you must have the IAMlong (IAM) permissions ``ssm:PutParameter`` and ``ssm:AddTagsToResource``. On stack creation, CFNlong adds the following three tags to the parameter: ``aws:cloudformation:stack-name``, ``aws:cloudformation:logical-id``, and ``aws:cloudformation:stack-id``, in addition to any custom tags you specify.
         To add, update, or remove tags during stack update, you must have IAM permissions for both ``ssm:AddTagsToResource`` and ``ssm:RemoveTagsFromResource``. For more information, see [Managing Access Using Policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/security-iam.html#security_iam_access-manage) in the *User Guide*.
          For information about valid values for parameters, see [About requirements and constraints for parameter names](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html#sysman-parameter-name-constraints) in the *User Guide* and [PutParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html) in the *API Reference*.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="commands",
            type=aws_native.ssm.ParameterType.STRING_LIST,
            value="date,ls",
            description="SSM Parameter of type StringList.",
            allowed_pattern="^[a-zA-Z]{1,10}$")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="commands",
            type=aws_native.ssm.ParameterType.STRING_LIST,
            value="date,ls",
            description="SSM Parameter of type StringList.",
            allowed_pattern="^[a-zA-Z]{1,10}$")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            tier=aws_native.ssm.ParameterTier.ADVANCED,
            policies="[{\\"Type\\":\\"Expiration\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Timestamp\\":\\"2020-05-13T00:00:00.000Z\\"}},{\\"Type\\":\\"ExpirationNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Before\\":\\"5\\",\\"Unit\\":\\"Days\\"}},{\\"Type\\":\\"NoChangeNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"After\\":\\"60\\",\\"Unit\\":\\"Days\\"}}]",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            tier=aws_native.ssm.ParameterTier.ADVANCED,
            policies="[{\\"Type\\":\\"Expiration\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Timestamp\\":\\"2020-05-13T00:00:00.000Z\\"}},{\\"Type\\":\\"ExpirationNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Before\\":\\"5\\",\\"Unit\\":\\"Days\\"}},{\\"Type\\":\\"NoChangeNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"After\\":\\"60\\",\\"Unit\\":\\"Days\\"}}]",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allowed_pattern: A regular expression used to validate the parameter value. For example, for ``String`` types with values restricted to numbers, you can specify the following: ``AllowedPattern=^\\d+$``
        :param pulumi.Input['ParameterDataType'] data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The default is ``text``.
        :param pulumi.Input[str] description: Information about the parameter.
        :param pulumi.Input[str] name: The name of the parameter.
                 The maximum length constraint listed below includes capacity for additional system attributes that aren't part of the name. The maximum length for a parameter name, including the full length of the parameter Amazon Resource Name (ARN), is 1011 characters. For example, the length of the following parameter name is 65 characters, not 20 characters: ``arn:aws:ssm:us-east-2:111222333444:parameter/ExampleParameterName``
        :param pulumi.Input[str] policies: Information about the policies assigned to a parameter.
                 [Assigning parameter policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html) in the *User Guide*.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs). Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a SYS parameter to identify the type of resource to which it applies, the environment, or the type of configuration data referenced by the parameter.
        :param pulumi.Input['ParameterTier'] tier: The parameter tier.
        :param pulumi.Input['ParameterType'] type: The type of parameter.
        :param pulumi.Input[str] value: The parameter value.
                 If type is ``StringList``, the system returns a comma-separated string with no spaces between commas in the ``Value`` field.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ParameterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``AWS::SSM::Parameter`` resource creates an SSM parameter in SYSlong Parameter Store.
          To create an SSM parameter, you must have the IAMlong (IAM) permissions ``ssm:PutParameter`` and ``ssm:AddTagsToResource``. On stack creation, CFNlong adds the following three tags to the parameter: ``aws:cloudformation:stack-name``, ``aws:cloudformation:logical-id``, and ``aws:cloudformation:stack-id``, in addition to any custom tags you specify.
         To add, update, or remove tags during stack update, you must have IAM permissions for both ``ssm:AddTagsToResource`` and ``ssm:RemoveTagsFromResource``. For more information, see [Managing Access Using Policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/security-iam.html#security_iam_access-manage) in the *User Guide*.
          For information about valid values for parameters, see [About requirements and constraints for parameter names](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html#sysman-parameter-name-constraints) in the *User Guide* and [PutParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html) in the *API Reference*.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="commands",
            type=aws_native.ssm.ParameterType.STRING_LIST,
            value="date,ls",
            description="SSM Parameter of type StringList.",
            allowed_pattern="^[a-zA-Z]{1,10}$")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="commands",
            type=aws_native.ssm.ParameterType.STRING_LIST,
            value="date,ls",
            description="SSM Parameter of type StringList.",
            allowed_pattern="^[a-zA-Z]{1,10}$")

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            tier=aws_native.ssm.ParameterTier.ADVANCED,
            policies="[{\\"Type\\":\\"Expiration\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Timestamp\\":\\"2020-05-13T00:00:00.000Z\\"}},{\\"Type\\":\\"ExpirationNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Before\\":\\"5\\",\\"Unit\\":\\"Days\\"}},{\\"Type\\":\\"NoChangeNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"After\\":\\"60\\",\\"Unit\\":\\"Days\\"}}]",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        basic_parameter = aws_native.ssm.Parameter("basicParameter",
            name="command",
            type=aws_native.ssm.ParameterType.STRING,
            value="date",
            tier=aws_native.ssm.ParameterTier.ADVANCED,
            policies="[{\\"Type\\":\\"Expiration\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Timestamp\\":\\"2020-05-13T00:00:00.000Z\\"}},{\\"Type\\":\\"ExpirationNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"Before\\":\\"5\\",\\"Unit\\":\\"Days\\"}},{\\"Type\\":\\"NoChangeNotification\\",\\"Version\\":\\"1.0\\",\\"Attributes\\":{\\"After\\":\\"60\\",\\"Unit\\":\\"Days\\"}}]",
            description="SSM Parameter for running date command.",
            allowed_pattern="^[a-zA-Z]{1,10}$",
            tags={
                "environment": "DEV",
            })

        ```

        :param str resource_name: The name of the resource.
        :param ParameterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ParameterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_pattern: Optional[pulumi.Input[str]] = None,
                 data_type: Optional[pulumi.Input['ParameterDataType']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tier: Optional[pulumi.Input['ParameterTier']] = None,
                 type: Optional[pulumi.Input['ParameterType']] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ParameterArgs.__new__(ParameterArgs)

            __props__.__dict__["allowed_pattern"] = allowed_pattern
            __props__.__dict__["data_type"] = data_type
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["policies"] = policies
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tier"] = tier
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            if value is None and not opts.urn:
                raise TypeError("Missing required property 'value'")
            __props__.__dict__["value"] = value
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Parameter, __self__).__init__(
            'aws-native:ssm:Parameter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Parameter':
        """
        Get an existing Parameter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ParameterArgs.__new__(ParameterArgs)

        __props__.__dict__["allowed_pattern"] = None
        __props__.__dict__["data_type"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policies"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["tier"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["value"] = None
        return Parameter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedPattern")
    def allowed_pattern(self) -> pulumi.Output[Optional[str]]:
        """
        A regular expression used to validate the parameter value. For example, for ``String`` types with values restricted to numbers, you can specify the following: ``AllowedPattern=^\\d+$``
        """
        return pulumi.get(self, "allowed_pattern")

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> pulumi.Output[Optional['ParameterDataType']]:
        """
        The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The default is ``text``.
        """
        return pulumi.get(self, "data_type")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Information about the parameter.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the parameter.
          The maximum length constraint listed below includes capacity for additional system attributes that aren't part of the name. The maximum length for a parameter name, including the full length of the parameter Amazon Resource Name (ARN), is 1011 characters. For example, the length of the following parameter name is 65 characters, not 20 characters: ``arn:aws:ssm:us-east-2:111222333444:parameter/ExampleParameterName``
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policies(self) -> pulumi.Output[Optional[str]]:
        """
        Information about the policies assigned to a parameter.
          [Assigning parameter policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html) in the *User Guide*.
        """
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs). Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a SYS parameter to identify the type of resource to which it applies, the environment, or the type of configuration data referenced by the parameter.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Output[Optional['ParameterTier']]:
        """
        The parameter tier.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output['ParameterType']:
        """
        The type of parameter.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> pulumi.Output[str]:
        """
        The parameter value.
          If type is ``StringList``, the system returns a comma-separated string with no spaces between commas in the ``Value`` field.
        """
        return pulumi.get(self, "value")

