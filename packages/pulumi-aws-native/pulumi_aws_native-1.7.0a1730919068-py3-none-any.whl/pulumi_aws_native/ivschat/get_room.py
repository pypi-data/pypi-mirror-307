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
    'GetRoomResult',
    'AwaitableGetRoomResult',
    'get_room',
    'get_room_output',
]

@pulumi.output_type
class GetRoomResult:
    def __init__(__self__, arn=None, id=None, logging_configuration_identifiers=None, maximum_message_length=None, maximum_message_rate_per_second=None, message_review_handler=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if logging_configuration_identifiers and not isinstance(logging_configuration_identifiers, list):
            raise TypeError("Expected argument 'logging_configuration_identifiers' to be a list")
        pulumi.set(__self__, "logging_configuration_identifiers", logging_configuration_identifiers)
        if maximum_message_length and not isinstance(maximum_message_length, int):
            raise TypeError("Expected argument 'maximum_message_length' to be a int")
        pulumi.set(__self__, "maximum_message_length", maximum_message_length)
        if maximum_message_rate_per_second and not isinstance(maximum_message_rate_per_second, int):
            raise TypeError("Expected argument 'maximum_message_rate_per_second' to be a int")
        pulumi.set(__self__, "maximum_message_rate_per_second", maximum_message_rate_per_second)
        if message_review_handler and not isinstance(message_review_handler, dict):
            raise TypeError("Expected argument 'message_review_handler' to be a dict")
        pulumi.set(__self__, "message_review_handler", message_review_handler)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Room ARN is automatically generated on creation and assigned as the unique identifier.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The system-generated ID of the room.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="loggingConfigurationIdentifiers")
    def logging_configuration_identifiers(self) -> Optional[Sequence[str]]:
        """
        Array of logging configuration identifiers attached to the room.
        """
        return pulumi.get(self, "logging_configuration_identifiers")

    @property
    @pulumi.getter(name="maximumMessageLength")
    def maximum_message_length(self) -> Optional[int]:
        """
        The maximum number of characters in a single message.
        """
        return pulumi.get(self, "maximum_message_length")

    @property
    @pulumi.getter(name="maximumMessageRatePerSecond")
    def maximum_message_rate_per_second(self) -> Optional[int]:
        """
        The maximum number of messages per second that can be sent to the room.
        """
        return pulumi.get(self, "maximum_message_rate_per_second")

    @property
    @pulumi.getter(name="messageReviewHandler")
    def message_review_handler(self) -> Optional['outputs.RoomMessageReviewHandler']:
        """
        Configuration information for optional review of messages.
        """
        return pulumi.get(self, "message_review_handler")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the room. The value does not need to be unique.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRoomResult(GetRoomResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoomResult(
            arn=self.arn,
            id=self.id,
            logging_configuration_identifiers=self.logging_configuration_identifiers,
            maximum_message_length=self.maximum_message_length,
            maximum_message_rate_per_second=self.maximum_message_rate_per_second,
            message_review_handler=self.message_review_handler,
            name=self.name,
            tags=self.tags)


def get_room(arn: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoomResult:
    """
    Resource type definition for AWS::IVSChat::Room.


    :param str arn: Room ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ivschat:getRoom', __args__, opts=opts, typ=GetRoomResult).value

    return AwaitableGetRoomResult(
        arn=pulumi.get(__ret__, 'arn'),
        id=pulumi.get(__ret__, 'id'),
        logging_configuration_identifiers=pulumi.get(__ret__, 'logging_configuration_identifiers'),
        maximum_message_length=pulumi.get(__ret__, 'maximum_message_length'),
        maximum_message_rate_per_second=pulumi.get(__ret__, 'maximum_message_rate_per_second'),
        message_review_handler=pulumi.get(__ret__, 'message_review_handler'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))
def get_room_output(arn: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoomResult]:
    """
    Resource type definition for AWS::IVSChat::Room.


    :param str arn: Room ARN is automatically generated on creation and assigned as the unique identifier.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ivschat:getRoom', __args__, opts=opts, typ=GetRoomResult)
    return __ret__.apply(lambda __response__: GetRoomResult(
        arn=pulumi.get(__response__, 'arn'),
        id=pulumi.get(__response__, 'id'),
        logging_configuration_identifiers=pulumi.get(__response__, 'logging_configuration_identifiers'),
        maximum_message_length=pulumi.get(__response__, 'maximum_message_length'),
        maximum_message_rate_per_second=pulumi.get(__response__, 'maximum_message_rate_per_second'),
        message_review_handler=pulumi.get(__response__, 'message_review_handler'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags')))
