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
    'ContactChannelTargetInfoArgs',
    'ContactChannelTargetInfoArgsDict',
    'ContactStageArgs',
    'ContactStageArgsDict',
    'ContactTargetInfoArgs',
    'ContactTargetInfoArgsDict',
    'ContactTargetsArgs',
    'ContactTargetsArgsDict',
    'PlanChannelTargetInfoArgs',
    'PlanChannelTargetInfoArgsDict',
    'PlanContactTargetInfoArgs',
    'PlanContactTargetInfoArgsDict',
    'PlanStageArgs',
    'PlanStageArgsDict',
    'PlanTargetsArgs',
    'PlanTargetsArgsDict',
    'RotationCoverageTimeArgs',
    'RotationCoverageTimeArgsDict',
    'RotationMonthlySettingArgs',
    'RotationMonthlySettingArgsDict',
    'RotationRecurrenceSettingsArgs',
    'RotationRecurrenceSettingsArgsDict',
    'RotationShiftCoverageArgs',
    'RotationShiftCoverageArgsDict',
    'RotationWeeklySettingArgs',
    'RotationWeeklySettingArgsDict',
]

MYPY = False

if not MYPY:
    class ContactChannelTargetInfoArgsDict(TypedDict):
        """
        Information about the contact channel that SSM Incident Manager uses to engage the contact.
        """
        channel_id: pulumi.Input[str]
        """
        The Amazon Resource Name (ARN) of the contact channel.
        """
        retry_interval_in_minutes: pulumi.Input[int]
        """
        The number of minutes to wait to retry sending engagement in the case the engagement initially fails.
        """
elif False:
    ContactChannelTargetInfoArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ContactChannelTargetInfoArgs:
    def __init__(__self__, *,
                 channel_id: pulumi.Input[str],
                 retry_interval_in_minutes: pulumi.Input[int]):
        """
        Information about the contact channel that SSM Incident Manager uses to engage the contact.
        :param pulumi.Input[str] channel_id: The Amazon Resource Name (ARN) of the contact channel.
        :param pulumi.Input[int] retry_interval_in_minutes: The number of minutes to wait to retry sending engagement in the case the engagement initially fails.
        """
        pulumi.set(__self__, "channel_id", channel_id)
        pulumi.set(__self__, "retry_interval_in_minutes", retry_interval_in_minutes)

    @property
    @pulumi.getter(name="channelId")
    def channel_id(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the contact channel.
        """
        return pulumi.get(self, "channel_id")

    @channel_id.setter
    def channel_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "channel_id", value)

    @property
    @pulumi.getter(name="retryIntervalInMinutes")
    def retry_interval_in_minutes(self) -> pulumi.Input[int]:
        """
        The number of minutes to wait to retry sending engagement in the case the engagement initially fails.
        """
        return pulumi.get(self, "retry_interval_in_minutes")

    @retry_interval_in_minutes.setter
    def retry_interval_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "retry_interval_in_minutes", value)


if not MYPY:
    class ContactStageArgsDict(TypedDict):
        """
        A set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.
        """
        duration_in_minutes: NotRequired[pulumi.Input[int]]
        """
        The time to wait until beginning the next stage.
        """
        rotation_ids: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        List of Rotation Ids to associate with Contact
        """
        targets: NotRequired[pulumi.Input[Sequence[pulumi.Input['ContactTargetsArgsDict']]]]
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
elif False:
    ContactStageArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ContactStageArgs:
    def __init__(__self__, *,
                 duration_in_minutes: Optional[pulumi.Input[int]] = None,
                 rotation_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['ContactTargetsArgs']]]] = None):
        """
        A set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.
        :param pulumi.Input[int] duration_in_minutes: The time to wait until beginning the next stage.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] rotation_ids: List of Rotation Ids to associate with Contact
        :param pulumi.Input[Sequence[pulumi.Input['ContactTargetsArgs']]] targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
        if duration_in_minutes is not None:
            pulumi.set(__self__, "duration_in_minutes", duration_in_minutes)
        if rotation_ids is not None:
            pulumi.set(__self__, "rotation_ids", rotation_ids)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)

    @property
    @pulumi.getter(name="durationInMinutes")
    def duration_in_minutes(self) -> Optional[pulumi.Input[int]]:
        """
        The time to wait until beginning the next stage.
        """
        return pulumi.get(self, "duration_in_minutes")

    @duration_in_minutes.setter
    def duration_in_minutes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "duration_in_minutes", value)

    @property
    @pulumi.getter(name="rotationIds")
    def rotation_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Rotation Ids to associate with Contact
        """
        return pulumi.get(self, "rotation_ids")

    @rotation_ids.setter
    def rotation_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "rotation_ids", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ContactTargetsArgs']]]]:
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ContactTargetsArgs']]]]):
        pulumi.set(self, "targets", value)


