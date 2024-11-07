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
from .. import outputs as _root_outputs

__all__ = [
    'GetStudioResult',
    'AwaitableGetStudioResult',
    'get_studio',
    'get_studio_output',
]

@pulumi.output_type
class GetStudioResult:
    def __init__(__self__, arn=None, default_s3_location=None, description=None, idp_auth_url=None, idp_relay_state_parameter_name=None, name=None, studio_id=None, subnet_ids=None, tags=None, url=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if default_s3_location and not isinstance(default_s3_location, str):
            raise TypeError("Expected argument 'default_s3_location' to be a str")
        pulumi.set(__self__, "default_s3_location", default_s3_location)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if idp_auth_url and not isinstance(idp_auth_url, str):
            raise TypeError("Expected argument 'idp_auth_url' to be a str")
        pulumi.set(__self__, "idp_auth_url", idp_auth_url)
        if idp_relay_state_parameter_name and not isinstance(idp_relay_state_parameter_name, str):
            raise TypeError("Expected argument 'idp_relay_state_parameter_name' to be a str")
        pulumi.set(__self__, "idp_relay_state_parameter_name", idp_relay_state_parameter_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if studio_id and not isinstance(studio_id, str):
            raise TypeError("Expected argument 'studio_id' to be a str")
        pulumi.set(__self__, "studio_id", studio_id)
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the EMR Studio.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultS3Location")
    def default_s3_location(self) -> Optional[str]:
        """
        The default Amazon S3 location to back up EMR Studio Workspaces and notebook files. A Studio user can select an alternative Amazon S3 location when creating a Workspace.
        """
        return pulumi.get(self, "default_s3_location")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A detailed description of the Studio.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="idpAuthUrl")
    def idp_auth_url(self) -> Optional[str]:
        """
        Your identity provider's authentication endpoint. Amazon EMR Studio redirects federated users to this endpoint for authentication when logging in to a Studio with the Studio URL.
        """
        return pulumi.get(self, "idp_auth_url")

    @property
    @pulumi.getter(name="idpRelayStateParameterName")
    def idp_relay_state_parameter_name(self) -> Optional[str]:
        """
        The name of relay state parameter for external Identity Provider.
        """
        return pulumi.get(self, "idp_relay_state_parameter_name")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A descriptive name for the Amazon EMR Studio.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="studioId")
    def studio_id(self) -> Optional[str]:
        """
        The ID of the EMR Studio.
        """
        return pulumi.get(self, "studio_id")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[Sequence[str]]:
        """
        A list of up to 5 subnet IDs to associate with the Studio. The subnets must belong to the VPC specified by VpcId. Studio users can create a Workspace in any of the specified subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of tags to associate with the Studio. Tags are user-defined key-value pairs that consist of a required key string with a maximum of 128 characters, and an optional value string with a maximum of 256 characters.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        """
        The unique Studio access URL.
        """
        return pulumi.get(self, "url")


class AwaitableGetStudioResult(GetStudioResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStudioResult(
            arn=self.arn,
            default_s3_location=self.default_s3_location,
            description=self.description,
            idp_auth_url=self.idp_auth_url,
            idp_relay_state_parameter_name=self.idp_relay_state_parameter_name,
            name=self.name,
            studio_id=self.studio_id,
            subnet_ids=self.subnet_ids,
            tags=self.tags,
            url=self.url)


def get_studio(studio_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStudioResult:
    """
    Resource schema for AWS::EMR::Studio


    :param str studio_id: The ID of the EMR Studio.
    """
    __args__ = dict()
    __args__['studioId'] = studio_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:emr:getStudio', __args__, opts=opts, typ=GetStudioResult).value

    return AwaitableGetStudioResult(
        arn=pulumi.get(__ret__, 'arn'),
        default_s3_location=pulumi.get(__ret__, 'default_s3_location'),
        description=pulumi.get(__ret__, 'description'),
        idp_auth_url=pulumi.get(__ret__, 'idp_auth_url'),
        idp_relay_state_parameter_name=pulumi.get(__ret__, 'idp_relay_state_parameter_name'),
        name=pulumi.get(__ret__, 'name'),
        studio_id=pulumi.get(__ret__, 'studio_id'),
        subnet_ids=pulumi.get(__ret__, 'subnet_ids'),
        tags=pulumi.get(__ret__, 'tags'),
        url=pulumi.get(__ret__, 'url'))
def get_studio_output(studio_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStudioResult]:
    """
    Resource schema for AWS::EMR::Studio


    :param str studio_id: The ID of the EMR Studio.
    """
    __args__ = dict()
    __args__['studioId'] = studio_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:emr:getStudio', __args__, opts=opts, typ=GetStudioResult)
    return __ret__.apply(lambda __response__: GetStudioResult(
        arn=pulumi.get(__response__, 'arn'),
        default_s3_location=pulumi.get(__response__, 'default_s3_location'),
        description=pulumi.get(__response__, 'description'),
        idp_auth_url=pulumi.get(__response__, 'idp_auth_url'),
        idp_relay_state_parameter_name=pulumi.get(__response__, 'idp_relay_state_parameter_name'),
        name=pulumi.get(__response__, 'name'),
        studio_id=pulumi.get(__response__, 'studio_id'),
        subnet_ids=pulumi.get(__response__, 'subnet_ids'),
        tags=pulumi.get(__response__, 'tags'),
        url=pulumi.get(__response__, 'url')))
