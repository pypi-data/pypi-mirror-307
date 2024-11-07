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
    'GetComponentResult',
    'AwaitableGetComponentResult',
    'get_component',
    'get_component_output',
]

@pulumi.output_type
class GetComponentResult:
    def __init__(__self__, binding_properties=None, children=None, collection_properties=None, component_type=None, created_at=None, events=None, id=None, modified_at=None, name=None, overrides=None, properties=None, schema_version=None, source_id=None, tags=None, variants=None):
        if binding_properties and not isinstance(binding_properties, dict):
            raise TypeError("Expected argument 'binding_properties' to be a dict")
        pulumi.set(__self__, "binding_properties", binding_properties)
        if children and not isinstance(children, list):
            raise TypeError("Expected argument 'children' to be a list")
        pulumi.set(__self__, "children", children)
        if collection_properties and not isinstance(collection_properties, dict):
            raise TypeError("Expected argument 'collection_properties' to be a dict")
        pulumi.set(__self__, "collection_properties", collection_properties)
        if component_type and not isinstance(component_type, str):
            raise TypeError("Expected argument 'component_type' to be a str")
        pulumi.set(__self__, "component_type", component_type)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if events and not isinstance(events, dict):
            raise TypeError("Expected argument 'events' to be a dict")
        pulumi.set(__self__, "events", events)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if modified_at and not isinstance(modified_at, str):
            raise TypeError("Expected argument 'modified_at' to be a str")
        pulumi.set(__self__, "modified_at", modified_at)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if overrides and not isinstance(overrides, dict):
            raise TypeError("Expected argument 'overrides' to be a dict")
        pulumi.set(__self__, "overrides", overrides)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if schema_version and not isinstance(schema_version, str):
            raise TypeError("Expected argument 'schema_version' to be a str")
        pulumi.set(__self__, "schema_version", schema_version)
        if source_id and not isinstance(source_id, str):
            raise TypeError("Expected argument 'source_id' to be a str")
        pulumi.set(__self__, "source_id", source_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if variants and not isinstance(variants, list):
            raise TypeError("Expected argument 'variants' to be a list")
        pulumi.set(__self__, "variants", variants)

    @property
    @pulumi.getter(name="bindingProperties")
    def binding_properties(self) -> Optional[Mapping[str, 'outputs.ComponentBindingPropertiesValue']]:
        """
        The information to connect a component's properties to data at runtime. You can't specify `tags` as a valid property for `bindingProperties` .
        """
        return pulumi.get(self, "binding_properties")

    @property
    @pulumi.getter
    def children(self) -> Optional[Sequence['outputs.ComponentChild']]:
        """
        A list of the component's `ComponentChild` instances.
        """
        return pulumi.get(self, "children")

    @property
    @pulumi.getter(name="collectionProperties")
    def collection_properties(self) -> Optional[Mapping[str, 'outputs.ComponentDataConfiguration']]:
        """
        The data binding configuration for the component's properties. Use this for a collection component. You can't specify `tags` as a valid property for `collectionProperties` .
        """
        return pulumi.get(self, "collection_properties")

    @property
    @pulumi.getter(name="componentType")
    def component_type(self) -> Optional[str]:
        """
        The type of the component. This can be an Amplify custom UI component or another custom component.
        """
        return pulumi.get(self, "component_type")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The time that the component was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def events(self) -> Optional[Mapping[str, 'outputs.ComponentEvent']]:
        """
        Describes the events that can be raised on the component. Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique ID of the component.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> Optional[str]:
        """
        The time that the component was modified.
        """
        return pulumi.get(self, "modified_at")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the component.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def overrides(self) -> Optional[Mapping[str, Any]]:
        """
        Describes the component's properties that can be overriden in a customized instance of the component. You can't specify `tags` as a valid property for `overrides` .
        """
        return pulumi.get(self, "overrides")

    @property
    @pulumi.getter
    def properties(self) -> Optional[Mapping[str, 'outputs.ComponentProperty']]:
        """
        Describes the component's properties. You can't specify `tags` as a valid property for `properties` .
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="schemaVersion")
    def schema_version(self) -> Optional[str]:
        """
        The schema version of the component when it was imported.
        """
        return pulumi.get(self, "schema_version")

    @property
    @pulumi.getter(name="sourceId")
    def source_id(self) -> Optional[str]:
        """
        The unique ID of the component in its original source system, such as Figma.
        """
        return pulumi.get(self, "source_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        One or more key-value pairs to use when tagging the component.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def variants(self) -> Optional[Sequence['outputs.ComponentVariant']]:
        """
        A list of the component's variants. A variant is a unique style configuration of a main component.
        """
        return pulumi.get(self, "variants")


class AwaitableGetComponentResult(GetComponentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetComponentResult(
            binding_properties=self.binding_properties,
            children=self.children,
            collection_properties=self.collection_properties,
            component_type=self.component_type,
            created_at=self.created_at,
            events=self.events,
            id=self.id,
            modified_at=self.modified_at,
            name=self.name,
            overrides=self.overrides,
            properties=self.properties,
            schema_version=self.schema_version,
            source_id=self.source_id,
            tags=self.tags,
            variants=self.variants)


def get_component(app_id: Optional[str] = None,
                  environment_name: Optional[str] = None,
                  id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetComponentResult:
    """
    Definition of AWS::AmplifyUIBuilder::Component Resource Type


    :param str app_id: The unique ID of the Amplify app associated with the component.
    :param str environment_name: The name of the backend environment that is a part of the Amplify app.
    :param str id: The unique ID of the component.
    """
    __args__ = dict()
    __args__['appId'] = app_id
    __args__['environmentName'] = environment_name
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:amplifyuibuilder:getComponent', __args__, opts=opts, typ=GetComponentResult).value

    return AwaitableGetComponentResult(
        binding_properties=pulumi.get(__ret__, 'binding_properties'),
        children=pulumi.get(__ret__, 'children'),
        collection_properties=pulumi.get(__ret__, 'collection_properties'),
        component_type=pulumi.get(__ret__, 'component_type'),
        created_at=pulumi.get(__ret__, 'created_at'),
        events=pulumi.get(__ret__, 'events'),
        id=pulumi.get(__ret__, 'id'),
        modified_at=pulumi.get(__ret__, 'modified_at'),
        name=pulumi.get(__ret__, 'name'),
        overrides=pulumi.get(__ret__, 'overrides'),
        properties=pulumi.get(__ret__, 'properties'),
        schema_version=pulumi.get(__ret__, 'schema_version'),
        source_id=pulumi.get(__ret__, 'source_id'),
        tags=pulumi.get(__ret__, 'tags'),
        variants=pulumi.get(__ret__, 'variants'))
def get_component_output(app_id: Optional[pulumi.Input[str]] = None,
                         environment_name: Optional[pulumi.Input[str]] = None,
                         id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetComponentResult]:
    """
    Definition of AWS::AmplifyUIBuilder::Component Resource Type


    :param str app_id: The unique ID of the Amplify app associated with the component.
    :param str environment_name: The name of the backend environment that is a part of the Amplify app.
    :param str id: The unique ID of the component.
    """
    __args__ = dict()
    __args__['appId'] = app_id
    __args__['environmentName'] = environment_name
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:amplifyuibuilder:getComponent', __args__, opts=opts, typ=GetComponentResult)
    return __ret__.apply(lambda __response__: GetComponentResult(
        binding_properties=pulumi.get(__response__, 'binding_properties'),
        children=pulumi.get(__response__, 'children'),
        collection_properties=pulumi.get(__response__, 'collection_properties'),
        component_type=pulumi.get(__response__, 'component_type'),
        created_at=pulumi.get(__response__, 'created_at'),
        events=pulumi.get(__response__, 'events'),
        id=pulumi.get(__response__, 'id'),
        modified_at=pulumi.get(__response__, 'modified_at'),
        name=pulumi.get(__response__, 'name'),
        overrides=pulumi.get(__response__, 'overrides'),
        properties=pulumi.get(__response__, 'properties'),
        schema_version=pulumi.get(__response__, 'schema_version'),
        source_id=pulumi.get(__response__, 'source_id'),
        tags=pulumi.get(__response__, 'tags'),
        variants=pulumi.get(__response__, 'variants')))
