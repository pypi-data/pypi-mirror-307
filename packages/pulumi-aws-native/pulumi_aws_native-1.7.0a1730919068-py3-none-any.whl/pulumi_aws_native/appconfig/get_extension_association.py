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
    'GetExtensionAssociationResult',
    'AwaitableGetExtensionAssociationResult',
    'get_extension_association',
    'get_extension_association_output',
]

@pulumi.output_type
class GetExtensionAssociationResult:
    def __init__(__self__, arn=None, extension_arn=None, id=None, parameters=None, resource_arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if extension_arn and not isinstance(extension_arn, str):
            raise TypeError("Expected argument 'extension_arn' to be a str")
        pulumi.set(__self__, "extension_arn", extension_arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if resource_arn and not isinstance(resource_arn, str):
            raise TypeError("Expected argument 'resource_arn' to be a str")
        pulumi.set(__self__, "resource_arn", resource_arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the extension defined in the association.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="extensionArn")
    def extension_arn(self) -> Optional[str]:
        """
        The ARN of the extension defined in the association.
        """
        return pulumi.get(self, "extension_arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The system-generated ID for the association.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, str]]:
        """
        The parameter names and values defined in the extensions. Extension parameters marked `Required` must be entered for this field.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[str]:
        """
        The ARNs of applications, configuration profiles, or environments defined in the association.
        """
        return pulumi.get(self, "resource_arn")


class AwaitableGetExtensionAssociationResult(GetExtensionAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExtensionAssociationResult(
            arn=self.arn,
            extension_arn=self.extension_arn,
            id=self.id,
            parameters=self.parameters,
            resource_arn=self.resource_arn)


def get_extension_association(id: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExtensionAssociationResult:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str id: The system-generated ID for the association.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appconfig:getExtensionAssociation', __args__, opts=opts, typ=GetExtensionAssociationResult).value

    return AwaitableGetExtensionAssociationResult(
        arn=pulumi.get(__ret__, 'arn'),
        extension_arn=pulumi.get(__ret__, 'extension_arn'),
        id=pulumi.get(__ret__, 'id'),
        parameters=pulumi.get(__ret__, 'parameters'),
        resource_arn=pulumi.get(__ret__, 'resource_arn'))
def get_extension_association_output(id: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExtensionAssociationResult]:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str id: The system-generated ID for the association.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:appconfig:getExtensionAssociation', __args__, opts=opts, typ=GetExtensionAssociationResult)
    return __ret__.apply(lambda __response__: GetExtensionAssociationResult(
        arn=pulumi.get(__response__, 'arn'),
        extension_arn=pulumi.get(__response__, 'extension_arn'),
        id=pulumi.get(__response__, 'id'),
        parameters=pulumi.get(__response__, 'parameters'),
        resource_arn=pulumi.get(__response__, 'resource_arn')))
