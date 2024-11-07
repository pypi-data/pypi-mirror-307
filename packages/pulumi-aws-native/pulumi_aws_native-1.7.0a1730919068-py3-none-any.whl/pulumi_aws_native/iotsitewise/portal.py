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
from .. import _inputs as _root_inputs
from .. import outputs as _root_outputs
from ._inputs import *

__all__ = ['PortalArgs', 'Portal']

@pulumi.input_type
class PortalArgs:
    def __init__(__self__, *,
                 portal_contact_email: pulumi.Input[str],
                 role_arn: pulumi.Input[str],
                 alarms: Optional[pulumi.Input['AlarmsPropertiesArgs']] = None,
                 notification_sender_email: Optional[pulumi.Input[str]] = None,
                 portal_auth_mode: Optional[pulumi.Input[str]] = None,
                 portal_description: Optional[pulumi.Input[str]] = None,
                 portal_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Portal resource.
        :param pulumi.Input[str] portal_contact_email: The AWS administrator's contact email address.
        :param pulumi.Input[str] role_arn: The ARN of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf.
        :param pulumi.Input['AlarmsPropertiesArgs'] alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range.
        :param pulumi.Input[str] notification_sender_email: The email address that sends alarm notifications.
        :param pulumi.Input[str] portal_auth_mode: The service to use to authenticate users to the portal. Choose from SSO or IAM. You can't change this value after you create a portal.
        :param pulumi.Input[str] portal_description: A description for the portal.
        :param pulumi.Input[str] portal_name: A friendly name for the portal.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: A list of key-value pairs that contain metadata for the portal.
        """
        pulumi.set(__self__, "portal_contact_email", portal_contact_email)
        pulumi.set(__self__, "role_arn", role_arn)
        if alarms is not None:
            pulumi.set(__self__, "alarms", alarms)
        if notification_sender_email is not None:
            pulumi.set(__self__, "notification_sender_email", notification_sender_email)
        if portal_auth_mode is not None:
            pulumi.set(__self__, "portal_auth_mode", portal_auth_mode)
        if portal_description is not None:
            pulumi.set(__self__, "portal_description", portal_description)
        if portal_name is not None:
            pulumi.set(__self__, "portal_name", portal_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="portalContactEmail")
    def portal_contact_email(self) -> pulumi.Input[str]:
        """
        The AWS administrator's contact email address.
        """
        return pulumi.get(self, "portal_contact_email")

    @portal_contact_email.setter
    def portal_contact_email(self, value: pulumi.Input[str]):
        pulumi.set(self, "portal_contact_email", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The ARN of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def alarms(self) -> Optional[pulumi.Input['AlarmsPropertiesArgs']]:
        """
        Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range.
        """
        return pulumi.get(self, "alarms")

    @alarms.setter
    def alarms(self, value: Optional[pulumi.Input['AlarmsPropertiesArgs']]):
        pulumi.set(self, "alarms", value)

    @property
    @pulumi.getter(name="notificationSenderEmail")
    def notification_sender_email(self) -> Optional[pulumi.Input[str]]:
        """
        The email address that sends alarm notifications.
        """
        return pulumi.get(self, "notification_sender_email")

    @notification_sender_email.setter
    def notification_sender_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_sender_email", value)

    @property
    @pulumi.getter(name="portalAuthMode")
    def portal_auth_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The service to use to authenticate users to the portal. Choose from SSO or IAM. You can't change this value after you create a portal.
        """
        return pulumi.get(self, "portal_auth_mode")

    @portal_auth_mode.setter
    def portal_auth_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "portal_auth_mode", value)

    @property
    @pulumi.getter(name="portalDescription")
    def portal_description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the portal.
        """
        return pulumi.get(self, "portal_description")

    @portal_description.setter
    def portal_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "portal_description", value)

    @property
    @pulumi.getter(name="portalName")
    def portal_name(self) -> Optional[pulumi.Input[str]]:
        """
        A friendly name for the portal.
        """
        return pulumi.get(self, "portal_name")

    @portal_name.setter
    def portal_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "portal_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        A list of key-value pairs that contain metadata for the portal.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Portal(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alarms: Optional[pulumi.Input[Union['AlarmsPropertiesArgs', 'AlarmsPropertiesArgsDict']]] = None,
                 notification_sender_email: Optional[pulumi.Input[str]] = None,
                 portal_auth_mode: Optional[pulumi.Input[str]] = None,
                 portal_contact_email: Optional[pulumi.Input[str]] = None,
                 portal_description: Optional[pulumi.Input[str]] = None,
                 portal_name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS::IoTSiteWise::Portal

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['AlarmsPropertiesArgs', 'AlarmsPropertiesArgsDict']] alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range.
        :param pulumi.Input[str] notification_sender_email: The email address that sends alarm notifications.
        :param pulumi.Input[str] portal_auth_mode: The service to use to authenticate users to the portal. Choose from SSO or IAM. You can't change this value after you create a portal.
        :param pulumi.Input[str] portal_contact_email: The AWS administrator's contact email address.
        :param pulumi.Input[str] portal_description: A description for the portal.
        :param pulumi.Input[str] portal_name: A friendly name for the portal.
        :param pulumi.Input[str] role_arn: The ARN of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: A list of key-value pairs that contain metadata for the portal.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PortalArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::IoTSiteWise::Portal

        :param str resource_name: The name of the resource.
        :param PortalArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PortalArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alarms: Optional[pulumi.Input[Union['AlarmsPropertiesArgs', 'AlarmsPropertiesArgsDict']]] = None,
                 notification_sender_email: Optional[pulumi.Input[str]] = None,
                 portal_auth_mode: Optional[pulumi.Input[str]] = None,
                 portal_contact_email: Optional[pulumi.Input[str]] = None,
                 portal_description: Optional[pulumi.Input[str]] = None,
                 portal_name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PortalArgs.__new__(PortalArgs)

            __props__.__dict__["alarms"] = alarms
            __props__.__dict__["notification_sender_email"] = notification_sender_email
            __props__.__dict__["portal_auth_mode"] = portal_auth_mode
            if portal_contact_email is None and not opts.urn:
                raise TypeError("Missing required property 'portal_contact_email'")
            __props__.__dict__["portal_contact_email"] = portal_contact_email
            __props__.__dict__["portal_description"] = portal_description
            __props__.__dict__["portal_name"] = portal_name
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["portal_arn"] = None
            __props__.__dict__["portal_client_id"] = None
            __props__.__dict__["portal_id"] = None
            __props__.__dict__["portal_start_url"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["portalAuthMode"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Portal, __self__).__init__(
            'aws-native:iotsitewise:Portal',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Portal':
        """
        Get an existing Portal resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PortalArgs.__new__(PortalArgs)

        __props__.__dict__["alarms"] = None
        __props__.__dict__["notification_sender_email"] = None
        __props__.__dict__["portal_arn"] = None
        __props__.__dict__["portal_auth_mode"] = None
        __props__.__dict__["portal_client_id"] = None
        __props__.__dict__["portal_contact_email"] = None
        __props__.__dict__["portal_description"] = None
        __props__.__dict__["portal_id"] = None
        __props__.__dict__["portal_name"] = None
        __props__.__dict__["portal_start_url"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["tags"] = None
        return Portal(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def alarms(self) -> pulumi.Output[Optional['outputs.AlarmsProperties']]:
        """
        Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range.
        """
        return pulumi.get(self, "alarms")

    @property
    @pulumi.getter(name="notificationSenderEmail")
    def notification_sender_email(self) -> pulumi.Output[Optional[str]]:
        """
        The email address that sends alarm notifications.
        """
        return pulumi.get(self, "notification_sender_email")

    @property
    @pulumi.getter(name="portalArn")
    def portal_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the portal, which has the following format.
        """
        return pulumi.get(self, "portal_arn")

    @property
    @pulumi.getter(name="portalAuthMode")
    def portal_auth_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The service to use to authenticate users to the portal. Choose from SSO or IAM. You can't change this value after you create a portal.
        """
        return pulumi.get(self, "portal_auth_mode")

    @property
    @pulumi.getter(name="portalClientId")
    def portal_client_id(self) -> pulumi.Output[str]:
        """
        The AWS SSO application generated client ID (used with AWS SSO APIs).
        """
        return pulumi.get(self, "portal_client_id")

    @property
    @pulumi.getter(name="portalContactEmail")
    def portal_contact_email(self) -> pulumi.Output[str]:
        """
        The AWS administrator's contact email address.
        """
        return pulumi.get(self, "portal_contact_email")

    @property
    @pulumi.getter(name="portalDescription")
    def portal_description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for the portal.
        """
        return pulumi.get(self, "portal_description")

    @property
    @pulumi.getter(name="portalId")
    def portal_id(self) -> pulumi.Output[str]:
        """
        The ID of the portal.
        """
        return pulumi.get(self, "portal_id")

    @property
    @pulumi.getter(name="portalName")
    def portal_name(self) -> pulumi.Output[str]:
        """
        A friendly name for the portal.
        """
        return pulumi.get(self, "portal_name")

    @property
    @pulumi.getter(name="portalStartUrl")
    def portal_start_url(self) -> pulumi.Output[str]:
        """
        The public root URL for the AWS IoT AWS IoT SiteWise Monitor application portal.
        """
        return pulumi.get(self, "portal_start_url")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The ARN of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        A list of key-value pairs that contain metadata for the portal.
        """
        return pulumi.get(self, "tags")

