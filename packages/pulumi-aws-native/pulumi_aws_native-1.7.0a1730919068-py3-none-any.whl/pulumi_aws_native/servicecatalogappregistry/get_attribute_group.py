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

__all__ = [
    'GetAttributeGroupResult',
    'AwaitableGetAttributeGroupResult',
    'get_attribute_group',
    'get_attribute_group_output',
]

@pulumi.output_type
class GetAttributeGroupResult:
    def __init__(__self__, arn=None, attributes=None, description=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if attributes and not isinstance(attributes, dict):
            raise TypeError("Expected argument 'attributes' to be a dict")
        pulumi.set(__self__, "attributes", attributes)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon resource name (ARN) that specifies the attribute group across services.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def attributes(self) -> Optional[Any]:
        """
        A nested object in a JSON or YAML template that supports arbitrary definitions. Represents the attributes in an attribute group that describes an application and its components.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ServiceCatalogAppRegistry::AttributeGroup` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "attributes")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the attribute group. 
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The globally unique attribute group identifier of the attribute group.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the attribute group. 
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Key-value pairs you can use to associate with the attribute group.
        """
        return pulumi.get(self, "tags")


class AwaitableGetAttributeGroupResult(GetAttributeGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttributeGroupResult(
            arn=self.arn,
            attributes=self.attributes,
            description=self.description,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_attribute_group(id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttributeGroupResult:
    """
    Resource Schema for AWS::ServiceCatalogAppRegistry::AttributeGroup.


    :param str id: The globally unique attribute group identifier of the attribute group.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:servicecatalogappregistry:getAttributeGroup', __args__, opts=opts, typ=GetAttributeGroupResult).value

    return AwaitableGetAttributeGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        attributes=pulumi.get(__ret__, 'attributes'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_attribute_group_output(id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttributeGroupResult]:
    """
    Resource Schema for AWS::ServiceCatalogAppRegistry::AttributeGroup.


    :param str id: The globally unique attribute group identifier of the attribute group.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:servicecatalogappregistry:getAttributeGroup', __args__, opts=opts, typ=GetAttributeGroupResult)
    return __ret__.apply(lambda __response__: GetAttributeGroupResult(
        arn=pulumi.get(__response__, 'arn'),
        attributes=pulumi.get(__response__, 'attributes'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
