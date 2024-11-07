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
    'GetLoggingConfigurationResult',
    'AwaitableGetLoggingConfigurationResult',
    'get_logging_configuration',
    'get_logging_configuration_output',
]

@pulumi.output_type
class GetLoggingConfigurationResult:
    def __init__(__self__, log_destination_configs=None, logging_filter=None, managed_by_firewall_manager=None, redacted_fields=None):
        if log_destination_configs and not isinstance(log_destination_configs, list):
            raise TypeError("Expected argument 'log_destination_configs' to be a list")
        pulumi.set(__self__, "log_destination_configs", log_destination_configs)
        if logging_filter and not isinstance(logging_filter, dict):
            raise TypeError("Expected argument 'logging_filter' to be a dict")
        pulumi.set(__self__, "logging_filter", logging_filter)
        if managed_by_firewall_manager and not isinstance(managed_by_firewall_manager, bool):
            raise TypeError("Expected argument 'managed_by_firewall_manager' to be a bool")
        pulumi.set(__self__, "managed_by_firewall_manager", managed_by_firewall_manager)
        if redacted_fields and not isinstance(redacted_fields, list):
            raise TypeError("Expected argument 'redacted_fields' to be a list")
        pulumi.set(__self__, "redacted_fields", redacted_fields)

    @property
    @pulumi.getter(name="logDestinationConfigs")
    def log_destination_configs(self) -> Optional[Sequence[str]]:
        """
        The Amazon Resource Names (ARNs) of the logging destinations that you want to associate with the web ACL.
        """
        return pulumi.get(self, "log_destination_configs")

    @property
    @pulumi.getter(name="loggingFilter")
    def logging_filter(self) -> Optional['outputs.LoggingFilterProperties']:
        """
        Filtering that specifies which web requests are kept in the logs and which are dropped. You can filter on the rule action and on the web request labels that were applied by matching rules during web ACL evaluation.
        """
        return pulumi.get(self, "logging_filter")

    @property
    @pulumi.getter(name="managedByFirewallManager")
    def managed_by_firewall_manager(self) -> Optional[bool]:
        """
        Indicates whether the logging configuration was created by AWS Firewall Manager, as part of an AWS WAF policy configuration. If true, only Firewall Manager can modify or delete the configuration.
        """
        return pulumi.get(self, "managed_by_firewall_manager")

    @property
    @pulumi.getter(name="redactedFields")
    def redacted_fields(self) -> Optional[Sequence['outputs.LoggingConfigurationFieldToMatch']]:
        """
        The parts of the request that you want to keep out of the logs. For example, if you redact the HEADER field, the HEADER field in the firehose will be xxx.
        """
        return pulumi.get(self, "redacted_fields")


class AwaitableGetLoggingConfigurationResult(GetLoggingConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoggingConfigurationResult(
            log_destination_configs=self.log_destination_configs,
            logging_filter=self.logging_filter,
            managed_by_firewall_manager=self.managed_by_firewall_manager,
            redacted_fields=self.redacted_fields)


def get_logging_configuration(resource_arn: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoggingConfigurationResult:
    """
    A WAFv2 Logging Configuration Resource Provider


    :param str resource_arn: The Amazon Resource Name (ARN) of the web ACL that you want to associate with LogDestinationConfigs.
    """
    __args__ = dict()
    __args__['resourceArn'] = resource_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:wafv2:getLoggingConfiguration', __args__, opts=opts, typ=GetLoggingConfigurationResult).value

    return AwaitableGetLoggingConfigurationResult(
        log_destination_configs=pulumi.get(__ret__, 'log_destination_configs'),
        logging_filter=pulumi.get(__ret__, 'logging_filter'),
        managed_by_firewall_manager=pulumi.get(__ret__, 'managed_by_firewall_manager'),
        redacted_fields=pulumi.get(__ret__, 'redacted_fields'))
def get_logging_configuration_output(resource_arn: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLoggingConfigurationResult]:
    """
    A WAFv2 Logging Configuration Resource Provider


    :param str resource_arn: The Amazon Resource Name (ARN) of the web ACL that you want to associate with LogDestinationConfigs.
    """
    __args__ = dict()
    __args__['resourceArn'] = resource_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:wafv2:getLoggingConfiguration', __args__, opts=opts, typ=GetLoggingConfigurationResult)
    return __ret__.apply(lambda __response__: GetLoggingConfigurationResult(
        log_destination_configs=pulumi.get(__response__, 'log_destination_configs'),
        logging_filter=pulumi.get(__response__, 'logging_filter'),
        managed_by_firewall_manager=pulumi.get(__response__, 'managed_by_firewall_manager'),
        redacted_fields=pulumi.get(__response__, 'redacted_fields')))
