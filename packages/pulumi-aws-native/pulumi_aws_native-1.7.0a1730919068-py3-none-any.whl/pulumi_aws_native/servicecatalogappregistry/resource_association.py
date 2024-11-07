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

__all__ = ['ResourceAssociationArgs', 'ResourceAssociation']

@pulumi.input_type
class ResourceAssociationArgs:
    def __init__(__self__, *,
                 application: pulumi.Input[str],
                 resource: pulumi.Input[str],
                 resource_type: pulumi.Input['ResourceAssociationResourceType']):
        """
        The set of arguments for constructing a ResourceAssociation resource.
        :param pulumi.Input[str] application: The name or the Id of the Application.
        :param pulumi.Input[str] resource: The name or the Id of the Resource.
        :param pulumi.Input['ResourceAssociationResourceType'] resource_type: The type of the CFN Resource for now it's enum CFN_STACK.
        """
        pulumi.set(__self__, "application", application)
        pulumi.set(__self__, "resource", resource)
        pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter
    def application(self) -> pulumi.Input[str]:
        """
        The name or the Id of the Application.
        """
        return pulumi.get(self, "application")

    @application.setter
    def application(self, value: pulumi.Input[str]):
        pulumi.set(self, "application", value)

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Input[str]:
        """
        The name or the Id of the Resource.
        """
        return pulumi.get(self, "resource")

    @resource.setter
    def resource(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input['ResourceAssociationResourceType']:
        """
        The type of the CFN Resource for now it's enum CFN_STACK.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input['ResourceAssociationResourceType']):
        pulumi.set(self, "resource_type", value)


class ResourceAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application: Optional[pulumi.Input[str]] = None,
                 resource: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input['ResourceAssociationResourceType']] = None,
                 __props__=None):
        """
        Resource Schema for AWS::ServiceCatalogAppRegistry::ResourceAssociation

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application: The name or the Id of the Application.
        :param pulumi.Input[str] resource: The name or the Id of the Resource.
        :param pulumi.Input['ResourceAssociationResourceType'] resource_type: The type of the CFN Resource for now it's enum CFN_STACK.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Schema for AWS::ServiceCatalogAppRegistry::ResourceAssociation

        :param str resource_name: The name of the resource.
        :param ResourceAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application: Optional[pulumi.Input[str]] = None,
                 resource: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input['ResourceAssociationResourceType']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceAssociationArgs.__new__(ResourceAssociationArgs)

            if application is None and not opts.urn:
                raise TypeError("Missing required property 'application'")
            __props__.__dict__["application"] = application
            if resource is None and not opts.urn:
                raise TypeError("Missing required property 'resource'")
            __props__.__dict__["resource"] = resource
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__.__dict__["resource_type"] = resource_type
            __props__.__dict__["application_arn"] = None
            __props__.__dict__["resource_arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["application", "resource", "resourceType"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ResourceAssociation, __self__).__init__(
            'aws-native:servicecatalogappregistry:ResourceAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourceAssociation':
        """
        Get an existing ResourceAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourceAssociationArgs.__new__(ResourceAssociationArgs)

        __props__.__dict__["application"] = None
        __props__.__dict__["application_arn"] = None
        __props__.__dict__["resource"] = None
        __props__.__dict__["resource_arn"] = None
        __props__.__dict__["resource_type"] = None
        return ResourceAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def application(self) -> pulumi.Output[str]:
        """
        The name or the Id of the Application.
        """
        return pulumi.get(self, "application")

    @property
    @pulumi.getter(name="applicationArn")
    def application_arn(self) -> pulumi.Output[str]:
        """
        The Amazon resource name (ARN) that specifies the application.
        """
        return pulumi.get(self, "application_arn")

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Output[str]:
        """
        The name or the Id of the Resource.
        """
        return pulumi.get(self, "resource")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Output[str]:
        """
        The Amazon resource name (ARN) that specifies the resource.
        """
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output['ResourceAssociationResourceType']:
        """
        The type of the CFN Resource for now it's enum CFN_STACK.
        """
        return pulumi.get(self, "resource_type")

