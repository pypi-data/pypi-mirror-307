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

__all__ = ['StorageLensArgs', 'StorageLens']

@pulumi.input_type
class StorageLensArgs:
    def __init__(__self__, *,
                 storage_lens_configuration: pulumi.Input['StorageLensConfigurationArgs'],
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a StorageLens resource.
        :param pulumi.Input['StorageLensConfigurationArgs'] storage_lens_configuration: This resource contains the details Amazon S3 Storage Lens configuration.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: A set of tags (key-value pairs) for this Amazon S3 Storage Lens configuration.
        """
        pulumi.set(__self__, "storage_lens_configuration", storage_lens_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="storageLensConfiguration")
    def storage_lens_configuration(self) -> pulumi.Input['StorageLensConfigurationArgs']:
        """
        This resource contains the details Amazon S3 Storage Lens configuration.
        """
        return pulumi.get(self, "storage_lens_configuration")

    @storage_lens_configuration.setter
    def storage_lens_configuration(self, value: pulumi.Input['StorageLensConfigurationArgs']):
        pulumi.set(self, "storage_lens_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        A set of tags (key-value pairs) for this Amazon S3 Storage Lens configuration.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class StorageLens(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 storage_lens_configuration: Optional[pulumi.Input[Union['StorageLensConfigurationArgs', 'StorageLensConfigurationArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        The AWS::S3::StorageLens resource is an Amazon S3 resource type that you can use to create Storage Lens configurations.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['StorageLensConfigurationArgs', 'StorageLensConfigurationArgsDict']] storage_lens_configuration: This resource contains the details Amazon S3 Storage Lens configuration.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: A set of tags (key-value pairs) for this Amazon S3 Storage Lens configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StorageLensArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::S3::StorageLens resource is an Amazon S3 resource type that you can use to create Storage Lens configurations.

        :param str resource_name: The name of the resource.
        :param StorageLensArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StorageLensArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 storage_lens_configuration: Optional[pulumi.Input[Union['StorageLensConfigurationArgs', 'StorageLensConfigurationArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StorageLensArgs.__new__(StorageLensArgs)

            if storage_lens_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'storage_lens_configuration'")
            __props__.__dict__["storage_lens_configuration"] = storage_lens_configuration
            __props__.__dict__["tags"] = tags
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["storageLensConfiguration.id"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(StorageLens, __self__).__init__(
            'aws-native:s3:StorageLens',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageLens':
        """
        Get an existing StorageLens resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StorageLensArgs.__new__(StorageLensArgs)

        __props__.__dict__["storage_lens_configuration"] = None
        __props__.__dict__["tags"] = None
        return StorageLens(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="storageLensConfiguration")
    def storage_lens_configuration(self) -> pulumi.Output['outputs.StorageLensConfiguration']:
        """
        This resource contains the details Amazon S3 Storage Lens configuration.
        """
        return pulumi.get(self, "storage_lens_configuration")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        A set of tags (key-value pairs) for this Amazon S3 Storage Lens configuration.
        """
        return pulumi.get(self, "tags")

