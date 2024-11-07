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
    'GetSimulationApplicationVersionResult',
    'AwaitableGetSimulationApplicationVersionResult',
    'get_simulation_application_version',
    'get_simulation_application_version_output',
]

@pulumi.output_type
class GetSimulationApplicationVersionResult:
    def __init__(__self__, application_version=None, arn=None):
        if application_version and not isinstance(application_version, str):
            raise TypeError("Expected argument 'application_version' to be a str")
        pulumi.set(__self__, "application_version", application_version)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter(name="applicationVersion")
    def application_version(self) -> Optional[str]:
        """
        The simulation application version.
        """
        return pulumi.get(self, "application_version")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the simulation application version.
        """
        return pulumi.get(self, "arn")


class AwaitableGetSimulationApplicationVersionResult(GetSimulationApplicationVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSimulationApplicationVersionResult(
            application_version=self.application_version,
            arn=self.arn)


def get_simulation_application_version(arn: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSimulationApplicationVersionResult:
    """
    AWS::RoboMaker::SimulationApplicationVersion resource creates an AWS RoboMaker SimulationApplicationVersion. This helps you control which code your simulation uses.


    :param str arn: The Amazon Resource Name (ARN) of the simulation application version.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:robomaker:getSimulationApplicationVersion', __args__, opts=opts, typ=GetSimulationApplicationVersionResult).value

    return AwaitableGetSimulationApplicationVersionResult(
        application_version=pulumi.get(__ret__, 'application_version'),
        arn=pulumi.get(__ret__, 'arn'))
def get_simulation_application_version_output(arn: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSimulationApplicationVersionResult]:
    """
    AWS::RoboMaker::SimulationApplicationVersion resource creates an AWS RoboMaker SimulationApplicationVersion. This helps you control which code your simulation uses.


    :param str arn: The Amazon Resource Name (ARN) of the simulation application version.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:robomaker:getSimulationApplicationVersion', __args__, opts=opts, typ=GetSimulationApplicationVersionResult)
    return __ret__.apply(lambda __response__: GetSimulationApplicationVersionResult(
        application_version=pulumi.get(__response__, 'application_version'),
        arn=pulumi.get(__response__, 'arn')))
