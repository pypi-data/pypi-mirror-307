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
from ._enums import *
from ._inputs import *

__all__ = ['GameSessionQueueArgs', 'GameSessionQueue']

@pulumi.input_type
class GameSessionQueueArgs:
    def __init__(__self__, *,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueueDestinationArgs']]]] = None,
                 filter_configuration: Optional[pulumi.Input['GameSessionQueueFilterConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]] = None,
                 priority_configuration: Optional[pulumi.Input['GameSessionQueuePriorityConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a GameSessionQueue resource.
        :param pulumi.Input[str] custom_event_data: Information that is added to all events that are related to this game session queue.
        :param pulumi.Input[Sequence[pulumi.Input['GameSessionQueueDestinationArgs']]] destinations: A list of fleets and/or fleet aliases that can be used to fulfill game session placement requests in the queue.
        :param pulumi.Input['GameSessionQueueFilterConfigurationArgs'] filter_configuration: A list of locations where a queue is allowed to place new game sessions.
        :param pulumi.Input[str] name: A descriptive label that is associated with game session queue. Queue names must be unique within each Region.
        :param pulumi.Input[str] notification_target: An SNS topic ARN that is set up to receive game session placement notifications.
        :param pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]] player_latency_policies: A set of policies that act as a sliding cap on player latency.
        :param pulumi.Input['GameSessionQueuePriorityConfigurationArgs'] priority_configuration: Custom settings to use when prioritizing destinations and locations for game session placements.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[int] timeout_in_seconds: The maximum time, in seconds, that a new game session placement request remains in the queue.
        """
        if custom_event_data is not None:
            pulumi.set(__self__, "custom_event_data", custom_event_data)
        if destinations is not None:
            pulumi.set(__self__, "destinations", destinations)
        if filter_configuration is not None:
            pulumi.set(__self__, "filter_configuration", filter_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if notification_target is not None:
            pulumi.set(__self__, "notification_target", notification_target)
        if player_latency_policies is not None:
            pulumi.set(__self__, "player_latency_policies", player_latency_policies)
        if priority_configuration is not None:
            pulumi.set(__self__, "priority_configuration", priority_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)

    @property
    @pulumi.getter(name="customEventData")
    def custom_event_data(self) -> Optional[pulumi.Input[str]]:
        """
        Information that is added to all events that are related to this game session queue.
        """
        return pulumi.get(self, "custom_event_data")

    @custom_event_data.setter
    def custom_event_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_event_data", value)

    @property
    @pulumi.getter
    def destinations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueueDestinationArgs']]]]:
        """
        A list of fleets and/or fleet aliases that can be used to fulfill game session placement requests in the queue.
        """
        return pulumi.get(self, "destinations")

    @destinations.setter
    def destinations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueueDestinationArgs']]]]):
        pulumi.set(self, "destinations", value)

    @property
    @pulumi.getter(name="filterConfiguration")
    def filter_configuration(self) -> Optional[pulumi.Input['GameSessionQueueFilterConfigurationArgs']]:
        """
        A list of locations where a queue is allowed to place new game sessions.
        """
        return pulumi.get(self, "filter_configuration")

    @filter_configuration.setter
    def filter_configuration(self, value: Optional[pulumi.Input['GameSessionQueueFilterConfigurationArgs']]):
        pulumi.set(self, "filter_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A descriptive label that is associated with game session queue. Queue names must be unique within each Region.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notificationTarget")
    def notification_target(self) -> Optional[pulumi.Input[str]]:
        """
        An SNS topic ARN that is set up to receive game session placement notifications.
        """
        return pulumi.get(self, "notification_target")

    @notification_target.setter
    def notification_target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notification_target", value)

    @property
    @pulumi.getter(name="playerLatencyPolicies")
    def player_latency_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]]:
        """
        A set of policies that act as a sliding cap on player latency.
        """
        return pulumi.get(self, "player_latency_policies")

    @player_latency_policies.setter
    def player_latency_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GameSessionQueuePlayerLatencyPolicyArgs']]]]):
        pulumi.set(self, "player_latency_policies", value)

    @property
    @pulumi.getter(name="priorityConfiguration")
    def priority_configuration(self) -> Optional[pulumi.Input['GameSessionQueuePriorityConfigurationArgs']]:
        """
        Custom settings to use when prioritizing destinations and locations for game session placements.
        """
        return pulumi.get(self, "priority_configuration")

    @priority_configuration.setter
    def priority_configuration(self, value: Optional[pulumi.Input['GameSessionQueuePriorityConfigurationArgs']]):
        pulumi.set(self, "priority_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum time, in seconds, that a new game session placement request remains in the queue.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_in_seconds", value)


class GameSessionQueue(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GameSessionQueueDestinationArgs', 'GameSessionQueueDestinationArgsDict']]]]] = None,
                 filter_configuration: Optional[pulumi.Input[Union['GameSessionQueueFilterConfigurationArgs', 'GameSessionQueueFilterConfigurationArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GameSessionQueuePlayerLatencyPolicyArgs', 'GameSessionQueuePlayerLatencyPolicyArgsDict']]]]] = None,
                 priority_configuration: Optional[pulumi.Input[Union['GameSessionQueuePriorityConfigurationArgs', 'GameSessionQueuePriorityConfigurationArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        The AWS::GameLift::GameSessionQueue resource creates an Amazon GameLift (GameLift) game session queue.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        queue = aws_native.gamelift.GameSessionQueue("queue",
            name="MyGameSessionQueue",
            timeout_in_seconds=60,
            notification_target="arn:aws:sns:us-west-2:111122223333:My_Placement_SNS_Topic",
            destinations=[
                {
                    "destination_arn": "arn:aws:gamelift:us-west-2:012345678912:fleet/fleet-id",
                },
                {
                    "destination_arn": "arn:aws:gamelift:us-west-2:012345678912:alias/alias-id",
                },
            ],
            player_latency_policies=[{
                "maximum_individual_player_latency_milliseconds": 1000,
                "policy_duration_seconds": 60,
            }],
            priority_configuration={
                "location_order": [
                    "us-west-2",
                    "us-east-1",
                ],
                "priority_order": [
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.COST,
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.LATENCY,
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.LOCATION,
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.DESTINATION,
                ],
            },
            filter_configuration={
                "allowed_locations": [
                    "us-east-1",
                    "us-west-2",
                ],
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        queue_resource = aws_native.gamelift.GameSessionQueue("queueResource", name="MyGameSessionQueue")
        matchmaking_rule_set_resource = aws_native.gamelift.MatchmakingRuleSet("matchmakingRuleSetResource",
            name="MyRuleSet",
            rule_set_body="{\\"name\\": \\"MyMatchmakingRuleSet\\",\\"ruleLanguageVersion\\": \\"1.0\\", \\"teams\\": [{\\"name\\": \\"MyTeam\\",\\"minPlayers\\": 1,\\"maxPlayers\\": 20}]}")
        matchmaking_configuration_resource = aws_native.gamelift.MatchmakingConfiguration("matchmakingConfigurationResource",
            name="MyMatchmakingConfiguration",
            acceptance_required=True,
            acceptance_timeout_seconds=60,
            additional_player_count=8,
            backfill_mode=aws_native.gamelift.MatchmakingConfigurationBackfillMode.AUTOMATIC,
            custom_event_data="MyCustomEventData",
            description="A basic matchmaking configuration for a GameLift-hosted game",
            flex_match_mode=aws_native.gamelift.MatchmakingConfigurationFlexMatchMode.WITH_QUEUE,
            game_session_data="MyGameSessionData",
            game_properties=[
                {
                    "key": "level",
                    "value": "10",
                },
                {
                    "key": "gameMode",
                    "value": "hard",
                },
            ],
            game_session_queue_arns=[queue_resource.arn],
            request_timeout_seconds=100,
            rule_set_name=matchmaking_rule_set_resource.id,
            opts = pulumi.ResourceOptions(depends_on=[
                    queue_resource,
                    matchmaking_rule_set_resource,
                ]))

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_event_data: Information that is added to all events that are related to this game session queue.
        :param pulumi.Input[Sequence[pulumi.Input[Union['GameSessionQueueDestinationArgs', 'GameSessionQueueDestinationArgsDict']]]] destinations: A list of fleets and/or fleet aliases that can be used to fulfill game session placement requests in the queue.
        :param pulumi.Input[Union['GameSessionQueueFilterConfigurationArgs', 'GameSessionQueueFilterConfigurationArgsDict']] filter_configuration: A list of locations where a queue is allowed to place new game sessions.
        :param pulumi.Input[str] name: A descriptive label that is associated with game session queue. Queue names must be unique within each Region.
        :param pulumi.Input[str] notification_target: An SNS topic ARN that is set up to receive game session placement notifications.
        :param pulumi.Input[Sequence[pulumi.Input[Union['GameSessionQueuePlayerLatencyPolicyArgs', 'GameSessionQueuePlayerLatencyPolicyArgsDict']]]] player_latency_policies: A set of policies that act as a sliding cap on player latency.
        :param pulumi.Input[Union['GameSessionQueuePriorityConfigurationArgs', 'GameSessionQueuePriorityConfigurationArgsDict']] priority_configuration: Custom settings to use when prioritizing destinations and locations for game session placements.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: An array of key-value pairs to apply to this resource.
        :param pulumi.Input[int] timeout_in_seconds: The maximum time, in seconds, that a new game session placement request remains in the queue.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GameSessionQueueArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The AWS::GameLift::GameSessionQueue resource creates an Amazon GameLift (GameLift) game session queue.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        queue = aws_native.gamelift.GameSessionQueue("queue",
            name="MyGameSessionQueue",
            timeout_in_seconds=60,
            notification_target="arn:aws:sns:us-west-2:111122223333:My_Placement_SNS_Topic",
            destinations=[
                {
                    "destination_arn": "arn:aws:gamelift:us-west-2:012345678912:fleet/fleet-id",
                },
                {
                    "destination_arn": "arn:aws:gamelift:us-west-2:012345678912:alias/alias-id",
                },
            ],
            player_latency_policies=[{
                "maximum_individual_player_latency_milliseconds": 1000,
                "policy_duration_seconds": 60,
            }],
            priority_configuration={
                "location_order": [
                    "us-west-2",
                    "us-east-1",
                ],
                "priority_order": [
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.COST,
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.LATENCY,
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.LOCATION,
                    aws_native.gamelift.GameSessionQueuePriorityOrderItem.DESTINATION,
                ],
            },
            filter_configuration={
                "allowed_locations": [
                    "us-east-1",
                    "us-west-2",
                ],
            })

        ```
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        queue_resource = aws_native.gamelift.GameSessionQueue("queueResource", name="MyGameSessionQueue")
        matchmaking_rule_set_resource = aws_native.gamelift.MatchmakingRuleSet("matchmakingRuleSetResource",
            name="MyRuleSet",
            rule_set_body="{\\"name\\": \\"MyMatchmakingRuleSet\\",\\"ruleLanguageVersion\\": \\"1.0\\", \\"teams\\": [{\\"name\\": \\"MyTeam\\",\\"minPlayers\\": 1,\\"maxPlayers\\": 20}]}")
        matchmaking_configuration_resource = aws_native.gamelift.MatchmakingConfiguration("matchmakingConfigurationResource",
            name="MyMatchmakingConfiguration",
            acceptance_required=True,
            acceptance_timeout_seconds=60,
            additional_player_count=8,
            backfill_mode=aws_native.gamelift.MatchmakingConfigurationBackfillMode.AUTOMATIC,
            custom_event_data="MyCustomEventData",
            description="A basic matchmaking configuration for a GameLift-hosted game",
            flex_match_mode=aws_native.gamelift.MatchmakingConfigurationFlexMatchMode.WITH_QUEUE,
            game_session_data="MyGameSessionData",
            game_properties=[
                {
                    "key": "level",
                    "value": "10",
                },
                {
                    "key": "gameMode",
                    "value": "hard",
                },
            ],
            game_session_queue_arns=[queue_resource.arn],
            request_timeout_seconds=100,
            rule_set_name=matchmaking_rule_set_resource.id,
            opts = pulumi.ResourceOptions(depends_on=[
                    queue_resource,
                    matchmaking_rule_set_resource,
                ]))

        ```

        :param str resource_name: The name of the resource.
        :param GameSessionQueueArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GameSessionQueueArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_event_data: Optional[pulumi.Input[str]] = None,
                 destinations: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GameSessionQueueDestinationArgs', 'GameSessionQueueDestinationArgsDict']]]]] = None,
                 filter_configuration: Optional[pulumi.Input[Union['GameSessionQueueFilterConfigurationArgs', 'GameSessionQueueFilterConfigurationArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notification_target: Optional[pulumi.Input[str]] = None,
                 player_latency_policies: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GameSessionQueuePlayerLatencyPolicyArgs', 'GameSessionQueuePlayerLatencyPolicyArgsDict']]]]] = None,
                 priority_configuration: Optional[pulumi.Input[Union['GameSessionQueuePriorityConfigurationArgs', 'GameSessionQueuePriorityConfigurationArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GameSessionQueueArgs.__new__(GameSessionQueueArgs)

            __props__.__dict__["custom_event_data"] = custom_event_data
            __props__.__dict__["destinations"] = destinations
            __props__.__dict__["filter_configuration"] = filter_configuration
            __props__.__dict__["name"] = name
            __props__.__dict__["notification_target"] = notification_target
            __props__.__dict__["player_latency_policies"] = player_latency_policies
            __props__.__dict__["priority_configuration"] = priority_configuration
            __props__.__dict__["tags"] = tags
            __props__.__dict__["timeout_in_seconds"] = timeout_in_seconds
            __props__.__dict__["arn"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(GameSessionQueue, __self__).__init__(
            'aws-native:gamelift:GameSessionQueue',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GameSessionQueue':
        """
        Get an existing GameSessionQueue resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GameSessionQueueArgs.__new__(GameSessionQueueArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["custom_event_data"] = None
        __props__.__dict__["destinations"] = None
        __props__.__dict__["filter_configuration"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["notification_target"] = None
        __props__.__dict__["player_latency_policies"] = None
        __props__.__dict__["priority_configuration"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["timeout_in_seconds"] = None
        return GameSessionQueue(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) that is assigned to a Amazon GameLift game session queue resource and uniquely identifies it.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="customEventData")
    def custom_event_data(self) -> pulumi.Output[Optional[str]]:
        """
        Information that is added to all events that are related to this game session queue.
        """
        return pulumi.get(self, "custom_event_data")

    @property
    @pulumi.getter
    def destinations(self) -> pulumi.Output[Optional[Sequence['outputs.GameSessionQueueDestination']]]:
        """
        A list of fleets and/or fleet aliases that can be used to fulfill game session placement requests in the queue.
        """
        return pulumi.get(self, "destinations")

    @property
    @pulumi.getter(name="filterConfiguration")
    def filter_configuration(self) -> pulumi.Output[Optional['outputs.GameSessionQueueFilterConfiguration']]:
        """
        A list of locations where a queue is allowed to place new game sessions.
        """
        return pulumi.get(self, "filter_configuration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A descriptive label that is associated with game session queue. Queue names must be unique within each Region.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notificationTarget")
    def notification_target(self) -> pulumi.Output[Optional[str]]:
        """
        An SNS topic ARN that is set up to receive game session placement notifications.
        """
        return pulumi.get(self, "notification_target")

    @property
    @pulumi.getter(name="playerLatencyPolicies")
    def player_latency_policies(self) -> pulumi.Output[Optional[Sequence['outputs.GameSessionQueuePlayerLatencyPolicy']]]:
        """
        A set of policies that act as a sliding cap on player latency.
        """
        return pulumi.get(self, "player_latency_policies")

    @property
    @pulumi.getter(name="priorityConfiguration")
    def priority_configuration(self) -> pulumi.Output[Optional['outputs.GameSessionQueuePriorityConfiguration']]:
        """
        Custom settings to use when prioritizing destinations and locations for game session placements.
        """
        return pulumi.get(self, "priority_configuration")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum time, in seconds, that a new game session placement request remains in the queue.
        """
        return pulumi.get(self, "timeout_in_seconds")

