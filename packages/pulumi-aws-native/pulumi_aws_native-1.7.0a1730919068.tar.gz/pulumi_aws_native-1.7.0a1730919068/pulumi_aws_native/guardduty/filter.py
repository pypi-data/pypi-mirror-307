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

__all__ = ['FilterArgs', 'Filter']

@pulumi.input_type
class FilterArgs:
    def __init__(__self__, *,
                 detector_id: pulumi.Input[str],
                 finding_criteria: pulumi.Input['FilterFindingCriteriaArgs'],
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rank: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None):
        """
        The set of arguments for constructing a Filter resource.
        :param pulumi.Input[str] detector_id: The detector ID associated with the GuardDuty account for which you want to create a filter.
               
               To find the `detectorId` in the current Region, see the
               Settings page in the GuardDuty console, or run the [ListDetectors](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html) API.
        :param pulumi.Input['FilterFindingCriteriaArgs'] finding_criteria: Represents the criteria to be used in the filter for querying findings.
        :param pulumi.Input[str] action: Specifies the action that is to be applied to the findings that match the filter.
        :param pulumi.Input[str] description: The description of the filter. Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( `{ }` , `[ ]` , and `( )` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.
        :param pulumi.Input[str] name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        :param pulumi.Input[int] rank: Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.
               
               By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, [DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html) , with the following syntax: `"DependsOn":[ "ObjectName" ]` .
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define.
               
               For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        pulumi.set(__self__, "detector_id", detector_id)
        pulumi.set(__self__, "finding_criteria", finding_criteria)
        if action is not None:
            pulumi.set(__self__, "action", action)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rank is not None:
            pulumi.set(__self__, "rank", rank)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> pulumi.Input[str]:
        """
        The detector ID associated with the GuardDuty account for which you want to create a filter.

        To find the `detectorId` in the current Region, see the
        Settings page in the GuardDuty console, or run the [ListDetectors](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html) API.
        """
        return pulumi.get(self, "detector_id")

    @detector_id.setter
    def detector_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "detector_id", value)

    @property
    @pulumi.getter(name="findingCriteria")
    def finding_criteria(self) -> pulumi.Input['FilterFindingCriteriaArgs']:
        """
        Represents the criteria to be used in the filter for querying findings.
        """
        return pulumi.get(self, "finding_criteria")

    @finding_criteria.setter
    def finding_criteria(self, value: pulumi.Input['FilterFindingCriteriaArgs']):
        pulumi.set(self, "finding_criteria", value)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the action that is to be applied to the findings that match the filter.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the filter. Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( `{ }` , `[ ]` , and `( )` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def rank(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.

        By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, [DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html) , with the following syntax: `"DependsOn":[ "ObjectName" ]` .
        """
        return pulumi.get(self, "rank")

    @rank.setter
    def rank(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "rank", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)


class Filter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 finding_criteria: Optional[pulumi.Input[Union['FilterFindingCriteriaArgs', 'FilterFindingCriteriaArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rank: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::GuardDuty::Filter

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: Specifies the action that is to be applied to the findings that match the filter.
        :param pulumi.Input[str] description: The description of the filter. Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( `{ }` , `[ ]` , and `( )` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.
        :param pulumi.Input[str] detector_id: The detector ID associated with the GuardDuty account for which you want to create a filter.
               
               To find the `detectorId` in the current Region, see the
               Settings page in the GuardDuty console, or run the [ListDetectors](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html) API.
        :param pulumi.Input[Union['FilterFindingCriteriaArgs', 'FilterFindingCriteriaArgsDict']] finding_criteria: Represents the criteria to be used in the filter for querying findings.
        :param pulumi.Input[str] name: The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        :param pulumi.Input[int] rank: Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.
               
               By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, [DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html) , with the following syntax: `"DependsOn":[ "ObjectName" ]` .
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define.
               
               For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FilterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::GuardDuty::Filter

        :param str resource_name: The name of the resource.
        :param FilterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FilterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 finding_criteria: Optional[pulumi.Input[Union['FilterFindingCriteriaArgs', 'FilterFindingCriteriaArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rank: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FilterArgs.__new__(FilterArgs)

            __props__.__dict__["action"] = action
            __props__.__dict__["description"] = description
            if detector_id is None and not opts.urn:
                raise TypeError("Missing required property 'detector_id'")
            __props__.__dict__["detector_id"] = detector_id
            if finding_criteria is None and not opts.urn:
                raise TypeError("Missing required property 'finding_criteria'")
            __props__.__dict__["finding_criteria"] = finding_criteria
            __props__.__dict__["name"] = name
            __props__.__dict__["rank"] = rank
            __props__.__dict__["tags"] = tags
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["detectorId", "name"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Filter, __self__).__init__(
            'aws-native:guardduty:Filter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Filter':
        """
        Get an existing Filter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FilterArgs.__new__(FilterArgs)

        __props__.__dict__["action"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["detector_id"] = None
        __props__.__dict__["finding_criteria"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["rank"] = None
        __props__.__dict__["tags"] = None
        return Filter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the action that is to be applied to the findings that match the filter.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the filter. Valid characters include alphanumeric characters, and special characters such as hyphen, period, colon, underscore, parentheses ( `{ }` , `[ ]` , and `( )` ), forward slash, horizontal tab, vertical tab, newline, form feed, return, and whitespace.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> pulumi.Output[str]:
        """
        The detector ID associated with the GuardDuty account for which you want to create a filter.

        To find the `detectorId` in the current Region, see the
        Settings page in the GuardDuty console, or run the [ListDetectors](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html) API.
        """
        return pulumi.get(self, "detector_id")

    @property
    @pulumi.getter(name="findingCriteria")
    def finding_criteria(self) -> pulumi.Output['outputs.FilterFindingCriteria']:
        """
        Represents the criteria to be used in the filter for querying findings.
        """
        return pulumi.get(self, "finding_criteria")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the filter. Valid characters include period (.), underscore (_), dash (-), and alphanumeric characters. A whitespace is considered to be an invalid character.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rank(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the position of the filter in the list of current filters. Also specifies the order in which this filter is applied to the findings. The minimum value for this property is 1 and the maximum is 100.

        By default, filters may not be created in the same order as they are ranked. To ensure that the filters are created in the expected order, you can use an optional attribute, [DependsOn](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html) , with the following syntax: `"DependsOn":[ "ObjectName" ]` .
        """
        return pulumi.get(self, "rank")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        The tags to be added to a new filter resource. Each tag consists of a key and an optional value, both of which you define.

        For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html) .
        """
        return pulumi.get(self, "tags")

