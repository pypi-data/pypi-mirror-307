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

__all__ = ['NetworkInsightsAccessScopeArgs', 'NetworkInsightsAccessScope']

@pulumi.input_type
class NetworkInsightsAccessScopeArgs:
    def __init__(__self__, *,
                 exclude_paths: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]]] = None,
                 match_paths: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a NetworkInsightsAccessScope resource.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]] exclude_paths: The paths to exclude.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]] match_paths: The paths to match.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags.
        """
        if exclude_paths is not None:
            pulumi.set(__self__, "exclude_paths", exclude_paths)
        if match_paths is not None:
            pulumi.set(__self__, "match_paths", match_paths)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="excludePaths")
    def exclude_paths(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]]]:
        """
        The paths to exclude.
        """
        return pulumi.get(self, "exclude_paths")

    @exclude_paths.setter
    def exclude_paths(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]]]):
        pulumi.set(self, "exclude_paths", value)

    @property
    @pulumi.getter(name="matchPaths")
    def match_paths(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]]]:
        """
        The paths to match.
        """
        return pulumi.get(self, "match_paths")

    @match_paths.setter
    def match_paths(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInsightsAccessScopeAccessScopePathRequestArgs']]]]):
        pulumi.set(self, "match_paths", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class NetworkInsightsAccessScope(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 exclude_paths: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkInsightsAccessScopeAccessScopePathRequestArgs', 'NetworkInsightsAccessScopeAccessScopePathRequestArgsDict']]]]] = None,
                 match_paths: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkInsightsAccessScopeAccessScopePathRequestArgs', 'NetworkInsightsAccessScopeAccessScopePathRequestArgsDict']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::EC2::NetworkInsightsAccessScope

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['NetworkInsightsAccessScopeAccessScopePathRequestArgs', 'NetworkInsightsAccessScopeAccessScopePathRequestArgsDict']]]] exclude_paths: The paths to exclude.
        :param pulumi.Input[Sequence[pulumi.Input[Union['NetworkInsightsAccessScopeAccessScopePathRequestArgs', 'NetworkInsightsAccessScopeAccessScopePathRequestArgsDict']]]] match_paths: The paths to match.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[NetworkInsightsAccessScopeArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::EC2::NetworkInsightsAccessScope

        :param str resource_name: The name of the resource.
        :param NetworkInsightsAccessScopeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkInsightsAccessScopeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 exclude_paths: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkInsightsAccessScopeAccessScopePathRequestArgs', 'NetworkInsightsAccessScopeAccessScopePathRequestArgsDict']]]]] = None,
                 match_paths: Optional[pulumi.Input[Sequence[pulumi.Input[Union['NetworkInsightsAccessScopeAccessScopePathRequestArgs', 'NetworkInsightsAccessScopeAccessScopePathRequestArgsDict']]]]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkInsightsAccessScopeArgs.__new__(NetworkInsightsAccessScopeArgs)

            __props__.__dict__["exclude_paths"] = exclude_paths
            __props__.__dict__["match_paths"] = match_paths
            __props__.__dict__["tags"] = tags
            __props__.__dict__["created_date"] = None
            __props__.__dict__["network_insights_access_scope_arn"] = None
            __props__.__dict__["network_insights_access_scope_id"] = None
            __props__.__dict__["updated_date"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["excludePaths[*]", "matchPaths[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(NetworkInsightsAccessScope, __self__).__init__(
            'aws-native:ec2:NetworkInsightsAccessScope',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkInsightsAccessScope':
        """
        Get an existing NetworkInsightsAccessScope resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkInsightsAccessScopeArgs.__new__(NetworkInsightsAccessScopeArgs)

        __props__.__dict__["created_date"] = None
        __props__.__dict__["exclude_paths"] = None
        __props__.__dict__["match_paths"] = None
        __props__.__dict__["network_insights_access_scope_arn"] = None
        __props__.__dict__["network_insights_access_scope_id"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["updated_date"] = None
        return NetworkInsightsAccessScope(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        The creation date.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="excludePaths")
    def exclude_paths(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkInsightsAccessScopeAccessScopePathRequest']]]:
        """
        The paths to exclude.
        """
        return pulumi.get(self, "exclude_paths")

    @property
    @pulumi.getter(name="matchPaths")
    def match_paths(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkInsightsAccessScopeAccessScopePathRequest']]]:
        """
        The paths to match.
        """
        return pulumi.get(self, "match_paths")

    @property
    @pulumi.getter(name="networkInsightsAccessScopeArn")
    def network_insights_access_scope_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Network Access Scope.
        """
        return pulumi.get(self, "network_insights_access_scope_arn")

    @property
    @pulumi.getter(name="networkInsightsAccessScopeId")
    def network_insights_access_scope_id(self) -> pulumi.Output[str]:
        """
        The ID of the Network Access Scope.
        """
        return pulumi.get(self, "network_insights_access_scope_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updatedDate")
    def updated_date(self) -> pulumi.Output[str]:
        """
        The last updated date.
        """
        return pulumi.get(self, "updated_date")

