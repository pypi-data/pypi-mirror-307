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
    'GetHookTypeConfigResult',
    'AwaitableGetHookTypeConfigResult',
    'get_hook_type_config',
    'get_hook_type_config_output',
]

@pulumi.output_type
class GetHookTypeConfigResult:
    def __init__(__self__, configuration=None, configuration_arn=None, type_arn=None, type_name=None):
        if configuration and not isinstance(configuration, str):
            raise TypeError("Expected argument 'configuration' to be a str")
        pulumi.set(__self__, "configuration", configuration)
        if configuration_arn and not isinstance(configuration_arn, str):
            raise TypeError("Expected argument 'configuration_arn' to be a str")
        pulumi.set(__self__, "configuration_arn", configuration_arn)
        if type_arn and not isinstance(type_arn, str):
            raise TypeError("Expected argument 'type_arn' to be a str")
        pulumi.set(__self__, "type_arn", type_arn)
        if type_name and not isinstance(type_name, str):
            raise TypeError("Expected argument 'type_name' to be a str")
        pulumi.set(__self__, "type_name", type_name)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[str]:
        """
        The configuration data for the extension, in this account and region.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter(name="configurationArn")
    def configuration_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the configuration data, in this account and region.
        """
        return pulumi.get(self, "configuration_arn")

    @property
    @pulumi.getter(name="typeArn")
    def type_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the type without version number.
        """
        return pulumi.get(self, "type_arn")

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> Optional[str]:
        """
        The name of the type being registered.

        We recommend that type names adhere to the following pattern: company_or_organization::service::type.
        """
        return pulumi.get(self, "type_name")


class AwaitableGetHookTypeConfigResult(GetHookTypeConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHookTypeConfigResult(
            configuration=self.configuration,
            configuration_arn=self.configuration_arn,
            type_arn=self.type_arn,
            type_name=self.type_name)


def get_hook_type_config(configuration_arn: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHookTypeConfigResult:
    """
    Specifies the configuration data for a registered hook in CloudFormation Registry.


    :param str configuration_arn: The Amazon Resource Name (ARN) for the configuration data, in this account and region.
    """
    __args__ = dict()
    __args__['configurationArn'] = configuration_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudformation:getHookTypeConfig', __args__, opts=opts, typ=GetHookTypeConfigResult).value

    return AwaitableGetHookTypeConfigResult(
        configuration=pulumi.get(__ret__, 'configuration'),
        configuration_arn=pulumi.get(__ret__, 'configuration_arn'),
        type_arn=pulumi.get(__ret__, 'type_arn'),
        type_name=pulumi.get(__ret__, 'type_name'))
def get_hook_type_config_output(configuration_arn: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHookTypeConfigResult]:
    """
    Specifies the configuration data for a registered hook in CloudFormation Registry.


    :param str configuration_arn: The Amazon Resource Name (ARN) for the configuration data, in this account and region.
    """
    __args__ = dict()
    __args__['configurationArn'] = configuration_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudformation:getHookTypeConfig', __args__, opts=opts, typ=GetHookTypeConfigResult)
    return __ret__.apply(lambda __response__: GetHookTypeConfigResult(
        configuration=pulumi.get(__response__, 'configuration'),
        configuration_arn=pulumi.get(__response__, 'configuration_arn'),
        type_arn=pulumi.get(__response__, 'type_arn'),
        type_name=pulumi.get(__response__, 'type_name')))