if not MYPY:
    class ContactTargetInfoArgsDict(TypedDict):
        """
        The contact that SSM Incident Manager is engaging during an incident.
        """
        contact_id: pulumi.Input[str]
        """
        The Amazon Resource Name (ARN) of the contact.
        """
        is_essential: pulumi.Input[bool]
        """
        A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.
        """
elif False:
    ContactTargetInfoArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ContactTargetInfoArgs:
    def __init__(__self__, *,
                 contact_id: pulumi.Input[str],
                 is_essential: pulumi.Input[bool]):
        """
        The contact that SSM Incident Manager is engaging during an incident.
        :param pulumi.Input[str] contact_id: The Amazon Resource Name (ARN) of the contact.
        :param pulumi.Input[bool] is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.
        """
        pulumi.set(__self__, "contact_id", contact_id)
        pulumi.set(__self__, "is_essential", is_essential)

    @property
    @pulumi.getter(name="contactId")
    def contact_id(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the contact.
        """
        return pulumi.get(self, "contact_id")

    @contact_id.setter
    def contact_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "contact_id", value)

    @property
    @pulumi.getter(name="isEssential")
    def is_essential(self) -> pulumi.Input[bool]:
        """
        A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.
        """
        return pulumi.get(self, "is_essential")

    @is_essential.setter
    def is_essential(self, value: pulumi.Input[bool]):
        pulumi.set(self, "is_essential", value)


if not MYPY:
    class ContactTargetsArgsDict(TypedDict):
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
        channel_target_info: NotRequired[pulumi.Input['ContactChannelTargetInfoArgsDict']]
        """
        Information about the contact channel that Incident Manager engages.
        """
        contact_target_info: NotRequired[pulumi.Input['ContactTargetInfoArgsDict']]
        """
        The contact that Incident Manager is engaging during an incident.
        """
elif False:
    ContactTargetsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ContactTargetsArgs:
    def __init__(__self__, *,
                 channel_target_info: Optional[pulumi.Input['ContactChannelTargetInfoArgs']] = None,
                 contact_target_info: Optional[pulumi.Input['ContactTargetInfoArgs']] = None):
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        :param pulumi.Input['ContactChannelTargetInfoArgs'] channel_target_info: Information about the contact channel that Incident Manager engages.
        :param pulumi.Input['ContactTargetInfoArgs'] contact_target_info: The contact that Incident Manager is engaging during an incident.
        """
        if channel_target_info is not None:
            pulumi.set(__self__, "channel_target_info", channel_target_info)
        if contact_target_info is not None:
            pulumi.set(__self__, "contact_target_info", contact_target_info)

    @property
    @pulumi.getter(name="channelTargetInfo")
    def channel_target_info(self) -> Optional[pulumi.Input['ContactChannelTargetInfoArgs']]:
        """
        Information about the contact channel that Incident Manager engages.
        """
        return pulumi.get(self, "channel_target_info")

    @channel_target_info.setter
    def channel_target_info(self, value: Optional[pulumi.Input['ContactChannelTargetInfoArgs']]):
        pulumi.set(self, "channel_target_info", value)

    @property
    @pulumi.getter(name="contactTargetInfo")
    def contact_target_info(self) -> Optional[pulumi.Input['ContactTargetInfoArgs']]:
        """
        The contact that Incident Manager is engaging during an incident.
        """
        return pulumi.get(self, "contact_target_info")

    @contact_target_info.setter
    def contact_target_info(self, value: Optional[pulumi.Input['ContactTargetInfoArgs']]):
        pulumi.set(self, "contact_target_info", value)


if not MYPY:
    class PlanChannelTargetInfoArgsDict(TypedDict):
        """
        Information about the contact channel that SSM Incident Manager uses to engage the contact.
        """
        channel_id: pulumi.Input[str]
        """
        The Amazon Resource Name (ARN) of the contact channel.
        """
        retry_interval_in_minutes: pulumi.Input[int]
        """
        The number of minutes to wait to retry sending engagement in the case the engagement initially fails.
        """
elif False:
    PlanChannelTargetInfoArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PlanChannelTargetInfoArgs:
    def __init__(__self__, *,
                 channel_id: pulumi.Input[str],
                 retry_interval_in_minutes: pulumi.Input[int]):
        """
        Information about the contact channel that SSM Incident Manager uses to engage the contact.
        :param pulumi.Input[str] channel_id: The Amazon Resource Name (ARN) of the contact channel.
        :param pulumi.Input[int] retry_interval_in_minutes: The number of minutes to wait to retry sending engagement in the case the engagement initially fails.
        """
        pulumi.set(__self__, "channel_id", channel_id)
        pulumi.set(__self__, "retry_interval_in_minutes", retry_interval_in_minutes)

    @property
    @pulumi.getter(name="channelId")
    def channel_id(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the contact channel.
        """
        return pulumi.get(self, "channel_id")

    @channel_id.setter
    def channel_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "channel_id", value)

    @property
    @pulumi.getter(name="retryIntervalInMinutes")
    def retry_interval_in_minutes(self) -> pulumi.Input[int]:
        """
        The number of minutes to wait to retry sending engagement in the case the engagement initially fails.
        """
        return pulumi.get(self, "retry_interval_in_minutes")

    @retry_interval_in_minutes.setter
    def retry_interval_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "retry_interval_in_minutes", value)


if not MYPY:
    class PlanContactTargetInfoArgsDict(TypedDict):
        """
        The contact that SSM Incident Manager is engaging during an incident.
        """
        contact_id: pulumi.Input[str]
        """
        The Amazon Resource Name (ARN) of the contact.
        """
        is_essential: pulumi.Input[bool]
        """
        A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.
        """
elif False:
    PlanContactTargetInfoArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PlanContactTargetInfoArgs:
    def __init__(__self__, *,
                 contact_id: pulumi.Input[str],
                 is_essential: pulumi.Input[bool]):
        """
        The contact that SSM Incident Manager is engaging during an incident.
        :param pulumi.Input[str] contact_id: The Amazon Resource Name (ARN) of the contact.
        :param pulumi.Input[bool] is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.
        """
        pulumi.set(__self__, "contact_id", contact_id)
        pulumi.set(__self__, "is_essential", is_essential)

    @property
    @pulumi.getter(name="contactId")
    def contact_id(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the contact.
        """
        return pulumi.get(self, "contact_id")

    @contact_id.setter
    def contact_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "contact_id", value)

    @property
    @pulumi.getter(name="isEssential")
    def is_essential(self) -> pulumi.Input[bool]:
        """
        A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.
        """
        return pulumi.get(self, "is_essential")

    @is_essential.setter
    def is_essential(self, value: pulumi.Input[bool]):
        pulumi.set(self, "is_essential", value)


if not MYPY:
    class PlanStageArgsDict(TypedDict):
        """
        A set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.
        """
        duration_in_minutes: pulumi.Input[int]
        """
        The time to wait until beginning the next stage.
        """
        targets: NotRequired[pulumi.Input[Sequence[pulumi.Input['PlanTargetsArgsDict']]]]
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
elif False:
    PlanStageArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PlanStageArgs:
    def __init__(__self__, *,
                 duration_in_minutes: pulumi.Input[int],
                 targets: Optional[pulumi.Input[Sequence[pulumi.Input['PlanTargetsArgs']]]] = None):
        """
        A set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.
        :param pulumi.Input[int] duration_in_minutes: The time to wait until beginning the next stage.
        :param pulumi.Input[Sequence[pulumi.Input['PlanTargetsArgs']]] targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
        pulumi.set(__self__, "duration_in_minutes", duration_in_minutes)
        if targets is not None:
            pulumi.set(__self__, "targets", targets)

    @property
    @pulumi.getter(name="durationInMinutes")
    def duration_in_minutes(self) -> pulumi.Input[int]:
        """
        The time to wait until beginning the next stage.
        """
        return pulumi.get(self, "duration_in_minutes")

    @duration_in_minutes.setter
    def duration_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "duration_in_minutes", value)

    @property
    @pulumi.getter
    def targets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PlanTargetsArgs']]]]:
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
        return pulumi.get(self, "targets")

    @targets.setter
    def targets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PlanTargetsArgs']]]]):
        pulumi.set(self, "targets", value)


if not MYPY:
    class PlanTargetsArgsDict(TypedDict):
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        """
        channel_target_info: NotRequired[pulumi.Input['PlanChannelTargetInfoArgsDict']]
        """
        Information about the contact channel that Incident Manager engages.
        """
        contact_target_info: NotRequired[pulumi.Input['PlanContactTargetInfoArgsDict']]
        """
        Information about the contact that Incident Manager engages.
        """
elif False:
    PlanTargetsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PlanTargetsArgs:
    def __init__(__self__, *,
                 channel_target_info: Optional[pulumi.Input['PlanChannelTargetInfoArgs']] = None,
                 contact_target_info: Optional[pulumi.Input['PlanContactTargetInfoArgs']] = None):
        """
        The contacts or contact methods that the escalation plan or engagement plan is engaging.
        :param pulumi.Input['PlanChannelTargetInfoArgs'] channel_target_info: Information about the contact channel that Incident Manager engages.
        :param pulumi.Input['PlanContactTargetInfoArgs'] contact_target_info: Information about the contact that Incident Manager engages.
        """
        if channel_target_info is not None:
            pulumi.set(__self__, "channel_target_info", channel_target_info)
        if contact_target_info is not None:
            pulumi.set(__self__, "contact_target_info", contact_target_info)

    @property
    @pulumi.getter(name="channelTargetInfo")
    def channel_target_info(self) -> Optional[pulumi.Input['PlanChannelTargetInfoArgs']]:
        """
        Information about the contact channel that Incident Manager engages.
        """
        return pulumi.get(self, "channel_target_info")

    @channel_target_info.setter
    def channel_target_info(self, value: Optional[pulumi.Input['PlanChannelTargetInfoArgs']]):
        pulumi.set(self, "channel_target_info", value)

    @property
    @pulumi.getter(name="contactTargetInfo")
    def contact_target_info(self) -> Optional[pulumi.Input['PlanContactTargetInfoArgs']]:
        """
        Information about the contact that Incident Manager engages.
        """
        return pulumi.get(self, "contact_target_info")

    @contact_target_info.setter
    def contact_target_info(self, value: Optional[pulumi.Input['PlanContactTargetInfoArgs']]):
        pulumi.set(self, "contact_target_info", value)


if not MYPY:
    class RotationCoverageTimeArgsDict(TypedDict):
        """
        StartTime and EndTime for the Shift
        """
        end_time: pulumi.Input[str]
        """
        Information about when an on-call rotation shift ends.
        """
        start_time: pulumi.Input[str]
        """
        Information about when an on-call rotation shift begins.
        """
elif False:
    RotationCoverageTimeArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class RotationCoverageTimeArgs:
    def __init__(__self__, *,
                 end_time: pulumi.Input[str],
                 start_time: pulumi.Input[str]):
        """
        StartTime and EndTime for the Shift
        :param pulumi.Input[str] end_time: Information about when an on-call rotation shift ends.
        :param pulumi.Input[str] start_time: Information about when an on-call rotation shift begins.
        """
        pulumi.set(__self__, "end_time", end_time)
        pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Input[str]:
        """
        Information about when an on-call rotation shift ends.
        """
        return pulumi.get(self, "end_time")

    @end_time.setter
    def end_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "end_time", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Input[str]:
        """
        Information about when an on-call rotation shift begins.
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "start_time", value)


if not MYPY:
    class RotationMonthlySettingArgsDict(TypedDict):
        """
        DayOfWeek for Month and HandOff Time for Monthly Recurring Rotation.
        """
        day_of_month: pulumi.Input[int]
        """
        The day of the month when monthly recurring on-call rotations begin.
        """
        hand_off_time: pulumi.Input[str]
        """
        The time of day when a monthly recurring on-call shift rotation begins.
        """
elif False:
    RotationMonthlySettingArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class RotationMonthlySettingArgs:
    def __init__(__self__, *,
                 day_of_month: pulumi.Input[int],
                 hand_off_time: pulumi.Input[str]):
        """
        DayOfWeek for Month and HandOff Time for Monthly Recurring Rotation.
        :param pulumi.Input[int] day_of_month: The day of the month when monthly recurring on-call rotations begin.
        :param pulumi.Input[str] hand_off_time: The time of day when a monthly recurring on-call shift rotation begins.
        """
        pulumi.set(__self__, "day_of_month", day_of_month)
        pulumi.set(__self__, "hand_off_time", hand_off_time)

    @property
    @pulumi.getter(name="dayOfMonth")
    def day_of_month(self) -> pulumi.Input[int]:
        """
        The day of the month when monthly recurring on-call rotations begin.
        """
        return pulumi.get(self, "day_of_month")

    @day_of_month.setter
    def day_of_month(self, value: pulumi.Input[int]):
        pulumi.set(self, "day_of_month", value)

    @property
    @pulumi.getter(name="handOffTime")
    def hand_off_time(self) -> pulumi.Input[str]:
        """
        The time of day when a monthly recurring on-call shift rotation begins.
        """
        return pulumi.get(self, "hand_off_time")

    @hand_off_time.setter
    def hand_off_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "hand_off_time", value)


if not MYPY:
    class RotationRecurrenceSettingsArgsDict(TypedDict):
        """
        Information about when an on-call rotation is in effect and how long the rotation period lasts.
        """
        daily_settings: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Information about on-call rotations that recur daily.
        """
        monthly_settings: NotRequired[pulumi.Input[Sequence[pulumi.Input['RotationMonthlySettingArgsDict']]]]
        """
        Information about on-call rotations that recur monthly.
        """
        number_of_on_calls: NotRequired[pulumi.Input[int]]
        """
        Number of Oncalls per shift.
        """
        recurrence_multiplier: NotRequired[pulumi.Input[int]]
        """
        The number of days, weeks, or months a single rotation lasts.
        """
        shift_coverages: NotRequired[pulumi.Input[Sequence[pulumi.Input['RotationShiftCoverageArgsDict']]]]
        """
        Information about the days of the week included in on-call rotation coverage.
        """
        weekly_settings: NotRequired[pulumi.Input[Sequence[pulumi.Input['RotationWeeklySettingArgsDict']]]]
        """
        Information about on-call rotations that recur weekly.
        """
elif False:
    RotationRecurrenceSettingsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class RotationRecurrenceSettingsArgs:
    def __init__(__self__, *,
                 daily_settings: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 monthly_settings: Optional[pulumi.Input[Sequence[pulumi.Input['RotationMonthlySettingArgs']]]] = None,
                 number_of_on_calls: Optional[pulumi.Input[int]] = None,
                 recurrence_multiplier: Optional[pulumi.Input[int]] = None,
                 shift_coverages: Optional[pulumi.Input[Sequence[pulumi.Input['RotationShiftCoverageArgs']]]] = None,
                 weekly_settings: Optional[pulumi.Input[Sequence[pulumi.Input['RotationWeeklySettingArgs']]]] = None):
        """
        Information about when an on-call rotation is in effect and how long the rotation period lasts.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] daily_settings: Information about on-call rotations that recur daily.
        :param pulumi.Input[Sequence[pulumi.Input['RotationMonthlySettingArgs']]] monthly_settings: Information about on-call rotations that recur monthly.
        :param pulumi.Input[int] number_of_on_calls: Number of Oncalls per shift.
        :param pulumi.Input[int] recurrence_multiplier: The number of days, weeks, or months a single rotation lasts.
        :param pulumi.Input[Sequence[pulumi.Input['RotationShiftCoverageArgs']]] shift_coverages: Information about the days of the week included in on-call rotation coverage.
        :param pulumi.Input[Sequence[pulumi.Input['RotationWeeklySettingArgs']]] weekly_settings: Information about on-call rotations that recur weekly.
        """
        if daily_settings is not None:
            pulumi.set(__self__, "daily_settings", daily_settings)
        if monthly_settings is not None:
            pulumi.set(__self__, "monthly_settings", monthly_settings)
        if number_of_on_calls is not None:
            pulumi.set(__self__, "number_of_on_calls", number_of_on_calls)
        if recurrence_multiplier is not None:
            pulumi.set(__self__, "recurrence_multiplier", recurrence_multiplier)
        if shift_coverages is not None:
            pulumi.set(__self__, "shift_coverages", shift_coverages)
        if weekly_settings is not None:
            pulumi.set(__self__, "weekly_settings", weekly_settings)

    @property
    @pulumi.getter(name="dailySettings")
    def daily_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Information about on-call rotations that recur daily.
        """
        return pulumi.get(self, "daily_settings")

    @daily_settings.setter
    def daily_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "daily_settings", value)

    @property
    @pulumi.getter(name="monthlySettings")
    def monthly_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RotationMonthlySettingArgs']]]]:
        """
        Information about on-call rotations that recur monthly.
        """
        return pulumi.get(self, "monthly_settings")

    @monthly_settings.setter
    def monthly_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RotationMonthlySettingArgs']]]]):
        pulumi.set(self, "monthly_settings", value)

    @property
    @pulumi.getter(name="numberOfOnCalls")
    def number_of_on_calls(self) -> Optional[pulumi.Input[int]]:
        """
        Number of Oncalls per shift.
        """
        return pulumi.get(self, "number_of_on_calls")

    @number_of_on_calls.setter
    def number_of_on_calls(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "number_of_on_calls", value)

    @property
    @pulumi.getter(name="recurrenceMultiplier")
    def recurrence_multiplier(self) -> Optional[pulumi.Input[int]]:
        """
        The number of days, weeks, or months a single rotation lasts.
        """
        return pulumi.get(self, "recurrence_multiplier")

    @recurrence_multiplier.setter
    def recurrence_multiplier(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "recurrence_multiplier", value)

    @property
    @pulumi.getter(name="shiftCoverages")
    def shift_coverages(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RotationShiftCoverageArgs']]]]:
        """
        Information about the days of the week included in on-call rotation coverage.
        """
        return pulumi.get(self, "shift_coverages")

    @shift_coverages.setter
    def shift_coverages(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RotationShiftCoverageArgs']]]]):
        pulumi.set(self, "shift_coverages", value)

    @property
    @pulumi.getter(name="weeklySettings")
    def weekly_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RotationWeeklySettingArgs']]]]:
        """
        Information about on-call rotations that recur weekly.
        """
        return pulumi.get(self, "weekly_settings")

    @weekly_settings.setter
    def weekly_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RotationWeeklySettingArgs']]]]):
        pulumi.set(self, "weekly_settings", value)


if not MYPY:
    class RotationShiftCoverageArgsDict(TypedDict):
        """
        Information about the days of the week included in on-call rotation coverage.
        """
        coverage_times: pulumi.Input[Sequence[pulumi.Input['RotationCoverageTimeArgsDict']]]
        """
        Information about when an on-call shift begins and ends.
        """
        day_of_week: pulumi.Input['RotationDayOfWeek']
        """
        A list of days on which the schedule is active.
        """
elif False:
    RotationShiftCoverageArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class RotationShiftCoverageArgs:
    def __init__(__self__, *,
                 coverage_times: pulumi.Input[Sequence[pulumi.Input['RotationCoverageTimeArgs']]],
                 day_of_week: pulumi.Input['RotationDayOfWeek']):
        """
        Information about the days of the week included in on-call rotation coverage.
        :param pulumi.Input[Sequence[pulumi.Input['RotationCoverageTimeArgs']]] coverage_times: Information about when an on-call shift begins and ends.
        :param pulumi.Input['RotationDayOfWeek'] day_of_week: A list of days on which the schedule is active.
        """
        pulumi.set(__self__, "coverage_times", coverage_times)
        pulumi.set(__self__, "day_of_week", day_of_week)

    @property
    @pulumi.getter(name="coverageTimes")
    def coverage_times(self) -> pulumi.Input[Sequence[pulumi.Input['RotationCoverageTimeArgs']]]:
        """
        Information about when an on-call shift begins and ends.
        """
        return pulumi.get(self, "coverage_times")

    @coverage_times.setter
    def coverage_times(self, value: pulumi.Input[Sequence[pulumi.Input['RotationCoverageTimeArgs']]]):
        pulumi.set(self, "coverage_times", value)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> pulumi.Input['RotationDayOfWeek']:
        """
        A list of days on which the schedule is active.
        """
        return pulumi.get(self, "day_of_week")

    @day_of_week.setter
    def day_of_week(self, value: pulumi.Input['RotationDayOfWeek']):
        pulumi.set(self, "day_of_week", value)


if not MYPY:
    class RotationWeeklySettingArgsDict(TypedDict):
        """
        DayOfWeek for Rotation and HandOff Time for Weekly Recurring Rotation.
        """
        day_of_week: pulumi.Input['RotationDayOfWeek']
        """
        The day of the week when weekly recurring on-call shift rotations begins.
        """
        hand_off_time: pulumi.Input[str]
        """
        The time of day when a weekly recurring on-call shift rotation begins.
        """
elif False:
    RotationWeeklySettingArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class RotationWeeklySettingArgs:
    def __init__(__self__, *,
                 day_of_week: pulumi.Input['RotationDayOfWeek'],
                 hand_off_time: pulumi.Input[str]):
        """
        DayOfWeek for Rotation and HandOff Time for Weekly Recurring Rotation.
        :param pulumi.Input['RotationDayOfWeek'] day_of_week: The day of the week when weekly recurring on-call shift rotations begins.
        :param pulumi.Input[str] hand_off_time: The time of day when a weekly recurring on-call shift rotation begins.
        """
        pulumi.set(__self__, "day_of_week", day_of_week)
        pulumi.set(__self__, "hand_off_time", hand_off_time)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> pulumi.Input['RotationDayOfWeek']:
        """
        The day of the week when weekly recurring on-call shift rotations begins.
        """
        return pulumi.get(self, "day_of_week")

    @day_of_week.setter
    def day_of_week(self, value: pulumi.Input['RotationDayOfWeek']):
        pulumi.set(self, "day_of_week", value)

    @property
    @pulumi.getter(name="handOffTime")
    def hand_off_time(self) -> pulumi.Input[str]:
        """
        The time of day when a weekly recurring on-call shift rotation begins.
        """
        return pulumi.get(self, "hand_off_time")

    @hand_off_time.setter
    def hand_off_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "hand_off_time", value)


