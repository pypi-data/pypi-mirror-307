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
    'GetBranchResult',
    'AwaitableGetBranchResult',
    'get_branch',
    'get_branch_output',
]

@pulumi.output_type
class GetBranchResult:
    def __init__(__self__, arn=None, backend=None, build_spec=None, description=None, enable_auto_build=None, enable_performance_mode=None, enable_pull_request_preview=None, environment_variables=None, framework=None, pull_request_environment_name=None, stage=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if backend and not isinstance(backend, dict):
            raise TypeError("Expected argument 'backend' to be a dict")
        pulumi.set(__self__, "backend", backend)
        if build_spec and not isinstance(build_spec, str):
            raise TypeError("Expected argument 'build_spec' to be a str")
        pulumi.set(__self__, "build_spec", build_spec)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enable_auto_build and not isinstance(enable_auto_build, bool):
            raise TypeError("Expected argument 'enable_auto_build' to be a bool")
        pulumi.set(__self__, "enable_auto_build", enable_auto_build)
        if enable_performance_mode and not isinstance(enable_performance_mode, bool):
            raise TypeError("Expected argument 'enable_performance_mode' to be a bool")
        pulumi.set(__self__, "enable_performance_mode", enable_performance_mode)
        if enable_pull_request_preview and not isinstance(enable_pull_request_preview, bool):
            raise TypeError("Expected argument 'enable_pull_request_preview' to be a bool")
        pulumi.set(__self__, "enable_pull_request_preview", enable_pull_request_preview)
        if environment_variables and not isinstance(environment_variables, list):
            raise TypeError("Expected argument 'environment_variables' to be a list")
        pulumi.set(__self__, "environment_variables", environment_variables)
        if framework and not isinstance(framework, str):
            raise TypeError("Expected argument 'framework' to be a str")
        pulumi.set(__self__, "framework", framework)
        if pull_request_environment_name and not isinstance(pull_request_environment_name, str):
            raise TypeError("Expected argument 'pull_request_environment_name' to be a str")
        pulumi.set(__self__, "pull_request_environment_name", pull_request_environment_name)
        if stage and not isinstance(stage, str):
            raise TypeError("Expected argument 'stage' to be a str")
        pulumi.set(__self__, "stage", stage)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        ARN for a branch, part of an Amplify App.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def backend(self) -> Optional['outputs.BranchBackend']:
        """
        The backend for a `Branch` of an Amplify app. Use for a backend created from an AWS CloudFormation stack.

        This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[str]:
        """
        The build specification (build spec) for the branch.
        """
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description for the branch that is part of an Amplify app.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> Optional[bool]:
        """
        Enables auto building for the branch.
        """
        return pulumi.get(self, "enable_auto_build")

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> Optional[bool]:
        """
        Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        """
        return pulumi.get(self, "enable_performance_mode")

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> Optional[bool]:
        """
        Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the `PullRequestEnvironmentName` property.

        For more information, see [Web Previews](https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "enable_pull_request_preview")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.BranchEnvironmentVariable']]:
        """
        The environment variables for the branch.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter
    def framework(self) -> Optional[str]:
        """
        The framework for the branch.
        """
        return pulumi.get(self, "framework")

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> Optional[str]:
        """
        If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named `prod` , `test` , or `dev` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the `EnablePullRequestPreview` property to `true` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see [Feature Branch Deployments and Team Workflows](https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html) in the *AWS Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "pull_request_environment_name")

    @property
    @pulumi.getter
    def stage(self) -> Optional['BranchStage']:
        """
        Describes the current stage for the branch.
        """
        return pulumi.get(self, "stage")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tag for the branch.
        """
        return pulumi.get(self, "tags")


class AwaitableGetBranchResult(GetBranchResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBranchResult(
            arn=self.arn,
            backend=self.backend,
            build_spec=self.build_spec,
            description=self.description,
            enable_auto_build=self.enable_auto_build,
            enable_performance_mode=self.enable_performance_mode,
            enable_pull_request_preview=self.enable_pull_request_preview,
            environment_variables=self.environment_variables,
            framework=self.framework,
            pull_request_environment_name=self.pull_request_environment_name,
            stage=self.stage,
            tags=self.tags)


def get_branch(arn: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBranchResult:
    """
    The AWS::Amplify::Branch resource creates a new branch within an app.


    :param str arn: ARN for a branch, part of an Amplify App.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:amplify:getBranch', __args__, opts=opts, typ=GetBranchResult).value

    return AwaitableGetBranchResult(
        arn=pulumi.get(__ret__, 'arn'),
        backend=pulumi.get(__ret__, 'backend'),
        build_spec=pulumi.get(__ret__, 'build_spec'),
        description=pulumi.get(__ret__, 'description'),
        enable_auto_build=pulumi.get(__ret__, 'enable_auto_build'),
        enable_performance_mode=pulumi.get(__ret__, 'enable_performance_mode'),
        enable_pull_request_preview=pulumi.get(__ret__, 'enable_pull_request_preview'),
        environment_variables=pulumi.get(__ret__, 'environment_variables'),
        framework=pulumi.get(__ret__, 'framework'),
        pull_request_environment_name=pulumi.get(__ret__, 'pull_request_environment_name'),
        stage=pulumi.get(__ret__, 'stage'),
        tags=pulumi.get(__ret__, 'tags'))
def get_branch_output(arn: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBranchResult]:
    """
    The AWS::Amplify::Branch resource creates a new branch within an app.


    :param str arn: ARN for a branch, part of an Amplify App.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:amplify:getBranch', __args__, opts=opts, typ=GetBranchResult)
    return __ret__.apply(lambda __response__: GetBranchResult(
        arn=pulumi.get(__response__, 'arn'),
        backend=pulumi.get(__response__, 'backend'),
        build_spec=pulumi.get(__response__, 'build_spec'),
        description=pulumi.get(__response__, 'description'),
        enable_auto_build=pulumi.get(__response__, 'enable_auto_build'),
        enable_performance_mode=pulumi.get(__response__, 'enable_performance_mode'),
        enable_pull_request_preview=pulumi.get(__response__, 'enable_pull_request_preview'),
        environment_variables=pulumi.get(__response__, 'environment_variables'),
        framework=pulumi.get(__response__, 'framework'),
        pull_request_environment_name=pulumi.get(__response__, 'pull_request_environment_name'),
        stage=pulumi.get(__response__, 'stage'),
        tags=pulumi.get(__response__, 'tags')))
