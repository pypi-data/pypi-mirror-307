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
    'GetAppResult',
    'AwaitableGetAppResult',
    'get_app',
    'get_app_output',
]

@pulumi.output_type
class GetAppResult:
    def __init__(__self__, app_id=None, app_name=None, arn=None, build_spec=None, cache_config=None, custom_headers=None, custom_rules=None, default_domain=None, description=None, enable_branch_auto_deletion=None, environment_variables=None, iam_service_role=None, name=None, platform=None, repository=None, tags=None):
        if app_id and not isinstance(app_id, str):
            raise TypeError("Expected argument 'app_id' to be a str")
        pulumi.set(__self__, "app_id", app_id)
        if app_name and not isinstance(app_name, str):
            raise TypeError("Expected argument 'app_name' to be a str")
        pulumi.set(__self__, "app_name", app_name)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if build_spec and not isinstance(build_spec, str):
            raise TypeError("Expected argument 'build_spec' to be a str")
        pulumi.set(__self__, "build_spec", build_spec)
        if cache_config and not isinstance(cache_config, dict):
            raise TypeError("Expected argument 'cache_config' to be a dict")
        pulumi.set(__self__, "cache_config", cache_config)
        if custom_headers and not isinstance(custom_headers, str):
            raise TypeError("Expected argument 'custom_headers' to be a str")
        pulumi.set(__self__, "custom_headers", custom_headers)
        if custom_rules and not isinstance(custom_rules, list):
            raise TypeError("Expected argument 'custom_rules' to be a list")
        pulumi.set(__self__, "custom_rules", custom_rules)
        if default_domain and not isinstance(default_domain, str):
            raise TypeError("Expected argument 'default_domain' to be a str")
        pulumi.set(__self__, "default_domain", default_domain)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enable_branch_auto_deletion and not isinstance(enable_branch_auto_deletion, bool):
            raise TypeError("Expected argument 'enable_branch_auto_deletion' to be a bool")
        pulumi.set(__self__, "enable_branch_auto_deletion", enable_branch_auto_deletion)
        if environment_variables and not isinstance(environment_variables, list):
            raise TypeError("Expected argument 'environment_variables' to be a list")
        pulumi.set(__self__, "environment_variables", environment_variables)
        if iam_service_role and not isinstance(iam_service_role, str):
            raise TypeError("Expected argument 'iam_service_role' to be a str")
        pulumi.set(__self__, "iam_service_role", iam_service_role)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform and not isinstance(platform, str):
            raise TypeError("Expected argument 'platform' to be a str")
        pulumi.set(__self__, "platform", platform)
        if repository and not isinstance(repository, str):
            raise TypeError("Expected argument 'repository' to be a str")
        pulumi.set(__self__, "repository", repository)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[str]:
        """
        Unique Id for the Amplify App.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="appName")
    def app_name(self) -> Optional[str]:
        """
        Name for the Amplify App.
        """
        return pulumi.get(self, "app_name")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        ARN for the Amplify App.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[str]:
        """
        The build specification (build spec) for an Amplify app.
        """
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter(name="cacheConfig")
    def cache_config(self) -> Optional['outputs.AppCacheConfig']:
        """
        The cache configuration for the Amplify app. If you don't specify the cache configuration `type` , Amplify uses the default `AMPLIFY_MANAGED` setting.
        """
        return pulumi.get(self, "cache_config")

    @property
    @pulumi.getter(name="customHeaders")
    def custom_headers(self) -> Optional[str]:
        """
        The custom HTTP headers for an Amplify app.
        """
        return pulumi.get(self, "custom_headers")

    @property
    @pulumi.getter(name="customRules")
    def custom_rules(self) -> Optional[Sequence['outputs.AppCustomRule']]:
        """
        The custom rewrite and redirect rules for an Amplify app.
        """
        return pulumi.get(self, "custom_rules")

    @property
    @pulumi.getter(name="defaultDomain")
    def default_domain(self) -> Optional[str]:
        """
        Default domain for the Amplify App.
        """
        return pulumi.get(self, "default_domain")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the Amplify app.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableBranchAutoDeletion")
    def enable_branch_auto_deletion(self) -> Optional[bool]:
        """
        Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.
        """
        return pulumi.get(self, "enable_branch_auto_deletion")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.AppEnvironmentVariable']]:
        """
        The environment variables for the Amplify app.

        For a list of the environment variables that are accessible to Amplify by default, see [Amplify Environment variables](https://docs.aws.amazon.com/amplify/latest/userguide/amplify-console-environment-variables.html) in the *Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter(name="iamServiceRole")
    def iam_service_role(self) -> Optional[str]:
        """
        AWS Identity and Access Management ( IAM ) service role for the Amazon Resource Name (ARN) of the Amplify app.
        """
        return pulumi.get(self, "iam_service_role")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the Amplify app.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> Optional['AppPlatform']:
        """
        The platform for the Amplify app. For a static app, set the platform type to `WEB` . For a dynamic server-side rendered (SSR) app, set the platform type to `WEB_COMPUTE` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to `WEB_DYNAMIC` .

        If you are deploying an SSG only app with Next.js version 14 or later, you must set the platform type to `WEB_COMPUTE` and set the artifacts `baseDirectory` to `.next` in the application's build settings. For an example of the build specification settings, see [Amplify build settings for a Next.js 14 SSG application](https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-app.html#build-setting-detection-ssg-14) in the *Amplify Hosting User Guide* .
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter
    def repository(self) -> Optional[str]:
        """
        The Git repository for the Amplify app.
        """
        return pulumi.get(self, "repository")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tag for an Amplify app.
        """
        return pulumi.get(self, "tags")


class AwaitableGetAppResult(GetAppResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppResult(
            app_id=self.app_id,
            app_name=self.app_name,
            arn=self.arn,
            build_spec=self.build_spec,
            cache_config=self.cache_config,
            custom_headers=self.custom_headers,
            custom_rules=self.custom_rules,
            default_domain=self.default_domain,
            description=self.description,
            enable_branch_auto_deletion=self.enable_branch_auto_deletion,
            environment_variables=self.environment_variables,
            iam_service_role=self.iam_service_role,
            name=self.name,
            platform=self.platform,
            repository=self.repository,
            tags=self.tags)


def get_app(arn: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAppResult:
    """
    The AWS::Amplify::App resource creates Apps in the Amplify Console. An App is a collection of branches.


    :param str arn: ARN for the Amplify App.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:amplify:getApp', __args__, opts=opts, typ=GetAppResult).value

    return AwaitableGetAppResult(
        app_id=pulumi.get(__ret__, 'app_id'),
        app_name=pulumi.get(__ret__, 'app_name'),
        arn=pulumi.get(__ret__, 'arn'),
        build_spec=pulumi.get(__ret__, 'build_spec'),
        cache_config=pulumi.get(__ret__, 'cache_config'),
        custom_headers=pulumi.get(__ret__, 'custom_headers'),
        custom_rules=pulumi.get(__ret__, 'custom_rules'),
        default_domain=pulumi.get(__ret__, 'default_domain'),
        description=pulumi.get(__ret__, 'description'),
        enable_branch_auto_deletion=pulumi.get(__ret__, 'enable_branch_auto_deletion'),
        environment_variables=pulumi.get(__ret__, 'environment_variables'),
        iam_service_role=pulumi.get(__ret__, 'iam_service_role'),
        name=pulumi.get(__ret__, 'name'),
        platform=pulumi.get(__ret__, 'platform'),
        repository=pulumi.get(__ret__, 'repository'),
        tags=pulumi.get(__ret__, 'tags'))
def get_app_output(arn: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAppResult]:
    """
    The AWS::Amplify::App resource creates Apps in the Amplify Console. An App is a collection of branches.


    :param str arn: ARN for the Amplify App.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:amplify:getApp', __args__, opts=opts, typ=GetAppResult)
    return __ret__.apply(lambda __response__: GetAppResult(
        app_id=pulumi.get(__response__, 'app_id'),
        app_name=pulumi.get(__response__, 'app_name'),
        arn=pulumi.get(__response__, 'arn'),
        build_spec=pulumi.get(__response__, 'build_spec'),
        cache_config=pulumi.get(__response__, 'cache_config'),
        custom_headers=pulumi.get(__response__, 'custom_headers'),
        custom_rules=pulumi.get(__response__, 'custom_rules'),
        default_domain=pulumi.get(__response__, 'default_domain'),
        description=pulumi.get(__response__, 'description'),
        enable_branch_auto_deletion=pulumi.get(__response__, 'enable_branch_auto_deletion'),
        environment_variables=pulumi.get(__response__, 'environment_variables'),
        iam_service_role=pulumi.get(__response__, 'iam_service_role'),
        name=pulumi.get(__response__, 'name'),
        platform=pulumi.get(__response__, 'platform'),
        repository=pulumi.get(__response__, 'repository'),
        tags=pulumi.get(__response__, 'tags')))
