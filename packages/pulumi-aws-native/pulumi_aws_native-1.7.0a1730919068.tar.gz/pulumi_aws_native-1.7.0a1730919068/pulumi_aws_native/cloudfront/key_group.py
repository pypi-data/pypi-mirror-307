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
from ._inputs import *

__all__ = ['KeyGroupArgs', 'KeyGroup']

@pulumi.input_type
class KeyGroupArgs:
    def __init__(__self__, *,
                 key_group_config: pulumi.Input['KeyGroupConfigArgs']):
        """
        The set of arguments for constructing a KeyGroup resource.
        :param pulumi.Input['KeyGroupConfigArgs'] key_group_config: The key group configuration.
        """
        pulumi.set(__self__, "key_group_config", key_group_config)

    @property
    @pulumi.getter(name="keyGroupConfig")
    def key_group_config(self) -> pulumi.Input['KeyGroupConfigArgs']:
        """
        The key group configuration.
        """
        return pulumi.get(self, "key_group_config")

    @key_group_config.setter
    def key_group_config(self, value: pulumi.Input['KeyGroupConfigArgs']):
        pulumi.set(self, "key_group_config", value)


class KeyGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_group_config: Optional[pulumi.Input[Union['KeyGroupConfigArgs', 'KeyGroupConfigArgsDict']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::CloudFront::KeyGroup

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['KeyGroupConfigArgs', 'KeyGroupConfigArgsDict']] key_group_config: The key group configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KeyGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::CloudFront::KeyGroup

        :param str resource_name: The name of the resource.
        :param KeyGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_group_config: Optional[pulumi.Input[Union['KeyGroupConfigArgs', 'KeyGroupConfigArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KeyGroupArgs.__new__(KeyGroupArgs)

            if key_group_config is None and not opts.urn:
                raise TypeError("Missing required property 'key_group_config'")
            __props__.__dict__["key_group_config"] = key_group_config
            __props__.__dict__["aws_id"] = None
            __props__.__dict__["last_modified_time"] = None
        super(KeyGroup, __self__).__init__(
            'aws-native:cloudfront:KeyGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'KeyGroup':
        """
        Get an existing KeyGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = KeyGroupArgs.__new__(KeyGroupArgs)

        __props__.__dict__["aws_id"] = None
        __props__.__dict__["key_group_config"] = None
        __props__.__dict__["last_modified_time"] = None
        return KeyGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="awsId")
    def aws_id(self) -> pulumi.Output[str]:
        """
        The identifier for the key group.
        """
        return pulumi.get(self, "aws_id")

    @property
    @pulumi.getter(name="keyGroupConfig")
    def key_group_config(self) -> pulumi.Output['outputs.KeyGroupConfig']:
        """
        The key group configuration.
        """
        return pulumi.get(self, "key_group_config")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        The date and time when the key group was last modified.
        """
        return pulumi.get(self, "last_modified_time")

