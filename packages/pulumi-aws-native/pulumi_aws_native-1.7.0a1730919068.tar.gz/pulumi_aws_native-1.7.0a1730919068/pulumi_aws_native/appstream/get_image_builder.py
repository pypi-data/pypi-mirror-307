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

__all__ = [
    'GetImageBuilderResult',
    'AwaitableGetImageBuilderResult',
    'get_image_builder',
    'get_image_builder_output',
]

@pulumi.output_type
class GetImageBuilderResult:
    def __init__(__self__, access_endpoints=None, appstream_agent_version=None, description=None, display_name=None, domain_join_info=None, enable_default_internet_access=None, iam_role_arn=None, image_arn=None, image_name=None, instance_type=None, name=None, streaming_url=None, tags=None, vpc_config=None):
        if access_endpoints and not isinstance(access_endpoints, list):
            raise TypeError("Expected argument 'access_endpoints' to be a list")
        pulumi.set(__self__, "access_endpoints", access_endpoints)
        if appstream_agent_version and not isinstance(appstream_agent_version, str):
            raise TypeError("Expected argument 'appstream_agent_version' to be a str")
        pulumi.set(__self__, "appstream_agent_version", appstream_agent_version)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if domain_join_info and not isinstance(domain_join_info, dict):
            raise TypeError("Expected argument 'domain_join_info' to be a dict")
        pulumi.set(__self__, "domain_join_info", domain_join_info)
        if enable_default_internet_access and not isinstance(enable_default_internet_access, bool):
            raise TypeError("Expected argument 'enable_default_internet_access' to be a bool")
        pulumi.set(__self__, "enable_default_internet_access", enable_default_internet_access)
        if iam_role_arn and not isinstance(iam_role_arn, str):
            raise TypeError("Expected argument 'iam_role_arn' to be a str")
        pulumi.set(__self__, "iam_role_arn", iam_role_arn)
        if image_arn and not isinstance(image_arn, str):
            raise TypeError("Expected argument 'image_arn' to be a str")
        pulumi.set(__self__, "image_arn", image_arn)
        if image_name and not isinstance(image_name, str):
            raise TypeError("Expected argument 'image_name' to be a str")
        pulumi.set(__self__, "image_name", image_name)
        if instance_type and not isinstance(instance_type, str):
            raise TypeError("Expected argument 'instance_type' to be a str")
        pulumi.set(__self__, "instance_type", instance_type)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if streaming_url and not isinstance(streaming_url, str):
            raise TypeError("Expected argument 'streaming_url' to be a str")
        pulumi.set(__self__, "streaming_url", streaming_url)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_config and not isinstance(vpc_config, dict):
            raise TypeError("Expected argument 'vpc_config' to be a dict")
        pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter(name="accessEndpoints")
    def access_endpoints(self) -> Optional[Sequence['outputs.ImageBuilderAccessEndpoint']]:
        """
        The list of virtual private cloud (VPC) interface endpoint objects. Administrators can connect to the image builder only through the specified endpoints.
        """
        return pulumi.get(self, "access_endpoints")

    @property
    @pulumi.getter(name="appstreamAgentVersion")
    def appstream_agent_version(self) -> Optional[str]:
        """
        The version of the AppStream 2.0 agent to use for this image builder. To use the latest version of the AppStream 2.0 agent, specify [LATEST].
        """
        return pulumi.get(self, "appstream_agent_version")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description to display.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The image builder name to display.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="domainJoinInfo")
    def domain_join_info(self) -> Optional['outputs.ImageBuilderDomainJoinInfo']:
        """
        The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.
        """
        return pulumi.get(self, "domain_join_info")

    @property
    @pulumi.getter(name="enableDefaultInternetAccess")
    def enable_default_internet_access(self) -> Optional[bool]:
        """
        Enables or disables default internet access for the image builder.
        """
        return pulumi.get(self, "enable_default_internet_access")

    @property
    @pulumi.getter(name="iamRoleArn")
    def iam_role_arn(self) -> Optional[str]:
        """
        The ARN of the IAM role that is applied to the image builder. To assume a role, the image builder calls the AWS Security Token Service `AssumeRole` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see [Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances](https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html) in the *Amazon AppStream 2.0 Administration Guide* .
        """
        return pulumi.get(self, "iam_role_arn")

    @property
    @pulumi.getter(name="imageArn")
    def image_arn(self) -> Optional[str]:
        """
        The ARN of the public, private, or shared image to use.
        """
        return pulumi.get(self, "image_arn")

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> Optional[str]:
        """
        The name of the image used to create the image builder.
        """
        return pulumi.get(self, "image_name")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> Optional[str]:
        """
        The instance type to use when launching the image builder. The following instance types are available:

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics-desktop.2xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics-pro.4xlarge
        - stream.graphics-pro.8xlarge
        - stream.graphics-pro.16xlarge
        """
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A unique name for the image builder.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="streamingUrl")
    def streaming_url(self) -> Optional[str]:
        """
        The URL to start an image builder streaming session, returned as a string.
        """
        return pulumi.get(self, "streaming_url")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional['outputs.ImageBuilderVpcConfig']:
        """
        The VPC configuration for the image builder. You can specify only one subnet.
        """
        return pulumi.get(self, "vpc_config")


