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
    'GetMemberResult',
    'AwaitableGetMemberResult',
    'get_member',
    'get_member_output',
]

@pulumi.output_type
class GetMemberResult:
    def __init__(__self__, email=None, status=None):
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def email(self) -> Optional[str]:
        """
        The email address associated with the member account.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        You can use the `Status` property to update the status of the relationship between the member account and its administrator account. Valid values are `Created` and `Invited` when using an `AWS::GuardDuty::Member` resource. If the value for this property is not provided or set to `Created` , a member account is created but not invited. If the value of this property is set to `Invited` , a member account is created and invited.
        """
        return pulumi.get(self, "status")


class AwaitableGetMemberResult(GetMemberResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMemberResult(
            email=self.email,
            status=self.status)


def get_member(detector_id: Optional[str] = None,
               member_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMemberResult:
    """
    Resource Type definition for AWS::GuardDuty::Member


    :param str detector_id: The ID of the detector associated with the GuardDuty service to add the member to.
    :param str member_id: The AWS account ID of the account to designate as a member.
    """
    __args__ = dict()
    __args__['detectorId'] = detector_id
    __args__['memberId'] = member_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:guardduty:getMember', __args__, opts=opts, typ=GetMemberResult).value

    return AwaitableGetMemberResult(
        email=pulumi.get(__ret__, 'email'),
        status=pulumi.get(__ret__, 'status'))
def get_member_output(detector_id: Optional[pulumi.Input[str]] = None,
                      member_id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMemberResult]:
    """
    Resource Type definition for AWS::GuardDuty::Member


    :param str detector_id: The ID of the detector associated with the GuardDuty service to add the member to.
    :param str member_id: The AWS account ID of the account to designate as a member.
    """
    __args__ = dict()
    __args__['detectorId'] = detector_id
    __args__['memberId'] = member_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:guardduty:getMember', __args__, opts=opts, typ=GetMemberResult)
    return __ret__.apply(lambda __response__: GetMemberResult(
        email=pulumi.get(__response__, 'email'),
        status=pulumi.get(__response__, 'status')))
