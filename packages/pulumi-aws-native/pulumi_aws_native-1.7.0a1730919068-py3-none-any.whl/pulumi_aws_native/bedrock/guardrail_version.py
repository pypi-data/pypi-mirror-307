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

__all__ = ['GuardrailVersionArgs', 'GuardrailVersion']

@pulumi.input_type
class GuardrailVersionArgs:
    def __init__(__self__, *,
                 guardrail_identifier: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a GuardrailVersion resource.
        :param pulumi.Input[str] guardrail_identifier: Identifier (GuardrailId or GuardrailArn) for the guardrail
        :param pulumi.Input[str] description: Description of the Guardrail version
        """
        pulumi.set(__self__, "guardrail_identifier", guardrail_identifier)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="guardrailIdentifier")
    def guardrail_identifier(self) -> pulumi.Input[str]:
        """
        Identifier (GuardrailId or GuardrailArn) for the guardrail
        """
        return pulumi.get(self, "guardrail_identifier")

    @guardrail_identifier.setter
    def guardrail_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "guardrail_identifier", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Guardrail version
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


class GuardrailVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 guardrail_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Definition of AWS::Bedrock::GuardrailVersion Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the Guardrail version
        :param pulumi.Input[str] guardrail_identifier: Identifier (GuardrailId or GuardrailArn) for the guardrail
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GuardrailVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Bedrock::GuardrailVersion Resource Type

        :param str resource_name: The name of the resource.
        :param GuardrailVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GuardrailVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 guardrail_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GuardrailVersionArgs.__new__(GuardrailVersionArgs)

            __props__.__dict__["description"] = description
            if guardrail_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'guardrail_identifier'")
            __props__.__dict__["guardrail_identifier"] = guardrail_identifier
            __props__.__dict__["guardrail_arn"] = None
            __props__.__dict__["guardrail_id"] = None
            __props__.__dict__["version"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["description", "guardrailIdentifier"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(GuardrailVersion, __self__).__init__(
            'aws-native:bedrock:GuardrailVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GuardrailVersion':
        """
        Get an existing GuardrailVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GuardrailVersionArgs.__new__(GuardrailVersionArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["guardrail_arn"] = None
        __props__.__dict__["guardrail_id"] = None
        __props__.__dict__["guardrail_identifier"] = None
        __props__.__dict__["version"] = None
        return GuardrailVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Guardrail version
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="guardrailArn")
    def guardrail_arn(self) -> pulumi.Output[str]:
        """
        Arn representation for the guardrail
        """
        return pulumi.get(self, "guardrail_arn")

    @property
    @pulumi.getter(name="guardrailId")
    def guardrail_id(self) -> pulumi.Output[str]:
        """
        Unique id for the guardrail
        """
        return pulumi.get(self, "guardrail_id")

    @property
    @pulumi.getter(name="guardrailIdentifier")
    def guardrail_identifier(self) -> pulumi.Output[str]:
        """
        Identifier (GuardrailId or GuardrailArn) for the guardrail
        """
        return pulumi.get(self, "guardrail_identifier")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        Guardrail version
        """
        return pulumi.get(self, "version")

