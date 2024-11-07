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
from ._inputs import *

__all__ = ['CisScanConfigurationArgs', 'CisScanConfiguration']

@pulumi.input_type
class CisScanConfigurationArgs:
    def __init__(__self__, *,
                 scan_name: pulumi.Input[str],
                 schedule: pulumi.Input['CisScanConfigurationScheduleArgs'],
                 security_level: pulumi.Input['CisScanConfigurationCisSecurityLevel'],
                 targets: pulumi.Input['CisScanConfigurationCisTargetsArgs'],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a CisScanConfiguration resource.
        :param pulumi.Input[str] scan_name: Name of the scan
        :param pulumi.Input['CisScanConfigurationScheduleArgs'] schedule: The CIS scan configuration's schedule.
        :param pulumi.Input['CisScanConfigurationCisSecurityLevel'] security_level: The CIS scan configuration's CIS Benchmark level.
        :param pulumi.Input['CisScanConfigurationCisTargetsArgs'] targets: The CIS scan configuration's targets.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The CIS scan configuration's tags.
        """
        pulumi.set(__self__, "scan_name", scan_name)
        pulumi.set(__self__, "schedule", schedule)
        pulumi.set(__self__, "security_level", security_level)
        pulumi.set(__self__, "targets", targets)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="scanName")
    def scan_name(self) -> pulumi.Input[str]:
        """
        Name of the scan
        """
        return pulumi.get(self, "scan_name")

    @scan_name.setter
    def scan_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "scan_name", value)

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Input['CisScanConfigurationScheduleArgs']:
        """
        The CIS scan configuration's schedule.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: pulumi.Input['CisScanConfigurationScheduleArgs']):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="securityLevel")
    def security_level(self) -> pulumi.Input['CisScanConfigurationCisSecurityLevel']:
        """
        The CIS scan configuration's CIS Benchmark level.
        """
        return pulumi.get(self, "security_level")

    @security_level.setter
    def security_level(self, value: pulumi.Input['CisScanConfigurationCisSecurityLevel']):
        pulumi.set(self, "security_level", value)

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Input['CisScanConfigurationCisTargetsArgs']:
        """
        The CIS scan configuration's targets.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: pulumi.Input['CisScanConfigurationCisTargetsArgs']):
        pulumi.set(self, "targets", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The CIS scan configuration's tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class CisScanConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 scan_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[Union['CisScanConfigurationScheduleArgs', 'CisScanConfigurationScheduleArgsDict']]] = None,
                 security_level: Optional[pulumi.Input['CisScanConfigurationCisSecurityLevel']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 targets: Optional[pulumi.Input[Union['CisScanConfigurationCisTargetsArgs', 'CisScanConfigurationCisTargetsArgsDict']]] = None,
                 __props__=None):
        """
        CIS Scan Configuration resource schema

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] scan_name: Name of the scan
        :param pulumi.Input[Union['CisScanConfigurationScheduleArgs', 'CisScanConfigurationScheduleArgsDict']] schedule: The CIS scan configuration's schedule.
        :param pulumi.Input['CisScanConfigurationCisSecurityLevel'] security_level: The CIS scan configuration's CIS Benchmark level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The CIS scan configuration's tags.
        :param pulumi.Input[Union['CisScanConfigurationCisTargetsArgs', 'CisScanConfigurationCisTargetsArgsDict']] targets: The CIS scan configuration's targets.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CisScanConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        CIS Scan Configuration resource schema

        :param str resource_name: The name of the resource.
        :param CisScanConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CisScanConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 scan_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[Union['CisScanConfigurationScheduleArgs', 'CisScanConfigurationScheduleArgsDict']]] = None,
                 security_level: Optional[pulumi.Input['CisScanConfigurationCisSecurityLevel']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 targets: Optional[pulumi.Input[Union['CisScanConfigurationCisTargetsArgs', 'CisScanConfigurationCisTargetsArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CisScanConfigurationArgs.__new__(CisScanConfigurationArgs)

            if scan_name is None and not opts.urn:
                raise TypeError("Missing required property 'scan_name'")
            __props__.__dict__["scan_name"] = scan_name
            if schedule is None and not opts.urn:
                raise TypeError("Missing required property 'schedule'")
            __props__.__dict__["schedule"] = schedule
            if security_level is None and not opts.urn:
                raise TypeError("Missing required property 'security_level'")
            __props__.__dict__["security_level"] = security_level
            __props__.__dict__["tags"] = tags
            if targets is None and not opts.urn:
                raise TypeError("Missing required property 'targets'")
            __props__.__dict__["targets"] = targets
            __props__.__dict__["arn"] = None
        super(CisScanConfiguration, __self__).__init__(
            'aws-native:inspectorv2:CisScanConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CisScanConfiguration':
        """
        Get an existing CisScanConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CisScanConfigurationArgs.__new__(CisScanConfigurationArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["scan_name"] = None
        __props__.__dict__["schedule"] = None
        __props__.__dict__["security_level"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["targets"] = None
        return CisScanConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        CIS Scan configuration unique identifier
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="scanName")
    def scan_name(self) -> pulumi.Output[str]:
        """
        Name of the scan
        """
        return pulumi.get(self, "scan_name")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output['outputs.CisScanConfigurationSchedule']:
        """
        The CIS scan configuration's schedule.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="securityLevel")
    def security_level(self) -> pulumi.Output['CisScanConfigurationCisSecurityLevel']:
        """
        The CIS scan configuration's CIS Benchmark level.
        """
        return pulumi.get(self, "security_level")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The CIS scan configuration's tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def targets(self) -> pulumi.Output['outputs.CisScanConfigurationCisTargets']:
        """
        The CIS scan configuration's targets.
        """
        return pulumi.get(self, "targets")

