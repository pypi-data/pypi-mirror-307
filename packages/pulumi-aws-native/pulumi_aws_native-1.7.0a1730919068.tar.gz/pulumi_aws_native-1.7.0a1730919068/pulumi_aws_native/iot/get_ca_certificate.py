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
    'GetCaCertificateResult',
    'AwaitableGetCaCertificateResult',
    'get_ca_certificate',
    'get_ca_certificate_output',
]

@pulumi.output_type
class GetCaCertificateResult:
    def __init__(__self__, arn=None, auto_registration_status=None, id=None, registration_config=None, status=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auto_registration_status and not isinstance(auto_registration_status, str):
            raise TypeError("Expected argument 'auto_registration_status' to be a str")
        pulumi.set(__self__, "auto_registration_status", auto_registration_status)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if registration_config and not isinstance(registration_config, dict):
            raise TypeError("Expected argument 'registration_config' to be a dict")
        pulumi.set(__self__, "registration_config", registration_config)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Returns the Amazon Resource Name (ARN) for the CA certificate. For example:

        `{ "Fn::GetAtt": ["MyCACertificate", "Arn"] }`

        A value similar to the following is returned:

        `arn:aws:iot:us-east-1:123456789012:cacert/a6be6b84559801927e35a8f901fae08b5971d78d1562e29504ff9663b276a5f5`
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoRegistrationStatus")
    def auto_registration_status(self) -> Optional['CaCertificateAutoRegistrationStatus']:
        """
        Whether the CA certificate is configured for auto registration of device certificates. Valid values are "ENABLE" and "DISABLE".
        """
        return pulumi.get(self, "auto_registration_status")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The CA certificate ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="registrationConfig")
    def registration_config(self) -> Optional['outputs.CaCertificateRegistrationConfig']:
        """
        Information about the registration configuration.
        """
        return pulumi.get(self, "registration_config")

    @property
    @pulumi.getter
    def status(self) -> Optional['CaCertificateStatus']:
        """
        The status of the CA certificate.

        Valid values are "ACTIVE" and "INACTIVE".
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetCaCertificateResult(GetCaCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCaCertificateResult(
            arn=self.arn,
            auto_registration_status=self.auto_registration_status,
            id=self.id,
            registration_config=self.registration_config,
            status=self.status,
            tags=self.tags)


def get_ca_certificate(id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCaCertificateResult:
    """
    Registers a CA Certificate in IoT.


    :param str id: The CA certificate ID.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iot:getCaCertificate', __args__, opts=opts, typ=GetCaCertificateResult).value

    return AwaitableGetCaCertificateResult(
        arn=pulumi.get(__ret__, 'arn'),
        auto_registration_status=pulumi.get(__ret__, 'auto_registration_status'),
        id=pulumi.get(__ret__, 'id'),
        registration_config=pulumi.get(__ret__, 'registration_config'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))
def get_ca_certificate_output(id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCaCertificateResult]:
    """
    Registers a CA Certificate in IoT.


    :param str id: The CA certificate ID.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iot:getCaCertificate', __args__, opts=opts, typ=GetCaCertificateResult)
    return __ret__.apply(lambda __response__: GetCaCertificateResult(
        arn=pulumi.get(__response__, 'arn'),
        auto_registration_status=pulumi.get(__response__, 'auto_registration_status'),
        id=pulumi.get(__response__, 'id'),
        registration_config=pulumi.get(__response__, 'registration_config'),
        status=pulumi.get(__response__, 'status'),
        tags=pulumi.get(__response__, 'tags')))
