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
from ._enums import *

__all__ = [
    'GetWorkspacesPoolResult',
    'AwaitableGetWorkspacesPoolResult',
    'get_workspaces_pool',
    'get_workspaces_pool_output',
]

@pulumi.output_type
class GetWorkspacesPoolResult:
    def __init__(__self__, application_settings=None, bundle_id=None, capacity=None, created_at=None, description=None, directory_id=None, pool_arn=None, pool_id=None, timeout_settings=None):
        if application_settings and not isinstance(application_settings, dict):
            raise TypeError("Expected argument 'application_settings' to be a dict")
        pulumi.set(__self__, "application_settings", application_settings)
        if bundle_id and not isinstance(bundle_id, str):
            raise TypeError("Expected argument 'bundle_id' to be a str")
        pulumi.set(__self__, "bundle_id", bundle_id)
        if capacity and not isinstance(capacity, dict):
            raise TypeError("Expected argument 'capacity' to be a dict")
        pulumi.set(__self__, "capacity", capacity)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if directory_id and not isinstance(directory_id, str):
            raise TypeError("Expected argument 'directory_id' to be a str")
        pulumi.set(__self__, "directory_id", directory_id)
        if pool_arn and not isinstance(pool_arn, str):
            raise TypeError("Expected argument 'pool_arn' to be a str")
        pulumi.set(__self__, "pool_arn", pool_arn)
        if pool_id and not isinstance(pool_id, str):
            raise TypeError("Expected argument 'pool_id' to be a str")
        pulumi.set(__self__, "pool_id", pool_id)
        if timeout_settings and not isinstance(timeout_settings, dict):
            raise TypeError("Expected argument 'timeout_settings' to be a dict")
        pulumi.set(__self__, "timeout_settings", timeout_settings)

    @property
    @pulumi.getter(name="applicationSettings")
    def application_settings(self) -> Optional['outputs.WorkspacesPoolApplicationSettings']:
        """
        The persistent application settings for users of the pool.
        """
        return pulumi.get(self, "application_settings")

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> Optional[str]:
        """
        The identifier of the bundle used by the pool.
        """
        return pulumi.get(self, "bundle_id")

    @property
    @pulumi.getter
    def capacity(self) -> Optional['outputs.WorkspacesPoolCapacity']:
        """
        Describes the user capacity for the pool.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The time the pool was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the pool.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> Optional[str]:
        """
        The identifier of the directory used by the pool.
        """
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter(name="poolArn")
    def pool_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) for the pool.
        """
        return pulumi.get(self, "pool_arn")

    @property
    @pulumi.getter(name="poolId")
    def pool_id(self) -> Optional[str]:
        """
        The identifier of the pool.
        """
        return pulumi.get(self, "pool_id")

    @property
    @pulumi.getter(name="timeoutSettings")
    def timeout_settings(self) -> Optional['outputs.WorkspacesPoolTimeoutSettings']:
        """
        The amount of time that a pool session remains active after users disconnect. If they try to reconnect to the pool session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new pool instance.
        """
        return pulumi.get(self, "timeout_settings")


class AwaitableGetWorkspacesPoolResult(GetWorkspacesPoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspacesPoolResult(
            application_settings=self.application_settings,
            bundle_id=self.bundle_id,
            capacity=self.capacity,
            created_at=self.created_at,
            description=self.description,
            directory_id=self.directory_id,
            pool_arn=self.pool_arn,
            pool_id=self.pool_id,
            timeout_settings=self.timeout_settings)


def get_workspaces_pool(pool_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspacesPoolResult:
    """
    Resource Type definition for AWS::WorkSpaces::WorkspacesPool


    :param str pool_id: The identifier of the pool.
    """
    __args__ = dict()
    __args__['poolId'] = pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:workspaces:getWorkspacesPool', __args__, opts=opts, typ=GetWorkspacesPoolResult).value

    return AwaitableGetWorkspacesPoolResult(
        application_settings=pulumi.get(__ret__, 'application_settings'),
        bundle_id=pulumi.get(__ret__, 'bundle_id'),
        capacity=pulumi.get(__ret__, 'capacity'),
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        directory_id=pulumi.get(__ret__, 'directory_id'),
        pool_arn=pulumi.get(__ret__, 'pool_arn'),
        pool_id=pulumi.get(__ret__, 'pool_id'),
        timeout_settings=pulumi.get(__ret__, 'timeout_settings'))
def get_workspaces_pool_output(pool_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkspacesPoolResult]:
    """
    Resource Type definition for AWS::WorkSpaces::WorkspacesPool


    :param str pool_id: The identifier of the pool.
    """
    __args__ = dict()
    __args__['poolId'] = pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:workspaces:getWorkspacesPool', __args__, opts=opts, typ=GetWorkspacesPoolResult)
    return __ret__.apply(lambda __response__: GetWorkspacesPoolResult(
        application_settings=pulumi.get(__response__, 'application_settings'),
        bundle_id=pulumi.get(__response__, 'bundle_id'),
        capacity=pulumi.get(__response__, 'capacity'),
        created_at=pulumi.get(__response__, 'created_at'),
        description=pulumi.get(__response__, 'description'),
        directory_id=pulumi.get(__response__, 'directory_id'),
        pool_arn=pulumi.get(__response__, 'pool_arn'),
        pool_id=pulumi.get(__response__, 'pool_id'),
        timeout_settings=pulumi.get(__response__, 'timeout_settings')))
