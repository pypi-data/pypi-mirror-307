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

__all__ = [
    'GetComponentTypeResult',
    'AwaitableGetComponentTypeResult',
    'get_component_type',
    'get_component_type_output',
]

@pulumi.output_type
class GetComponentTypeResult:
    def __init__(__self__, arn=None, composite_component_types=None, creation_date_time=None, description=None, extends_from=None, functions=None, is_abstract=None, is_schema_initialized=None, is_singleton=None, property_definitions=None, property_groups=None, status=None, tags=None, update_date_time=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if composite_component_types and not isinstance(composite_component_types, dict):
            raise TypeError("Expected argument 'composite_component_types' to be a dict")
        pulumi.set(__self__, "composite_component_types", composite_component_types)
        if creation_date_time and not isinstance(creation_date_time, str):
            raise TypeError("Expected argument 'creation_date_time' to be a str")
        pulumi.set(__self__, "creation_date_time", creation_date_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if extends_from and not isinstance(extends_from, list):
            raise TypeError("Expected argument 'extends_from' to be a list")
        pulumi.set(__self__, "extends_from", extends_from)
        if functions and not isinstance(functions, dict):
            raise TypeError("Expected argument 'functions' to be a dict")
        pulumi.set(__self__, "functions", functions)
        if is_abstract and not isinstance(is_abstract, bool):
            raise TypeError("Expected argument 'is_abstract' to be a bool")
        pulumi.set(__self__, "is_abstract", is_abstract)
        if is_schema_initialized and not isinstance(is_schema_initialized, bool):
            raise TypeError("Expected argument 'is_schema_initialized' to be a bool")
        pulumi.set(__self__, "is_schema_initialized", is_schema_initialized)
        if is_singleton and not isinstance(is_singleton, bool):
            raise TypeError("Expected argument 'is_singleton' to be a bool")
        pulumi.set(__self__, "is_singleton", is_singleton)
        if property_definitions and not isinstance(property_definitions, dict):
            raise TypeError("Expected argument 'property_definitions' to be a dict")
        pulumi.set(__self__, "property_definitions", property_definitions)
        if property_groups and not isinstance(property_groups, dict):
            raise TypeError("Expected argument 'property_groups' to be a dict")
        pulumi.set(__self__, "property_groups", property_groups)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if update_date_time and not isinstance(update_date_time, str):
            raise TypeError("Expected argument 'update_date_time' to be a str")
        pulumi.set(__self__, "update_date_time", update_date_time)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the component type.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="compositeComponentTypes")
    def composite_component_types(self) -> Optional[Mapping[str, 'outputs.ComponentTypeCompositeComponentType']]:
        """
        An map of the composite component types in the component type. Each composite component type's key must be unique to this map.
        """
        return pulumi.get(self, "composite_component_types")

    @property
    @pulumi.getter(name="creationDateTime")
    def creation_date_time(self) -> Optional[str]:
        """
        The date and time when the component type was created.
        """
        return pulumi.get(self, "creation_date_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the component type.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="extendsFrom")
    def extends_from(self) -> Optional[Sequence[str]]:
        """
        Specifies the parent component type to extend.
        """
        return pulumi.get(self, "extends_from")

    @property
    @pulumi.getter
    def functions(self) -> Optional[Mapping[str, 'outputs.ComponentTypeFunction']]:
        """
        a Map of functions in the component type. Each function's key must be unique to this map.
        """
        return pulumi.get(self, "functions")

    @property
    @pulumi.getter(name="isAbstract")
    def is_abstract(self) -> Optional[bool]:
        """
        A Boolean value that specifies whether the component type is abstract.
        """
        return pulumi.get(self, "is_abstract")

    @property
    @pulumi.getter(name="isSchemaInitialized")
    def is_schema_initialized(self) -> Optional[bool]:
        """
        A Boolean value that specifies whether the component type has a schema initializer and that the schema initializer has run.
        """
        return pulumi.get(self, "is_schema_initialized")

    @property
    @pulumi.getter(name="isSingleton")
    def is_singleton(self) -> Optional[bool]:
        """
        A Boolean value that specifies whether an entity can have more than one component of this type.
        """
        return pulumi.get(self, "is_singleton")

    @property
    @pulumi.getter(name="propertyDefinitions")
    def property_definitions(self) -> Optional[Mapping[str, 'outputs.ComponentTypePropertyDefinition']]:
        """
        An map of the property definitions in the component type. Each property definition's key must be unique to this map.
        """
        return pulumi.get(self, "property_definitions")

    @property
    @pulumi.getter(name="propertyGroups")
    def property_groups(self) -> Optional[Mapping[str, 'outputs.ComponentTypePropertyGroup']]:
        """
        An map of the property groups in the component type. Each property group's key must be unique to this map.
        """
        return pulumi.get(self, "property_groups")

    @property
    @pulumi.getter
    def status(self) -> Optional['outputs.ComponentTypeStatus']:
        """
        The current status of the component type.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        A map of key-value pairs to associate with a resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updateDateTime")
    def update_date_time(self) -> Optional[str]:
        """
        The last date and time when the component type was updated.
        """
        return pulumi.get(self, "update_date_time")


class AwaitableGetComponentTypeResult(GetComponentTypeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetComponentTypeResult(
            arn=self.arn,
            composite_component_types=self.composite_component_types,
            creation_date_time=self.creation_date_time,
            description=self.description,
            extends_from=self.extends_from,
            functions=self.functions,
            is_abstract=self.is_abstract,
            is_schema_initialized=self.is_schema_initialized,
            is_singleton=self.is_singleton,
            property_definitions=self.property_definitions,
            property_groups=self.property_groups,
            status=self.status,
            tags=self.tags,
            update_date_time=self.update_date_time)


def get_component_type(component_type_id: Optional[str] = None,
                       workspace_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetComponentTypeResult:
    """
    Resource schema for AWS::IoTTwinMaker::ComponentType


    :param str component_type_id: The ID of the component type.
    :param str workspace_id: The ID of the workspace that contains the component type.
    """
    __args__ = dict()
    __args__['componentTypeId'] = component_type_id
    __args__['workspaceId'] = workspace_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iottwinmaker:getComponentType', __args__, opts=opts, typ=GetComponentTypeResult).value

    return AwaitableGetComponentTypeResult(
        arn=pulumi.get(__ret__, 'arn'),
        composite_component_types=pulumi.get(__ret__, 'composite_component_types'),
        creation_date_time=pulumi.get(__ret__, 'creation_date_time'),
        description=pulumi.get(__ret__, 'description'),
        extends_from=pulumi.get(__ret__, 'extends_from'),
        functions=pulumi.get(__ret__, 'functions'),
        is_abstract=pulumi.get(__ret__, 'is_abstract'),
        is_schema_initialized=pulumi.get(__ret__, 'is_schema_initialized'),
        is_singleton=pulumi.get(__ret__, 'is_singleton'),
        property_definitions=pulumi.get(__ret__, 'property_definitions'),
        property_groups=pulumi.get(__ret__, 'property_groups'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        update_date_time=pulumi.get(__ret__, 'update_date_time'))
def get_component_type_output(component_type_id: Optional[pulumi.Input[str]] = None,
                              workspace_id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetComponentTypeResult]:
    """
    Resource schema for AWS::IoTTwinMaker::ComponentType


    :param str component_type_id: The ID of the component type.
    :param str workspace_id: The ID of the workspace that contains the component type.
    """
    __args__ = dict()
    __args__['componentTypeId'] = component_type_id
    __args__['workspaceId'] = workspace_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iottwinmaker:getComponentType', __args__, opts=opts, typ=GetComponentTypeResult)
    return __ret__.apply(lambda __response__: GetComponentTypeResult(
        arn=pulumi.get(__response__, 'arn'),
        composite_component_types=pulumi.get(__response__, 'composite_component_types'),
        creation_date_time=pulumi.get(__response__, 'creation_date_time'),
        description=pulumi.get(__response__, 'description'),
        extends_from=pulumi.get(__response__, 'extends_from'),
        functions=pulumi.get(__response__, 'functions'),
        is_abstract=pulumi.get(__response__, 'is_abstract'),
        is_schema_initialized=pulumi.get(__response__, 'is_schema_initialized'),
        is_singleton=pulumi.get(__response__, 'is_singleton'),
        property_definitions=pulumi.get(__response__, 'property_definitions'),
        property_groups=pulumi.get(__response__, 'property_groups'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags'),
        update_date_time=pulumi.get(__response__, 'update_date_time')))
