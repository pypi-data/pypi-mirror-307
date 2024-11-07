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
    'GetResourceDefaultVersionResult',
    'AwaitableGetResourceDefaultVersionResult',
    'get_resource_default_version',
    'get_resource_default_version_output',
]

@pulumi.output_type
class GetResourceDefaultVersionResult:
    def __init__(__self__, arn=None, type_name=None, type_version_arn=None, version_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if type_name and not isinstance(type_name, str):
            raise TypeError("Expected argument 'type_name' to be a str")
        pulumi.set(__self__, "type_name", type_name)
        if type_version_arn and not isinstance(type_version_arn, str):
            raise TypeError("Expected argument 'type_version_arn' to be a str")
        pulumi.set(__self__, "type_version_arn", type_version_arn)
        if version_id and not isinstance(version_id, str):
            raise TypeError("Expected argument 'version_id' to be a str")
        pulumi.set(__self__, "version_id", version_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the type. This is used to uniquely identify a ResourceDefaultVersion
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> Optional[str]:
        """
        The name of the type being registered.

        We recommend that type names adhere to the following pattern: company_or_organization::service::type.
        """
        return pulumi.get(self, "type_name")

    @property
    @pulumi.getter(name="typeVersionArn")
    def type_version_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the type version.
        """
        return pulumi.get(self, "type_version_arn")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[str]:
        """
        The ID of an existing version of the resource to set as the default.
        """
        return pulumi.get(self, "version_id")


class AwaitableGetResourceDefaultVersionResult(GetResourceDefaultVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourceDefaultVersionResult(
            arn=self.arn,
            type_name=self.type_name,
            type_version_arn=self.type_version_arn,
            version_id=self.version_id)


def get_resource_default_version(arn: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourceDefaultVersionResult:
    """
    The default version of a resource that has been registered in the CloudFormation Registry.


    :param str arn: The Amazon Resource Name (ARN) of the type. This is used to uniquely identify a ResourceDefaultVersion
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudformation:getResourceDefaultVersion', __args__, opts=opts, typ=GetResourceDefaultVersionResult).value

    return AwaitableGetResourceDefaultVersionResult(
        arn=pulumi.get(__ret__, 'arn'),
        type_name=pulumi.get(__ret__, 'type_name'),
        type_version_arn=pulumi.get(__ret__, 'type_version_arn'),
        version_id=pulumi.get(__ret__, 'version_id'))
def get_resource_default_version_output(arn: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourceDefaultVersionResult]:
    """
    The default version of a resource that has been registered in the CloudFormation Registry.


    :param str arn: The Amazon Resource Name (ARN) of the type. This is used to uniquely identify a ResourceDefaultVersion
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudformation:getResourceDefaultVersion', __args__, opts=opts, typ=GetResourceDefaultVersionResult)
    return __ret__.apply(lambda __response__: GetResourceDefaultVersionResult(
        arn=pulumi.get(__response__, 'arn'),
        type_name=pulumi.get(__response__, 'type_name'),
        type_version_arn=pulumi.get(__response__, 'type_version_arn'),
        version_id=pulumi.get(__response__, 'version_id')))
