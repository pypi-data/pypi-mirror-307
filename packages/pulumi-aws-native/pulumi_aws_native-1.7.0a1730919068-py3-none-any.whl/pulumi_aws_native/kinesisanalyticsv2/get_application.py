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
from .. import outputs as _root_outputs
from ._enums import *

__all__ = [
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    def __init__(__self__, application_configuration=None, application_description=None, application_maintenance_configuration=None, runtime_environment=None, service_execution_role=None, tags=None):
        if application_configuration and not isinstance(application_configuration, dict):
            raise TypeError("Expected argument 'application_configuration' to be a dict")
        pulumi.set(__self__, "application_configuration", application_configuration)
        if application_description and not isinstance(application_description, str):
            raise TypeError("Expected argument 'application_description' to be a str")
        pulumi.set(__self__, "application_description", application_description)
        if application_maintenance_configuration and not isinstance(application_maintenance_configuration, dict):
            raise TypeError("Expected argument 'application_maintenance_configuration' to be a dict")
        pulumi.set(__self__, "application_maintenance_configuration", application_maintenance_configuration)
        if runtime_environment and not isinstance(runtime_environment, str):
            raise TypeError("Expected argument 'runtime_environment' to be a str")
        pulumi.set(__self__, "runtime_environment", runtime_environment)
        if service_execution_role and not isinstance(service_execution_role, str):
            raise TypeError("Expected argument 'service_execution_role' to be a str")
        pulumi.set(__self__, "service_execution_role", service_execution_role)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="applicationConfiguration")
    def application_configuration(self) -> Optional['outputs.ApplicationConfiguration']:
        """
        Use this parameter to configure the application.
        """
        return pulumi.get(self, "application_configuration")

    @property
    @pulumi.getter(name="applicationDescription")
    def application_description(self) -> Optional[str]:
        """
        The description of the application.
        """
        return pulumi.get(self, "application_description")

    @property
    @pulumi.getter(name="applicationMaintenanceConfiguration")
    def application_maintenance_configuration(self) -> Optional['outputs.ApplicationMaintenanceConfiguration']:
        """
        Used to configure start of maintenance window.
        """
        return pulumi.get(self, "application_maintenance_configuration")

    @property
    @pulumi.getter(name="runtimeEnvironment")
    def runtime_environment(self) -> Optional[str]:
        """
        The runtime environment for the application.
        """
        return pulumi.get(self, "runtime_environment")

    @property
    @pulumi.getter(name="serviceExecutionRole")
    def service_execution_role(self) -> Optional[str]:
        """
        Specifies the IAM role that the application uses to access external resources.
        """
        return pulumi.get(self, "service_execution_role")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of one or more tags to assign to the application. A tag is a key-value pair that identifies an application. Note that the maximum number of application tags includes system tags. The maximum number of user-defined application tags is 50.
        """
        return pulumi.get(self, "tags")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            application_configuration=self.application_configuration,
            application_description=self.application_description,
            application_maintenance_configuration=self.application_maintenance_configuration,
            runtime_environment=self.runtime_environment,
            service_execution_role=self.service_execution_role,
            tags=self.tags)


def get_application(application_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Creates an Amazon Kinesis Data Analytics application. For information about creating a Kinesis Data Analytics application, see [Creating an Application](https://docs.aws.amazon.com/kinesisanalytics/latest/java/getting-started.html).


    :param str application_name: The name of the application.
    """
    __args__ = dict()
    __args__['applicationName'] = application_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kinesisanalyticsv2:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        application_configuration=pulumi.get(__ret__, 'application_configuration'),
        application_description=pulumi.get(__ret__, 'application_description'),
        application_maintenance_configuration=pulumi.get(__ret__, 'application_maintenance_configuration'),
        runtime_environment=pulumi.get(__ret__, 'runtime_environment'),
        service_execution_role=pulumi.get(__ret__, 'service_execution_role'),
        tags=pulumi.get(__ret__, 'tags'))
def get_application_output(application_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Creates an Amazon Kinesis Data Analytics application. For information about creating a Kinesis Data Analytics application, see [Creating an Application](https://docs.aws.amazon.com/kinesisanalytics/latest/java/getting-started.html).


    :param str application_name: The name of the application.
    """
    __args__ = dict()
    __args__['applicationName'] = application_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:kinesisanalyticsv2:getApplication', __args__, opts=opts, typ=GetApplicationResult)
    return __ret__.apply(lambda __response__: GetApplicationResult(
        application_configuration=pulumi.get(__response__, 'application_configuration'),
        application_description=pulumi.get(__response__, 'application_description'),
        application_maintenance_configuration=pulumi.get(__response__, 'application_maintenance_configuration'),
        runtime_environment=pulumi.get(__response__, 'runtime_environment'),
        service_execution_role=pulumi.get(__response__, 'service_execution_role'),
        tags=pulumi.get(__response__, 'tags')))
