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

__all__ = [
    'GetConnectAttachmentResult',
    'AwaitableGetConnectAttachmentResult',
    'get_connect_attachment',
    'get_connect_attachment_output',
]

@pulumi.output_type
class GetConnectAttachmentResult:
    def __init__(__self__, attachment_id=None, attachment_policy_rule_number=None, attachment_type=None, core_network_arn=None, created_at=None, network_function_group_name=None, owner_account_id=None, proposed_network_function_group_change=None, proposed_segment_change=None, resource_arn=None, segment_name=None, state=None, tags=None, updated_at=None):
        if attachment_id and not isinstance(attachment_id, str):
            raise TypeError("Expected argument 'attachment_id' to be a str")
        pulumi.set(__self__, "attachment_id", attachment_id)
        if attachment_policy_rule_number and not isinstance(attachment_policy_rule_number, int):
            raise TypeError("Expected argument 'attachment_policy_rule_number' to be a int")
        pulumi.set(__self__, "attachment_policy_rule_number", attachment_policy_rule_number)
        if attachment_type and not isinstance(attachment_type, str):
            raise TypeError("Expected argument 'attachment_type' to be a str")
        pulumi.set(__self__, "attachment_type", attachment_type)
        if core_network_arn and not isinstance(core_network_arn, str):
            raise TypeError("Expected argument 'core_network_arn' to be a str")
        pulumi.set(__self__, "core_network_arn", core_network_arn)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if network_function_group_name and not isinstance(network_function_group_name, str):
            raise TypeError("Expected argument 'network_function_group_name' to be a str")
        pulumi.set(__self__, "network_function_group_name", network_function_group_name)
        if owner_account_id and not isinstance(owner_account_id, str):
            raise TypeError("Expected argument 'owner_account_id' to be a str")
        pulumi.set(__self__, "owner_account_id", owner_account_id)
        if proposed_network_function_group_change and not isinstance(proposed_network_function_group_change, dict):
            raise TypeError("Expected argument 'proposed_network_function_group_change' to be a dict")
        pulumi.set(__self__, "proposed_network_function_group_change", proposed_network_function_group_change)
        if proposed_segment_change and not isinstance(proposed_segment_change, dict):
            raise TypeError("Expected argument 'proposed_segment_change' to be a dict")
        pulumi.set(__self__, "proposed_segment_change", proposed_segment_change)
        if resource_arn and not isinstance(resource_arn, str):
            raise TypeError("Expected argument 'resource_arn' to be a str")
        pulumi.set(__self__, "resource_arn", resource_arn)
        if segment_name and not isinstance(segment_name, str):
            raise TypeError("Expected argument 'segment_name' to be a str")
        pulumi.set(__self__, "segment_name", segment_name)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="attachmentId")
    def attachment_id(self) -> Optional[str]:
        """
        The ID of the attachment.
        """
        return pulumi.get(self, "attachment_id")

    @property
    @pulumi.getter(name="attachmentPolicyRuleNumber")
    def attachment_policy_rule_number(self) -> Optional[int]:
        """
        The policy rule number associated with the attachment.
        """
        return pulumi.get(self, "attachment_policy_rule_number")

    @property
    @pulumi.getter(name="attachmentType")
    def attachment_type(self) -> Optional[str]:
        """
        The type of attachment.
        """
        return pulumi.get(self, "attachment_type")

    @property
    @pulumi.getter(name="coreNetworkArn")
    def core_network_arn(self) -> Optional[str]:
        """
        The ARN of a core network.
        """
        return pulumi.get(self, "core_network_arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        Creation time of the attachment.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="networkFunctionGroupName")
    def network_function_group_name(self) -> Optional[str]:
        """
        The name of the network function group attachment.
        """
        return pulumi.get(self, "network_function_group_name")

    @property
    @pulumi.getter(name="ownerAccountId")
    def owner_account_id(self) -> Optional[str]:
        """
        The ID of the attachment account owner.
        """
        return pulumi.get(self, "owner_account_id")

    @property
    @pulumi.getter(name="proposedNetworkFunctionGroupChange")
    def proposed_network_function_group_change(self) -> Optional['outputs.ConnectAttachmentProposedNetworkFunctionGroupChange']:
        """
        The attachment to move from one network function group to another.
        """
        return pulumi.get(self, "proposed_network_function_group_change")

    @property
    @pulumi.getter(name="proposedSegmentChange")
    def proposed_segment_change(self) -> Optional['outputs.ConnectAttachmentProposedSegmentChange']:
        """
        The attachment to move from one segment to another.
        """
        return pulumi.get(self, "proposed_segment_change")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[str]:
        """
        The attachment resource ARN.
        """
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter(name="segmentName")
    def segment_name(self) -> Optional[str]:
        """
        The name of the segment attachment.
        """
        return pulumi.get(self, "segment_name")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        State of the attachment.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Tags for the attachment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        Last update time of the attachment.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetConnectAttachmentResult(GetConnectAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectAttachmentResult(
            attachment_id=self.attachment_id,
            attachment_policy_rule_number=self.attachment_policy_rule_number,
            attachment_type=self.attachment_type,
            core_network_arn=self.core_network_arn,
            created_at=self.created_at,
            network_function_group_name=self.network_function_group_name,
            owner_account_id=self.owner_account_id,
            proposed_network_function_group_change=self.proposed_network_function_group_change,
            proposed_segment_change=self.proposed_segment_change,
            resource_arn=self.resource_arn,
            segment_name=self.segment_name,
            state=self.state,
            tags=self.tags,
            updated_at=self.updated_at)


def get_connect_attachment(attachment_id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectAttachmentResult:
    """
    AWS::NetworkManager::ConnectAttachment Resource Type Definition


    :param str attachment_id: The ID of the attachment.
    """
    __args__ = dict()
    __args__['attachmentId'] = attachment_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:networkmanager:getConnectAttachment', __args__, opts=opts, typ=GetConnectAttachmentResult).value

    return AwaitableGetConnectAttachmentResult(
        attachment_id=pulumi.get(__ret__, 'attachment_id'),
        attachment_policy_rule_number=pulumi.get(__ret__, 'attachment_policy_rule_number'),
        attachment_type=pulumi.get(__ret__, 'attachment_type'),
        core_network_arn=pulumi.get(__ret__, 'core_network_arn'),
        created_at=pulumi.get(__ret__, 'created_at'),
        network_function_group_name=pulumi.get(__ret__, 'network_function_group_name'),
        owner_account_id=pulumi.get(__ret__, 'owner_account_id'),
        proposed_network_function_group_change=pulumi.get(__ret__, 'proposed_network_function_group_change'),
        proposed_segment_change=pulumi.get(__ret__, 'proposed_segment_change'),
        resource_arn=pulumi.get(__ret__, 'resource_arn'),
        segment_name=pulumi.get(__ret__, 'segment_name'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        updated_at=pulumi.get(__ret__, 'updated_at'))
def get_connect_attachment_output(attachment_id: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConnectAttachmentResult]:
    """
    AWS::NetworkManager::ConnectAttachment Resource Type Definition


    :param str attachment_id: The ID of the attachment.
    """
    __args__ = dict()
    __args__['attachmentId'] = attachment_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:networkmanager:getConnectAttachment', __args__, opts=opts, typ=GetConnectAttachmentResult)
    return __ret__.apply(lambda __response__: GetConnectAttachmentResult(
        attachment_id=pulumi.get(__response__, 'attachment_id'),
        attachment_policy_rule_number=pulumi.get(__response__, 'attachment_policy_rule_number'),
        attachment_type=pulumi.get(__response__, 'attachment_type'),
        core_network_arn=pulumi.get(__response__, 'core_network_arn'),
        created_at=pulumi.get(__response__, 'created_at'),
        network_function_group_name=pulumi.get(__response__, 'network_function_group_name'),
        owner_account_id=pulumi.get(__response__, 'owner_account_id'),
        proposed_network_function_group_change=pulumi.get(__response__, 'proposed_network_function_group_change'),
        proposed_segment_change=pulumi.get(__response__, 'proposed_segment_change'),
        resource_arn=pulumi.get(__response__, 'resource_arn'),
        segment_name=pulumi.get(__response__, 'segment_name'),
        state=pulumi.get(__response__, 'state'),
        tags=pulumi.get(__response__, 'tags'),
        updated_at=pulumi.get(__response__, 'updated_at')))
