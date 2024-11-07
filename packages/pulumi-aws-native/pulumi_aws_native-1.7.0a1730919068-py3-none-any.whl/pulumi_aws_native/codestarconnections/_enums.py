# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'RepositoryLinkProviderType',
    'SyncConfigurationProviderType',
    'SyncConfigurationPublishDeploymentStatus',
    'SyncConfigurationTriggerResourceUpdateOn',
]


class RepositoryLinkProviderType(str, Enum):
    """
    The name of the external provider where your third-party code repository is configured.
    """
    GIT_HUB = "GitHub"
    BITBUCKET = "Bitbucket"
    GIT_HUB_ENTERPRISE = "GitHubEnterprise"
    GIT_LAB = "GitLab"
    GIT_LAB_SELF_MANAGED = "GitLabSelfManaged"


class SyncConfigurationProviderType(str, Enum):
    """
    The name of the external provider where your third-party code repository is configured.
    """
    GIT_HUB = "GitHub"
    BITBUCKET = "Bitbucket"
    GIT_HUB_ENTERPRISE = "GitHubEnterprise"
    GIT_LAB = "GitLab"
    GIT_LAB_SELF_MANAGED = "GitLabSelfManaged"


class SyncConfigurationPublishDeploymentStatus(str, Enum):
    """
    Whether to enable or disable publishing of deployment status to source providers.
    """
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class SyncConfigurationTriggerResourceUpdateOn(str, Enum):
    """
    When to trigger Git sync to begin the stack update.
    """
    ANY_CHANGE = "ANY_CHANGE"
    FILE_CHANGE = "FILE_CHANGE"
