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

__all__ = [
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
    'get_application_output',
]

@pulumi.output_type
class GetApplicationResult:
    def __init__(__self__, app_block_arn=None, arn=None, created_time=None, description=None, display_name=None, icon_s3_location=None, launch_parameters=None, launch_path=None, working_directory=None):
        if app_block_arn and not isinstance(app_block_arn, str):
            raise TypeError("Expected argument 'app_block_arn' to be a str")
        pulumi.set(__self__, "app_block_arn", app_block_arn)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if icon_s3_location and not isinstance(icon_s3_location, dict):
            raise TypeError("Expected argument 'icon_s3_location' to be a dict")
        pulumi.set(__self__, "icon_s3_location", icon_s3_location)
        if launch_parameters and not isinstance(launch_parameters, str):
            raise TypeError("Expected argument 'launch_parameters' to be a str")
        pulumi.set(__self__, "launch_parameters", launch_parameters)
        if launch_path and not isinstance(launch_path, str):
            raise TypeError("Expected argument 'launch_path' to be a str")
        pulumi.set(__self__, "launch_path", launch_path)
        if working_directory and not isinstance(working_directory, str):
            raise TypeError("Expected argument 'working_directory' to be a str")
        pulumi.set(__self__, "working_directory", working_directory)

    @property
    @pulumi.getter(name="appBlockArn")
    def app_block_arn(self) -> Optional[str]:
        """
        The app block ARN with which the application should be associated.
        """
        return pulumi.get(self, "app_block_arn")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the application.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[str]:
        """
        The time when the application was created.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the application.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the application. This name is visible to users in the application catalog.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="iconS3Location")
    def icon_s3_location(self) -> Optional['outputs.ApplicationS3Location']:
        """
        The icon S3 location of the application.
        """
        return pulumi.get(self, "icon_s3_location")

    @property
    @pulumi.getter(name="launchParameters")
    def launch_parameters(self) -> Optional[str]:
        """
        The launch parameters of the application.
        """
        return pulumi.get(self, "launch_parameters")

    @property
    @pulumi.getter(name="launchPath")
    def launch_path(self) -> Optional[str]:
        """
        The launch path of the application.
        """
        return pulumi.get(self, "launch_path")

    @property
    @pulumi.getter(name="workingDirectory")
    def working_directory(self) -> Optional[str]:
        """
        The working directory of the application.
        """
        return pulumi.get(self, "working_directory")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            app_block_arn=self.app_block_arn,
            arn=self.arn,
            created_time=self.created_time,
            description=self.description,
            display_name=self.display_name,
            icon_s3_location=self.icon_s3_location,
            launch_parameters=self.launch_parameters,
            launch_path=self.launch_path,
            working_directory=self.working_directory)


def get_application(arn: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Resource Type definition for AWS::AppStream::Application


    :param str arn: The ARN of the application.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appstream:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        app_block_arn=pulumi.get(__ret__, 'app_block_arn'),
        arn=pulumi.get(__ret__, 'arn'),
        created_time=pulumi.get(__ret__, 'created_time'),
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        icon_s3_location=pulumi.get(__ret__, 'icon_s3_location'),
        launch_parameters=pulumi.get(__ret__, 'launch_parameters'),
        launch_path=pulumi.get(__ret__, 'launch_path'),
        working_directory=pulumi.get(__ret__, 'working_directory'))
def get_application_output(arn: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplicationResult]:
    """
    Resource Type definition for AWS::AppStream::Application


    :param str arn: The ARN of the application.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:appstream:getApplication', __args__, opts=opts, typ=GetApplicationResult)
    return __ret__.apply(lambda __response__: GetApplicationResult(
        app_block_arn=pulumi.get(__response__, 'app_block_arn'),
        arn=pulumi.get(__response__, 'arn'),
        created_time=pulumi.get(__response__, 'created_time'),
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        icon_s3_location=pulumi.get(__response__, 'icon_s3_location'),
        launch_parameters=pulumi.get(__response__, 'launch_parameters'),
        launch_path=pulumi.get(__response__, 'launch_path'),
        working_directory=pulumi.get(__response__, 'working_directory')))
