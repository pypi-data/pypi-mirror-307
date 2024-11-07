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
    'GetVersionResult',
    'AwaitableGetVersionResult',
    'get_version',
    'get_version_output',
]

@pulumi.output_type
class GetVersionResult:
    def __init__(__self__, function_arn=None, version=None):
        if function_arn and not isinstance(function_arn, str):
            raise TypeError("Expected argument 'function_arn' to be a str")
        pulumi.set(__self__, "function_arn", function_arn)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="functionArn")
    def function_arn(self) -> Optional[str]:
        """
        The ARN of the version.
        """
        return pulumi.get(self, "function_arn")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        The version number.
        """
        return pulumi.get(self, "version")


class AwaitableGetVersionResult(GetVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVersionResult(
            function_arn=self.function_arn,
            version=self.version)


def get_version(function_arn: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVersionResult:
    """
    Resource Type definition for AWS::Lambda::Version


    :param str function_arn: The ARN of the version.
    """
    __args__ = dict()
    __args__['functionArn'] = function_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lambda:getVersion', __args__, opts=opts, typ=GetVersionResult).value

    return AwaitableGetVersionResult(
        function_arn=pulumi.get(__ret__, 'function_arn'),
        version=pulumi.get(__ret__, 'version'))
def get_version_output(function_arn: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVersionResult]:
    """
    Resource Type definition for AWS::Lambda::Version


    :param str function_arn: The ARN of the version.
    """
    __args__ = dict()
    __args__['functionArn'] = function_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:lambda:getVersion', __args__, opts=opts, typ=GetVersionResult)
    return __ret__.apply(lambda __response__: GetVersionResult(
        function_arn=pulumi.get(__response__, 'function_arn'),
        version=pulumi.get(__response__, 'version')))
