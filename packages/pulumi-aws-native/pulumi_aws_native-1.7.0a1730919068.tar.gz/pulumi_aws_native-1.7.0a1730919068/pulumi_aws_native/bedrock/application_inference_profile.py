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
from ._enums import *
from ._inputs import *

__all__ = ['ApplicationInferenceProfileArgs', 'ApplicationInferenceProfile']

@pulumi.input_type
class ApplicationInferenceProfileArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 inference_profile_name: Optional[pulumi.Input[str]] = None,
                 model_source: Optional[pulumi.Input['ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a ApplicationInferenceProfile resource.
        :param pulumi.Input[str] description: Description of the inference profile
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: List of Tags
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if inference_profile_name is not None:
            pulumi.set(__self__, "inference_profile_name", inference_profile_name)
        if model_source is not None:
            pulumi.set(__self__, "model_source", model_source)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the inference profile
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="inferenceProfileName")
    def inference_profile_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "inference_profile_name")

    @inference_profile_name.setter
    def inference_profile_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "inference_profile_name", value)

    @property
    @pulumi.getter(name="modelSource")
    def model_source(self) -> Optional[pulumi.Input['ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgs']]:
        return pulumi.get(self, "model_source")

    @model_source.setter
    def model_source(self, value: Optional[pulumi.Input['ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgs']]):
        pulumi.set(self, "model_source", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        List of Tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class ApplicationInferenceProfile(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 inference_profile_name: Optional[pulumi.Input[str]] = None,
                 model_source: Optional[pulumi.Input[Union['ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgs', 'ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Definition of AWS::Bedrock::ApplicationInferenceProfile Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the inference profile
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: List of Tags
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ApplicationInferenceProfileArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Bedrock::ApplicationInferenceProfile Resource Type

        :param str resource_name: The name of the resource.
        :param ApplicationInferenceProfileArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationInferenceProfileArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 inference_profile_name: Optional[pulumi.Input[str]] = None,
                 model_source: Optional[pulumi.Input[Union['ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgs', 'ApplicationInferenceProfileInferenceProfileModelSourcePropertiesArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationInferenceProfileArgs.__new__(ApplicationInferenceProfileArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["inference_profile_name"] = inference_profile_name
            __props__.__dict__["model_source"] = model_source
            __props__.__dict__["tags"] = tags
            __props__.__dict__["created_at"] = None
            __props__.__dict__["inference_profile_arn"] = None
            __props__.__dict__["inference_profile_id"] = None
            __props__.__dict__["inference_profile_identifier"] = None
            __props__.__dict__["models"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["updated_at"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["description", "inferenceProfileName", "modelSource"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ApplicationInferenceProfile, __self__).__init__(
            'aws-native:bedrock:ApplicationInferenceProfile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationInferenceProfile':
        """
        Get an existing ApplicationInferenceProfile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationInferenceProfileArgs.__new__(ApplicationInferenceProfileArgs)

        __props__.__dict__["created_at"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["inference_profile_arn"] = None
        __props__.__dict__["inference_profile_id"] = None
        __props__.__dict__["inference_profile_identifier"] = None
        __props__.__dict__["inference_profile_name"] = None
        __props__.__dict__["model_source"] = None
        __props__.__dict__["models"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["updated_at"] = None
        return ApplicationInferenceProfile(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Time Stamp
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the inference profile
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="inferenceProfileArn")
    def inference_profile_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "inference_profile_arn")

    @property
    @pulumi.getter(name="inferenceProfileId")
    def inference_profile_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "inference_profile_id")

    @property
    @pulumi.getter(name="inferenceProfileIdentifier")
    def inference_profile_identifier(self) -> pulumi.Output[str]:
        """
        Inference profile identifier. Supports both system-defined inference profile ids, and inference profile ARNs.
        """
        return pulumi.get(self, "inference_profile_identifier")

    @property
    @pulumi.getter(name="inferenceProfileName")
    def inference_profile_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "inference_profile_name")

    @property
    @pulumi.getter(name="modelSource")
    def model_source(self) -> pulumi.Output[Optional['outputs.ApplicationInferenceProfileInferenceProfileModelSourceProperties']]:
        return pulumi.get(self, "model_source")

    @property
    @pulumi.getter
    def models(self) -> pulumi.Output[Sequence['outputs.ApplicationInferenceProfileInferenceProfileModel']]:
        """
        List of model configuration
        """
        return pulumi.get(self, "models")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['ApplicationInferenceProfileInferenceProfileStatus']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        List of Tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output['ApplicationInferenceProfileInferenceProfileType']:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        Time Stamp
        """
        return pulumi.get(self, "updated_at")

