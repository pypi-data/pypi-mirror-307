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

__all__ = ['PrefixListArgs', 'PrefixList']

@pulumi.input_type
class PrefixListArgs:
    def __init__(__self__, *,
                 address_family: pulumi.Input['PrefixListAddressFamily'],
                 entries: Optional[pulumi.Input[Sequence[pulumi.Input['PrefixListEntryArgs']]]] = None,
                 max_entries: Optional[pulumi.Input[int]] = None,
                 prefix_list_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a PrefixList resource.
        :param pulumi.Input['PrefixListAddressFamily'] address_family: Ip Version of Prefix List.
        :param pulumi.Input[Sequence[pulumi.Input['PrefixListEntryArgs']]] entries: Entries of Prefix List.
        :param pulumi.Input[int] max_entries: Max Entries of Prefix List.
        :param pulumi.Input[str] prefix_list_name: Name of Prefix List.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: Tags for Prefix List
        """
        pulumi.set(__self__, "address_family", address_family)
        if entries is not None:
            pulumi.set(__self__, "entries", entries)
        if max_entries is not None:
            pulumi.set(__self__, "max_entries", max_entries)
        if prefix_list_name is not None:
            pulumi.set(__self__, "prefix_list_name", prefix_list_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="addressFamily")
    def address_family(self) -> pulumi.Input['PrefixListAddressFamily']:
        """
        Ip Version of Prefix List.
        """
        return pulumi.get(self, "address_family")

    @address_family.setter
    def address_family(self, value: pulumi.Input['PrefixListAddressFamily']):
        pulumi.set(self, "address_family", value)

    @property
    @pulumi.getter
    def entries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrefixListEntryArgs']]]]:
        """
        Entries of Prefix List.
        """
        return pulumi.get(self, "entries")

    @entries.setter
    def entries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrefixListEntryArgs']]]]):
        pulumi.set(self, "entries", value)

    @property
    @pulumi.getter(name="maxEntries")
    def max_entries(self) -> Optional[pulumi.Input[int]]:
        """
        Max Entries of Prefix List.
        """
        return pulumi.get(self, "max_entries")

    @max_entries.setter
    def max_entries(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_entries", value)

    @property
    @pulumi.getter(name="prefixListName")
    def prefix_list_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Prefix List.
        """
        return pulumi.get(self, "prefix_list_name")

    @prefix_list_name.setter
    def prefix_list_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix_list_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        Tags for Prefix List
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class PrefixList(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_family: Optional[pulumi.Input['PrefixListAddressFamily']] = None,
                 entries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['PrefixListEntryArgs', 'PrefixListEntryArgsDict']]]]] = None,
                 max_entries: Optional[pulumi.Input[int]] = None,
                 prefix_list_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource schema of AWS::EC2::PrefixList Type

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        new_prefix_list = aws_native.ec2.PrefixList("newPrefixList",
            prefix_list_name="vpc-1-servers",
            address_family=aws_native.ec2.PrefixListAddressFamily.I_PV4,
            max_entries=10,
            entries=[
                {
                    "cidr": "10.0.0.5/32",
                    "description": "Server 1",
                },
                {
                    "cidr": "10.0.0.10/32",
                    "description": "Server 2",
                },
            ],
            tags=[{
                "key": "Name",
                "value": "VPC-1-Servers",
            }])

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        new_prefix_list = aws_native.ec2.PrefixList("newPrefixList",
            prefix_list_name="vpc-1-servers",
            address_family=aws_native.ec2.PrefixListAddressFamily.I_PV4,
            max_entries=10,
            entries=[
                {
                    "cidr": "10.0.0.5/32",
                    "description": "Server 1",
                },
                {
                    "cidr": "10.0.0.10/32",
                    "description": "Server 2",
                },
            ],
            tags=[{
                "key": "Name",
                "value": "VPC-1-Servers",
            }])

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['PrefixListAddressFamily'] address_family: Ip Version of Prefix List.
        :param pulumi.Input[Sequence[pulumi.Input[Union['PrefixListEntryArgs', 'PrefixListEntryArgsDict']]]] entries: Entries of Prefix List.
        :param pulumi.Input[int] max_entries: Max Entries of Prefix List.
        :param pulumi.Input[str] prefix_list_name: Name of Prefix List.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: Tags for Prefix List
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrefixListArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema of AWS::EC2::PrefixList Type

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        new_prefix_list = aws_native.ec2.PrefixList("newPrefixList",
            prefix_list_name="vpc-1-servers",
            address_family=aws_native.ec2.PrefixListAddressFamily.I_PV4,
            max_entries=10,
            entries=[
                {
                    "cidr": "10.0.0.5/32",
                    "description": "Server 1",
                },
                {
                    "cidr": "10.0.0.10/32",
                    "description": "Server 2",
                },
            ],
            tags=[{
                "key": "Name",
                "value": "VPC-1-Servers",
            }])

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        new_prefix_list = aws_native.ec2.PrefixList("newPrefixList",
            prefix_list_name="vpc-1-servers",
            address_family=aws_native.ec2.PrefixListAddressFamily.I_PV4,
            max_entries=10,
            entries=[
                {
                    "cidr": "10.0.0.5/32",
                    "description": "Server 1",
                },
                {
                    "cidr": "10.0.0.10/32",
                    "description": "Server 2",
                },
            ],
            tags=[{
                "key": "Name",
                "value": "VPC-1-Servers",
            }])

        ```

        :param str resource_name: The name of the resource.
        :param PrefixListArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrefixListArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_family: Optional[pulumi.Input['PrefixListAddressFamily']] = None,
                 entries: Optional[pulumi.Input[Sequence[pulumi.Input[Union['PrefixListEntryArgs', 'PrefixListEntryArgsDict']]]]] = None,
                 max_entries: Optional[pulumi.Input[int]] = None,
                 prefix_list_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrefixListArgs.__new__(PrefixListArgs)

            if address_family is None and not opts.urn:
                raise TypeError("Missing required property 'address_family'")
            __props__.__dict__["address_family"] = address_family
            __props__.__dict__["entries"] = entries
            __props__.__dict__["max_entries"] = max_entries
            __props__.__dict__["prefix_list_name"] = prefix_list_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["prefix_list_id"] = None
            __props__.__dict__["version"] = None
        super(PrefixList, __self__).__init__(
            'aws-native:ec2:PrefixList',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrefixList':
        """
        Get an existing PrefixList resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrefixListArgs.__new__(PrefixListArgs)

        __props__.__dict__["address_family"] = None
        __props__.__dict__["arn"] = None
        __props__.__dict__["entries"] = None
        __props__.__dict__["max_entries"] = None
        __props__.__dict__["owner_id"] = None
        __props__.__dict__["prefix_list_id"] = None
        __props__.__dict__["prefix_list_name"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["version"] = None
        return PrefixList(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressFamily")
    def address_family(self) -> pulumi.Output['PrefixListAddressFamily']:
        """
        Ip Version of Prefix List.
        """
        return pulumi.get(self, "address_family")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the Prefix List.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def entries(self) -> pulumi.Output[Optional[Sequence['outputs.PrefixListEntry']]]:
        """
        Entries of Prefix List.
        """
        return pulumi.get(self, "entries")

    @property
    @pulumi.getter(name="maxEntries")
    def max_entries(self) -> pulumi.Output[Optional[int]]:
        """
        Max Entries of Prefix List.
        """
        return pulumi.get(self, "max_entries")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        Owner Id of Prefix List.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> pulumi.Output[str]:
        """
        Id of Prefix List.
        """
        return pulumi.get(self, "prefix_list_id")

    @property
    @pulumi.getter(name="prefixListName")
    def prefix_list_name(self) -> pulumi.Output[str]:
        """
        Name of Prefix List.
        """
        return pulumi.get(self, "prefix_list_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        Tags for Prefix List
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        Version of Prefix List.
        """
        return pulumi.get(self, "version")

