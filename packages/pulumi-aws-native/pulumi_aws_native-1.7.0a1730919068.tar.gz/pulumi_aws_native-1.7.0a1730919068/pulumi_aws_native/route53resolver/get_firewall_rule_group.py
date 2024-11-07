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
    'GetFirewallRuleGroupResult',
    'AwaitableGetFirewallRuleGroupResult',
    'get_firewall_rule_group',
    'get_firewall_rule_group_output',
]

@pulumi.output_type
class GetFirewallRuleGroupResult:
    def __init__(__self__, arn=None, creation_time=None, creator_request_id=None, firewall_rules=None, id=None, modification_time=None, owner_id=None, rule_count=None, share_status=None, status=None, status_message=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if creator_request_id and not isinstance(creator_request_id, str):
            raise TypeError("Expected argument 'creator_request_id' to be a str")
        pulumi.set(__self__, "creator_request_id", creator_request_id)
        if firewall_rules and not isinstance(firewall_rules, list):
            raise TypeError("Expected argument 'firewall_rules' to be a list")
        pulumi.set(__self__, "firewall_rules", firewall_rules)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if modification_time and not isinstance(modification_time, str):
            raise TypeError("Expected argument 'modification_time' to be a str")
        pulumi.set(__self__, "modification_time", modification_time)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if rule_count and not isinstance(rule_count, int):
            raise TypeError("Expected argument 'rule_count' to be a int")
        pulumi.set(__self__, "rule_count", rule_count)
        if share_status and not isinstance(share_status, str):
            raise TypeError("Expected argument 'share_status' to be a str")
        pulumi.set(__self__, "share_status", share_status)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if status_message and not isinstance(status_message, str):
            raise TypeError("Expected argument 'status_message' to be a str")
        pulumi.set(__self__, "status_message", status_message)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Arn
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        Rfc3339TimeString
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="creatorRequestId")
    def creator_request_id(self) -> Optional[str]:
        """
        The id of the creator request.
        """
        return pulumi.get(self, "creator_request_id")

    @property
    @pulumi.getter(name="firewallRules")
    def firewall_rules(self) -> Optional[Sequence['outputs.FirewallRuleGroupFirewallRule']]:
        """
        FirewallRules
        """
        return pulumi.get(self, "firewall_rules")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        ResourceId
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="modificationTime")
    def modification_time(self) -> Optional[str]:
        """
        Rfc3339TimeString
        """
        return pulumi.get(self, "modification_time")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[str]:
        """
        AccountId
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="ruleCount")
    def rule_count(self) -> Optional[int]:
        """
        Count
        """
        return pulumi.get(self, "rule_count")

    @property
    @pulumi.getter(name="shareStatus")
    def share_status(self) -> Optional['FirewallRuleGroupShareStatus']:
        """
        ShareStatus, possible values are NOT_SHARED, SHARED_WITH_ME, SHARED_BY_ME.
        """
        return pulumi.get(self, "share_status")

    @property
    @pulumi.getter
    def status(self) -> Optional['FirewallRuleGroupStatus']:
        """
        ResolverFirewallRuleGroupAssociation, possible values are COMPLETE, DELETING, UPDATING, and INACTIVE_OWNER_ACCOUNT_CLOSED.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusMessage")
    def status_message(self) -> Optional[str]:
        """
        FirewallRuleGroupStatus
        """
        return pulumi.get(self, "status_message")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Tags
        """
        return pulumi.get(self, "tags")


class AwaitableGetFirewallRuleGroupResult(GetFirewallRuleGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirewallRuleGroupResult(
            arn=self.arn,
            creation_time=self.creation_time,
            creator_request_id=self.creator_request_id,
            firewall_rules=self.firewall_rules,
            id=self.id,
            modification_time=self.modification_time,
            owner_id=self.owner_id,
            rule_count=self.rule_count,
            share_status=self.share_status,
            status=self.status,
            status_message=self.status_message,
            tags=self.tags)


def get_firewall_rule_group(id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirewallRuleGroupResult:
    """
    Resource schema for AWS::Route53Resolver::FirewallRuleGroup.


    :param str id: ResourceId
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:route53resolver:getFirewallRuleGroup', __args__, opts=opts, typ=GetFirewallRuleGroupResult).value

    return AwaitableGetFirewallRuleGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        creation_time=pulumi.get(__ret__, 'creation_time'),
        creator_request_id=pulumi.get(__ret__, 'creator_request_id'),
        firewall_rules=pulumi.get(__ret__, 'firewall_rules'),
        id=pulumi.get(__ret__, 'id'),
        modification_time=pulumi.get(__ret__, 'modification_time'),
        owner_id=pulumi.get(__ret__, 'owner_id'),
        rule_count=pulumi.get(__ret__, 'rule_count'),
        share_status=pulumi.get(__ret__, 'share_status'),
        status=pulumi.get(__ret__, 'status'),
        status_message=pulumi.get(__ret__, 'status_message'),
        tags=pulumi.get(__ret__, 'tags'))
def get_firewall_rule_group_output(id: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirewallRuleGroupResult]:
    """
    Resource schema for AWS::Route53Resolver::FirewallRuleGroup.


    :param str id: ResourceId
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:route53resolver:getFirewallRuleGroup', __args__, opts=opts, typ=GetFirewallRuleGroupResult)
    return __ret__.apply(lambda __response__: GetFirewallRuleGroupResult(
        arn=pulumi.get(__response__, 'arn'),
        creation_time=pulumi.get(__response__, 'creation_time'),
        creator_request_id=pulumi.get(__response__, 'creator_request_id'),
        firewall_rules=pulumi.get(__response__, 'firewall_rules'),
        id=pulumi.get(__response__, 'id'),
        modification_time=pulumi.get(__response__, 'modification_time'),
        owner_id=pulumi.get(__response__, 'owner_id'),
        rule_count=pulumi.get(__response__, 'rule_count'),
        share_status=pulumi.get(__response__, 'share_status'),
        status=pulumi.get(__response__, 'status'),
        status_message=pulumi.get(__response__, 'status_message'),
        tags=pulumi.get(__response__, 'tags')))
