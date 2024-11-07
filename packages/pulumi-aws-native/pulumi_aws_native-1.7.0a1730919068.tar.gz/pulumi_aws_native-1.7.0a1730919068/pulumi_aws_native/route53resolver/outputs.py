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
    'FirewallRuleGroupFirewallRule',
    'ResolverRuleTargetAddress',
]

@pulumi.output_type
class FirewallRuleGroupFirewallRule(dict):
    """
    Firewall Rule associating the Rule Group to a Domain List
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "firewallDomainListId":
            suggest = "firewall_domain_list_id"
        elif key == "blockOverrideDnsType":
            suggest = "block_override_dns_type"
        elif key == "blockOverrideDomain":
            suggest = "block_override_domain"
        elif key == "blockOverrideTtl":
            suggest = "block_override_ttl"
        elif key == "blockResponse":
            suggest = "block_response"
        elif key == "firewallDomainRedirectionAction":
            suggest = "firewall_domain_redirection_action"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FirewallRuleGroupFirewallRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FirewallRuleGroupFirewallRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FirewallRuleGroupFirewallRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action: 'FirewallRuleGroupFirewallRuleAction',
                 firewall_domain_list_id: str,
                 priority: int,
                 block_override_dns_type: Optional['FirewallRuleGroupFirewallRuleBlockOverrideDnsType'] = None,
                 block_override_domain: Optional[str] = None,
                 block_override_ttl: Optional[int] = None,
                 block_response: Optional['FirewallRuleGroupFirewallRuleBlockResponse'] = None,
                 firewall_domain_redirection_action: Optional['FirewallRuleGroupFirewallRuleFirewallDomainRedirectionAction'] = None,
                 qtype: Optional[str] = None):
        """
        Firewall Rule associating the Rule Group to a Domain List
        :param 'FirewallRuleGroupFirewallRuleAction' action: Rule Action
        :param str firewall_domain_list_id: ResourceId
        :param int priority: Rule Priority
        :param 'FirewallRuleGroupFirewallRuleBlockOverrideDnsType' block_override_dns_type: BlockOverrideDnsType
        :param str block_override_domain: BlockOverrideDomain
        :param int block_override_ttl: BlockOverrideTtl
        :param 'FirewallRuleGroupFirewallRuleBlockResponse' block_response: BlockResponse
        :param 'FirewallRuleGroupFirewallRuleFirewallDomainRedirectionAction' firewall_domain_redirection_action: FirewallDomainRedirectionAction
        :param str qtype: Qtype
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "firewall_domain_list_id", firewall_domain_list_id)
        pulumi.set(__self__, "priority", priority)
        if block_override_dns_type is not None:
            pulumi.set(__self__, "block_override_dns_type", block_override_dns_type)
        if block_override_domain is not None:
            pulumi.set(__self__, "block_override_domain", block_override_domain)
        if block_override_ttl is not None:
            pulumi.set(__self__, "block_override_ttl", block_override_ttl)
        if block_response is not None:
            pulumi.set(__self__, "block_response", block_response)
        if firewall_domain_redirection_action is not None:
            pulumi.set(__self__, "firewall_domain_redirection_action", firewall_domain_redirection_action)
        if qtype is not None:
            pulumi.set(__self__, "qtype", qtype)

    @property
    @pulumi.getter
    def action(self) -> 'FirewallRuleGroupFirewallRuleAction':
        """
        Rule Action
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="firewallDomainListId")
    def firewall_domain_list_id(self) -> str:
        """
        ResourceId
        """
        return pulumi.get(self, "firewall_domain_list_id")

    @property
    @pulumi.getter
    def priority(self) -> int:
        """
        Rule Priority
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="blockOverrideDnsType")
    def block_override_dns_type(self) -> Optional['FirewallRuleGroupFirewallRuleBlockOverrideDnsType']:
        """
        BlockOverrideDnsType
        """
        return pulumi.get(self, "block_override_dns_type")

    @property
    @pulumi.getter(name="blockOverrideDomain")
    def block_override_domain(self) -> Optional[str]:
        """
        BlockOverrideDomain
        """
        return pulumi.get(self, "block_override_domain")

    @property
    @pulumi.getter(name="blockOverrideTtl")
    def block_override_ttl(self) -> Optional[int]:
        """
        BlockOverrideTtl
        """
        return pulumi.get(self, "block_override_ttl")

    @property
    @pulumi.getter(name="blockResponse")
    def block_response(self) -> Optional['FirewallRuleGroupFirewallRuleBlockResponse']:
        """
        BlockResponse
        """
        return pulumi.get(self, "block_response")

    @property
    @pulumi.getter(name="firewallDomainRedirectionAction")
    def firewall_domain_redirection_action(self) -> Optional['FirewallRuleGroupFirewallRuleFirewallDomainRedirectionAction']:
        """
        FirewallDomainRedirectionAction
        """
        return pulumi.get(self, "firewall_domain_redirection_action")

    @property
    @pulumi.getter
    def qtype(self) -> Optional[str]:
        """
        Qtype
        """
        return pulumi.get(self, "qtype")


@pulumi.output_type
class ResolverRuleTargetAddress(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "serverNameIndication":
            suggest = "server_name_indication"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResolverRuleTargetAddress. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResolverRuleTargetAddress.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResolverRuleTargetAddress.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ip: Optional[str] = None,
                 ipv6: Optional[str] = None,
                 port: Optional[str] = None,
                 protocol: Optional['ResolverRuleTargetAddressProtocol'] = None,
                 server_name_indication: Optional[str] = None):
        """
        :param str ip: One IP address that you want to forward DNS queries to. You can specify only IPv4 addresses. 
        :param str ipv6: One IPv6 address that you want to forward DNS queries to. You can specify only IPv6 addresses. 
        :param str port: The port at Ip that you want to forward DNS queries to. 
        :param 'ResolverRuleTargetAddressProtocol' protocol: The protocol that you want to use to forward DNS queries. 
        :param str server_name_indication: The SNI of the target name servers for DoH/DoH-FIPS outbound endpoints
        """
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if ipv6 is not None:
            pulumi.set(__self__, "ipv6", ipv6)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if server_name_indication is not None:
            pulumi.set(__self__, "server_name_indication", server_name_indication)

    @property
    @pulumi.getter
    def ip(self) -> Optional[str]:
        """
        One IP address that you want to forward DNS queries to. You can specify only IPv4 addresses. 
        """
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter
    def ipv6(self) -> Optional[str]:
        """
        One IPv6 address that you want to forward DNS queries to. You can specify only IPv6 addresses. 
        """
        return pulumi.get(self, "ipv6")

    @property
    @pulumi.getter
    def port(self) -> Optional[str]:
        """
        The port at Ip that you want to forward DNS queries to. 
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional['ResolverRuleTargetAddressProtocol']:
        """
        The protocol that you want to use to forward DNS queries. 
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="serverNameIndication")
    def server_name_indication(self) -> Optional[str]:
        """
        The SNI of the target name servers for DoH/DoH-FIPS outbound endpoints
        """
        return pulumi.get(self, "server_name_indication")