class AwaitableGetImageBuilderResult(GetImageBuilderResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetImageBuilderResult(
            access_endpoints=self.access_endpoints,
            appstream_agent_version=self.appstream_agent_version,
            description=self.description,
            display_name=self.display_name,
            domain_join_info=self.domain_join_info,
            enable_default_internet_access=self.enable_default_internet_access,
            iam_role_arn=self.iam_role_arn,
            image_arn=self.image_arn,
            image_name=self.image_name,
            instance_type=self.instance_type,
            name=self.name,
            streaming_url=self.streaming_url,
            tags=self.tags,
            vpc_config=self.vpc_config)


def get_image_builder(name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetImageBuilderResult:
    """
    Resource Type definition for AWS::AppStream::ImageBuilder


    :param str name: A unique name for the image builder.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:appstream:getImageBuilder', __args__, opts=opts, typ=GetImageBuilderResult).value

    return AwaitableGetImageBuilderResult(
        access_endpoints=pulumi.get(__ret__, 'access_endpoints'),
        appstream_agent_version=pulumi.get(__ret__, 'appstream_agent_version'),
        description=pulumi.get(__ret__, 'description'),
        display_name=pulumi.get(__ret__, 'display_name'),
        domain_join_info=pulumi.get(__ret__, 'domain_join_info'),
        enable_default_internet_access=pulumi.get(__ret__, 'enable_default_internet_access'),
        iam_role_arn=pulumi.get(__ret__, 'iam_role_arn'),
        image_arn=pulumi.get(__ret__, 'image_arn'),
        image_name=pulumi.get(__ret__, 'image_name'),
        instance_type=pulumi.get(__ret__, 'instance_type'),
        name=pulumi.get(__ret__, 'name'),
        streaming_url=pulumi.get(__ret__, 'streaming_url'),
        tags=pulumi.get(__ret__, 'tags'),
        vpc_config=pulumi.get(__ret__, 'vpc_config'))
def get_image_builder_output(name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetImageBuilderResult]:
    """
    Resource Type definition for AWS::AppStream::ImageBuilder


    :param str name: A unique name for the image builder.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:appstream:getImageBuilder', __args__, opts=opts, typ=GetImageBuilderResult)
    return __ret__.apply(lambda __response__: GetImageBuilderResult(
        access_endpoints=pulumi.get(__response__, 'access_endpoints'),
        appstream_agent_version=pulumi.get(__response__, 'appstream_agent_version'),
        description=pulumi.get(__response__, 'description'),
        display_name=pulumi.get(__response__, 'display_name'),
        domain_join_info=pulumi.get(__response__, 'domain_join_info'),
        enable_default_internet_access=pulumi.get(__response__, 'enable_default_internet_access'),
        iam_role_arn=pulumi.get(__response__, 'iam_role_arn'),
        image_arn=pulumi.get(__response__, 'image_arn'),
        image_name=pulumi.get(__response__, 'image_name'),
        instance_type=pulumi.get(__response__, 'instance_type'),
        name=pulumi.get(__response__, 'name'),
        streaming_url=pulumi.get(__response__, 'streaming_url'),
        tags=pulumi.get(__response__, 'tags'),
        vpc_config=pulumi.get(__response__, 'vpc_config')))
