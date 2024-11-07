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
from ._enums import *

__all__ = [
    'ConnectionAliasAssociation',
    'WorkspacesPoolApplicationSettings',
    'WorkspacesPoolCapacity',
    'WorkspacesPoolTimeoutSettings',
]

@pulumi.output_type
class ConnectionAliasAssociation(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "associatedAccountId":
            suggest = "associated_account_id"
        elif key == "associationStatus":
            suggest = "association_status"
        elif key == "connectionIdentifier":
            suggest = "connection_identifier"
        elif key == "resourceId":
            suggest = "resource_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConnectionAliasAssociation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConnectionAliasAssociation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConnectionAliasAssociation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 associated_account_id: Optional[str] = None,
                 association_status: Optional['ConnectionAliasAssociationAssociationStatus'] = None,
                 connection_identifier: Optional[str] = None,
                 resource_id: Optional[str] = None):
        """
        :param str associated_account_id: The identifier of the AWS account that associated the connection alias with a directory.
        :param 'ConnectionAliasAssociationAssociationStatus' association_status: The association status of the connection alias.
        :param str connection_identifier: The identifier of the connection alias association. You use the connection identifier in the DNS TXT record when you're configuring your DNS routing policies.
        :param str resource_id: The identifier of the directory associated with a connection alias.
        """
        if associated_account_id is not None:
            pulumi.set(__self__, "associated_account_id", associated_account_id)
        if association_status is not None:
            pulumi.set(__self__, "association_status", association_status)
        if connection_identifier is not None:
            pulumi.set(__self__, "connection_identifier", connection_identifier)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="associatedAccountId")
    def associated_account_id(self) -> Optional[str]:
        """
        The identifier of the AWS account that associated the connection alias with a directory.
        """
        return pulumi.get(self, "associated_account_id")

    @property
    @pulumi.getter(name="associationStatus")
    def association_status(self) -> Optional['ConnectionAliasAssociationAssociationStatus']:
        """
        The association status of the connection alias.
        """
        return pulumi.get(self, "association_status")

    @property
    @pulumi.getter(name="connectionIdentifier")
    def connection_identifier(self) -> Optional[str]:
        """
        The identifier of the connection alias association. You use the connection identifier in the DNS TXT record when you're configuring your DNS routing policies.
        """
        return pulumi.get(self, "connection_identifier")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The identifier of the directory associated with a connection alias.
        """
        return pulumi.get(self, "resource_id")


@pulumi.output_type
class WorkspacesPoolApplicationSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "settingsGroup":
            suggest = "settings_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspacesPoolApplicationSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspacesPoolApplicationSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspacesPoolApplicationSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 status: 'WorkspacesPoolApplicationSettingsStatus',
                 settings_group: Optional[str] = None):
        """
        :param 'WorkspacesPoolApplicationSettingsStatus' status: Enables or disables persistent application settings for users during their pool sessions.
        :param str settings_group: The path prefix for the S3 bucket where users’ persistent application settings are stored.
        """
        pulumi.set(__self__, "status", status)
        if settings_group is not None:
            pulumi.set(__self__, "settings_group", settings_group)

    @property
    @pulumi.getter
    def status(self) -> 'WorkspacesPoolApplicationSettingsStatus':
        """
        Enables or disables persistent application settings for users during their pool sessions.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="settingsGroup")
    def settings_group(self) -> Optional[str]:
        """
        The path prefix for the S3 bucket where users’ persistent application settings are stored.
        """
        return pulumi.get(self, "settings_group")


@pulumi.output_type
class WorkspacesPoolCapacity(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "desiredUserSessions":
            suggest = "desired_user_sessions"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspacesPoolCapacity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspacesPoolCapacity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspacesPoolCapacity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 desired_user_sessions: int):
        """
        :param int desired_user_sessions: The desired number of user sessions for the WorkSpaces in the pool.
        """
        pulumi.set(__self__, "desired_user_sessions", desired_user_sessions)

    @property
    @pulumi.getter(name="desiredUserSessions")
    def desired_user_sessions(self) -> int:
        """
        The desired number of user sessions for the WorkSpaces in the pool.
        """
        return pulumi.get(self, "desired_user_sessions")


@pulumi.output_type
class WorkspacesPoolTimeoutSettings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "disconnectTimeoutInSeconds":
            suggest = "disconnect_timeout_in_seconds"
        elif key == "idleDisconnectTimeoutInSeconds":
            suggest = "idle_disconnect_timeout_in_seconds"
        elif key == "maxUserDurationInSeconds":
            suggest = "max_user_duration_in_seconds"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspacesPoolTimeoutSettings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspacesPoolTimeoutSettings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspacesPoolTimeoutSettings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 disconnect_timeout_in_seconds: Optional[int] = None,
                 idle_disconnect_timeout_in_seconds: Optional[int] = None,
                 max_user_duration_in_seconds: Optional[int] = None):
        """
        :param int disconnect_timeout_in_seconds: Specifies the amount of time, in seconds, that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within the time set, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.
        :param int idle_disconnect_timeout_in_seconds: The amount of time in seconds a connection will stay active while idle.
        :param int max_user_duration_in_seconds: Specifies the maximum amount of time, in seconds, that a streaming session can remain active. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.
        """
        if disconnect_timeout_in_seconds is not None:
            pulumi.set(__self__, "disconnect_timeout_in_seconds", disconnect_timeout_in_seconds)
        if idle_disconnect_timeout_in_seconds is not None:
            pulumi.set(__self__, "idle_disconnect_timeout_in_seconds", idle_disconnect_timeout_in_seconds)
        if max_user_duration_in_seconds is not None:
            pulumi.set(__self__, "max_user_duration_in_seconds", max_user_duration_in_seconds)

    @property
    @pulumi.getter(name="disconnectTimeoutInSeconds")
    def disconnect_timeout_in_seconds(self) -> Optional[int]:
        """
        Specifies the amount of time, in seconds, that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within the time set, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.
        """
        return pulumi.get(self, "disconnect_timeout_in_seconds")

    @property
    @pulumi.getter(name="idleDisconnectTimeoutInSeconds")
    def idle_disconnect_timeout_in_seconds(self) -> Optional[int]:
        """
        The amount of time in seconds a connection will stay active while idle.
        """
        return pulumi.get(self, "idle_disconnect_timeout_in_seconds")

    @property
    @pulumi.getter(name="maxUserDurationInSeconds")
    def max_user_duration_in_seconds(self) -> Optional[int]:
        """
        Specifies the maximum amount of time, in seconds, that a streaming session can remain active. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.
        """
        return pulumi.get(self, "max_user_duration_in_seconds")


