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
from ._enums import *
from ._inputs import *

__all__ = ['AnnotationStoreArgs', 'AnnotationStore']

@pulumi.input_type
class AnnotationStoreArgs:
    def __init__(__self__, *,
                 store_format: pulumi.Input['AnnotationStoreStoreFormat'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reference: Optional[pulumi.Input['AnnotationStoreReferenceItemArgs']] = None,
                 sse_config: Optional[pulumi.Input['AnnotationStoreSseConfigArgs']] = None,
                 store_options: Optional[pulumi.Input['AnnotationStoreStoreOptionsPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AnnotationStore resource.
        :param pulumi.Input['AnnotationStoreStoreFormat'] store_format: The annotation file format of the store.
        :param pulumi.Input[str] description: A description for the store.
        :param pulumi.Input[str] name: The name of the Annotation Store.
        :param pulumi.Input['AnnotationStoreReferenceItemArgs'] reference: The genome reference for the store's annotations.
        :param pulumi.Input['AnnotationStoreSseConfigArgs'] sse_config: The store's server-side encryption (SSE) settings.
        :param pulumi.Input['AnnotationStoreStoreOptionsPropertiesArgs'] store_options: File parsing options for the annotation store.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags for the store.
        """
        pulumi.set(__self__, "store_format", store_format)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reference is not None:
            pulumi.set(__self__, "reference", reference)
        if sse_config is not None:
            pulumi.set(__self__, "sse_config", sse_config)
        if store_options is not None:
            pulumi.set(__self__, "store_options", store_options)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="storeFormat")
    def store_format(self) -> pulumi.Input['AnnotationStoreStoreFormat']:
        """
        The annotation file format of the store.
        """
        return pulumi.get(self, "store_format")

    @store_format.setter
    def store_format(self, value: pulumi.Input['AnnotationStoreStoreFormat']):
        pulumi.set(self, "store_format", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the store.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Annotation Store.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def reference(self) -> Optional[pulumi.Input['AnnotationStoreReferenceItemArgs']]:
        """
        The genome reference for the store's annotations.
        """
        return pulumi.get(self, "reference")

    @reference.setter
    def reference(self, value: Optional[pulumi.Input['AnnotationStoreReferenceItemArgs']]):
        pulumi.set(self, "reference", value)

    @property
    @pulumi.getter(name="sseConfig")
    def sse_config(self) -> Optional[pulumi.Input['AnnotationStoreSseConfigArgs']]:
        """
        The store's server-side encryption (SSE) settings.
        """
        return pulumi.get(self, "sse_config")

    @sse_config.setter
    def sse_config(self, value: Optional[pulumi.Input['AnnotationStoreSseConfigArgs']]):
        pulumi.set(self, "sse_config", value)

    @property
    @pulumi.getter(name="storeOptions")
    def store_options(self) -> Optional[pulumi.Input['AnnotationStoreStoreOptionsPropertiesArgs']]:
        """
        File parsing options for the annotation store.
        """
        return pulumi.get(self, "store_options")

    @store_options.setter
    def store_options(self, value: Optional[pulumi.Input['AnnotationStoreStoreOptionsPropertiesArgs']]):
        pulumi.set(self, "store_options", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags for the store.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class AnnotationStore(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reference: Optional[pulumi.Input[Union['AnnotationStoreReferenceItemArgs', 'AnnotationStoreReferenceItemArgsDict']]] = None,
                 sse_config: Optional[pulumi.Input[Union['AnnotationStoreSseConfigArgs', 'AnnotationStoreSseConfigArgsDict']]] = None,
                 store_format: Optional[pulumi.Input['AnnotationStoreStoreFormat']] = None,
                 store_options: Optional[pulumi.Input[Union['AnnotationStoreStoreOptionsPropertiesArgs', 'AnnotationStoreStoreOptionsPropertiesArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Definition of AWS::Omics::AnnotationStore Resource Type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description for the store.
        :param pulumi.Input[str] name: The name of the Annotation Store.
        :param pulumi.Input[Union['AnnotationStoreReferenceItemArgs', 'AnnotationStoreReferenceItemArgsDict']] reference: The genome reference for the store's annotations.
        :param pulumi.Input[Union['AnnotationStoreSseConfigArgs', 'AnnotationStoreSseConfigArgsDict']] sse_config: The store's server-side encryption (SSE) settings.
        :param pulumi.Input['AnnotationStoreStoreFormat'] store_format: The annotation file format of the store.
        :param pulumi.Input[Union['AnnotationStoreStoreOptionsPropertiesArgs', 'AnnotationStoreStoreOptionsPropertiesArgsDict']] store_options: File parsing options for the annotation store.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags for the store.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnnotationStoreArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of AWS::Omics::AnnotationStore Resource Type

        :param str resource_name: The name of the resource.
        :param AnnotationStoreArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnnotationStoreArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reference: Optional[pulumi.Input[Union['AnnotationStoreReferenceItemArgs', 'AnnotationStoreReferenceItemArgsDict']]] = None,
                 sse_config: Optional[pulumi.Input[Union['AnnotationStoreSseConfigArgs', 'AnnotationStoreSseConfigArgsDict']]] = None,
                 store_format: Optional[pulumi.Input['AnnotationStoreStoreFormat']] = None,
                 store_options: Optional[pulumi.Input[Union['AnnotationStoreStoreOptionsPropertiesArgs', 'AnnotationStoreStoreOptionsPropertiesArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AnnotationStoreArgs.__new__(AnnotationStoreArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["reference"] = reference
            __props__.__dict__["sse_config"] = sse_config
            if store_format is None and not opts.urn:
                raise TypeError("Missing required property 'store_format'")
            __props__.__dict__["store_format"] = store_format
            __props__.__dict__["store_options"] = store_options
            __props__.__dict__["tags"] = tags
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["status_message"] = None
            __props__.__dict__["store_arn"] = None
            __props__.__dict__["store_size_bytes"] = None
            __props__.__dict__["update_time"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name", "reference", "sseConfig", "storeFormat", "storeOptions", "tags.*"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(AnnotationStore, __self__).__init__(
            'aws-native:omics:AnnotationStore',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AnnotationStore':
        """
        Get an existing AnnotationStore resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AnnotationStoreArgs.__new__(AnnotationStoreArgs)

        __props__.__dict__["aws_id"] = None
        __props__.__dict__["creation_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["reference"] = None
        __props__.__dict__["sse_config"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["status_message"] = None
        __props__.__dict__["store_arn"] = None
        __props__.__dict__["store_format"] = None
        __props__.__dict__["store_options"] = None
        __props__.__dict__["store_size_bytes"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["update_time"] = None
        return AnnotationStore(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The store's ID.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        When the store was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for the store.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Annotation Store.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def reference(self) -> pulumi.Output[Optional['outputs.AnnotationStoreReferenceItem']]:
        """
        The genome reference for the store's annotations.
        """
        return pulumi.get(self, "reference")

    @property
    @pulumi.getter(name="sseConfig")
    def sse_config(self) -> pulumi.Output[Optional['outputs.AnnotationStoreSseConfig']]:
        """
        The store's server-side encryption (SSE) settings.
        """
        return pulumi.get(self, "sse_config")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['AnnotationStoreStoreStatus']:
        """
        The store's status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusMessage")
    def status_message(self) -> pulumi.Output[str]:
        """
        The store's status message.
        """
        return pulumi.get(self, "status_message")

    @property
    @pulumi.getter(name="storeArn")
    def store_arn(self) -> pulumi.Output[str]:
        """
        The store's ARN.
        """
        return pulumi.get(self, "store_arn")

    @property
    @pulumi.getter(name="storeFormat")
    def store_format(self) -> pulumi.Output['AnnotationStoreStoreFormat']:
        """
        The annotation file format of the store.
        """
        return pulumi.get(self, "store_format")

    @property
    @pulumi.getter(name="storeOptions")
    def store_options(self) -> pulumi.Output[Optional['outputs.AnnotationStoreStoreOptionsProperties']]:
        """
        File parsing options for the annotation store.
        """
        return pulumi.get(self, "store_options")

    @property
    @pulumi.getter(name="storeSizeBytes")
    def store_size_bytes(self) -> pulumi.Output[float]:
        """
        The store's size in bytes.
        """
        return pulumi.get(self, "store_size_bytes")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags for the store.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        When the store was updated.
        """
        return pulumi.get(self, "update_time")

