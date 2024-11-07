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
    'GroupPolicyArgs',
    'GroupPolicyArgsDict',
    'RolePolicyArgs',
    'RolePolicyArgsDict',
    'UserLoginProfileArgs',
    'UserLoginProfileArgsDict',
    'UserPolicyArgs',
    'UserPolicyArgsDict',
]

MYPY = False

if not MYPY:
    class GroupPolicyArgsDict(TypedDict):
        """
        Contains information about an attached policy.
         An attached policy is a managed policy that has been attached to a user, group, or role.
         For more information about managed policies, see [Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *User Guide*.
        """
        policy_document: Any
        """
        The policy document.
        """
        policy_name: pulumi.Input[str]
        """
        The friendly name (not ARN) identifying the policy.
        """
elif False:
    GroupPolicyArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class GroupPolicyArgs:
    def __init__(__self__, *,
                 policy_document: Any,
                 policy_name: pulumi.Input[str]):
        """
        Contains information about an attached policy.
         An attached policy is a managed policy that has been attached to a user, group, or role.
         For more information about managed policies, see [Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *User Guide*.
        :param Any policy_document: The policy document.
        :param pulumi.Input[str] policy_name: The friendly name (not ARN) identifying the policy.
        """
        pulumi.set(__self__, "policy_document", policy_document)
        pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Any:
        """
        The policy document.
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Any):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        The friendly name (not ARN) identifying the policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)


if not MYPY:
    class RolePolicyArgsDict(TypedDict):
        """
        Contains information about an attached policy.
         An attached policy is a managed policy that has been attached to a user, group, or role.
         For more information about managed policies, refer to [Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *User Guide*.
        """
        policy_document: Any
        """
        The entire contents of the policy that defines permissions. For more information, see [Overview of JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
        """
        policy_name: pulumi.Input[str]
        """
        The friendly name (not ARN) identifying the policy.
        """
elif False:
    RolePolicyArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class RolePolicyArgs:
    def __init__(__self__, *,
                 policy_document: Any,
                 policy_name: pulumi.Input[str]):
        """
        Contains information about an attached policy.
         An attached policy is a managed policy that has been attached to a user, group, or role.
         For more information about managed policies, refer to [Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *User Guide*.
        :param Any policy_document: The entire contents of the policy that defines permissions. For more information, see [Overview of JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
        :param pulumi.Input[str] policy_name: The friendly name (not ARN) identifying the policy.
        """
        pulumi.set(__self__, "policy_document", policy_document)
        pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Any:
        """
        The entire contents of the policy that defines permissions. For more information, see [Overview of JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Any):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        The friendly name (not ARN) identifying the policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)


if not MYPY:
    class UserLoginProfileArgsDict(TypedDict):
        """
        Creates a password for the specified user, giving the user the ability to access AWS services through the console. For more information about managing passwords, see [Managing Passwords](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html) in the *User Guide*.
        """
        password: pulumi.Input[str]
        """
        The user's password.
        """
        password_reset_required: NotRequired[pulumi.Input[bool]]
        """
        Specifies whether the user is required to set a new password on next sign-in.
        """
elif False:
    UserLoginProfileArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class UserLoginProfileArgs:
    def __init__(__self__, *,
                 password: pulumi.Input[str],
                 password_reset_required: Optional[pulumi.Input[bool]] = None):
        """
        Creates a password for the specified user, giving the user the ability to access AWS services through the console. For more information about managing passwords, see [Managing Passwords](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html) in the *User Guide*.
        :param pulumi.Input[str] password: The user's password.
        :param pulumi.Input[bool] password_reset_required: Specifies whether the user is required to set a new password on next sign-in.
        """
        pulumi.set(__self__, "password", password)
        if password_reset_required is not None:
            pulumi.set(__self__, "password_reset_required", password_reset_required)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        The user's password.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="passwordResetRequired")
    def password_reset_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the user is required to set a new password on next sign-in.
        """
        return pulumi.get(self, "password_reset_required")

    @password_reset_required.setter
    def password_reset_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "password_reset_required", value)


if not MYPY:
    class UserPolicyArgsDict(TypedDict):
        """
        Contains information about an attached policy.
         An attached policy is a managed policy that has been attached to a user, group, or role.
         For more information about managed policies, refer to [Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *User Guide*.
        """
        policy_document: Any
        """
        The entire contents of the policy that defines permissions. For more information, see [Overview of JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
        """
        policy_name: pulumi.Input[str]
        """
        The friendly name (not ARN) identifying the policy.
        """
elif False:
    UserPolicyArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class UserPolicyArgs:
    def __init__(__self__, *,
                 policy_document: Any,
                 policy_name: pulumi.Input[str]):
        """
        Contains information about an attached policy.
         An attached policy is a managed policy that has been attached to a user, group, or role.
         For more information about managed policies, refer to [Managed Policies and Inline Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *User Guide*.
        :param Any policy_document: The entire contents of the policy that defines permissions. For more information, see [Overview of JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
        :param pulumi.Input[str] policy_name: The friendly name (not ARN) identifying the policy.
        """
        pulumi.set(__self__, "policy_document", policy_document)
        pulumi.set(__self__, "policy_name", policy_name)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Any:
        """
        The entire contents of the policy that defines permissions. For more information, see [Overview of JSON policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
        """
        return pulumi.get(self, "policy_document")

    @policy_document.setter
    def policy_document(self, value: Any):
        pulumi.set(self, "policy_document", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        The friendly name (not ARN) identifying the policy.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)


