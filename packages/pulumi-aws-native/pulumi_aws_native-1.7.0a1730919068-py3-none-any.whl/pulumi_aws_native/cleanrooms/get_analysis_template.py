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
    'GetAnalysisTemplateResult',
    'AwaitableGetAnalysisTemplateResult',
    'get_analysis_template',
    'get_analysis_template_output',
]

@pulumi.output_type
class GetAnalysisTemplateResult:
    def __init__(__self__, analysis_template_identifier=None, arn=None, collaboration_arn=None, collaboration_identifier=None, description=None, membership_arn=None, schema=None, tags=None):
        if analysis_template_identifier and not isinstance(analysis_template_identifier, str):
            raise TypeError("Expected argument 'analysis_template_identifier' to be a str")
        pulumi.set(__self__, "analysis_template_identifier", analysis_template_identifier)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if collaboration_arn and not isinstance(collaboration_arn, str):
            raise TypeError("Expected argument 'collaboration_arn' to be a str")
        pulumi.set(__self__, "collaboration_arn", collaboration_arn)
        if collaboration_identifier and not isinstance(collaboration_identifier, str):
            raise TypeError("Expected argument 'collaboration_identifier' to be a str")
        pulumi.set(__self__, "collaboration_identifier", collaboration_identifier)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if membership_arn and not isinstance(membership_arn, str):
            raise TypeError("Expected argument 'membership_arn' to be a str")
        pulumi.set(__self__, "membership_arn", membership_arn)
        if schema and not isinstance(schema, dict):
            raise TypeError("Expected argument 'schema' to be a dict")
        pulumi.set(__self__, "schema", schema)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="analysisTemplateIdentifier")
    def analysis_template_identifier(self) -> Optional[str]:
        """
        Returns the identifier for the analysis template.

        Example: `a1b2c3d4-5678-90ab-cdef-EXAMPLE2222`
        """
        return pulumi.get(self, "analysis_template_identifier")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Returns the Amazon Resource Name (ARN) of the analysis template.

        Example: `arn:aws:cleanrooms:us-east-1:111122223333:membership/a1b2c3d4-5678-90ab-cdef-EXAMPLE11111/analysistemplates/a1b2c3d4-5678-90ab-cdef-EXAMPLE2222`
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="collaborationArn")
    def collaboration_arn(self) -> Optional[str]:
        """
        Returns the unique ARN for the analysis template’s associated collaboration.

        Example: `arn:aws:cleanrooms:us-east-1:111122223333:collaboration/a1b2c3d4-5678-90ab-cdef-EXAMPLE33333`
        """
        return pulumi.get(self, "collaboration_arn")

    @property
    @pulumi.getter(name="collaborationIdentifier")
    def collaboration_identifier(self) -> Optional[str]:
        """
        Returns the unique ID for the associated collaboration of the analysis template.

        Example: `a1b2c3d4-5678-90ab-cdef-EXAMPLE33333`
        """
        return pulumi.get(self, "collaboration_identifier")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the analysis template.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="membershipArn")
    def membership_arn(self) -> Optional[str]:
        """
        Returns the Amazon Resource Name (ARN) of the member who created the analysis template.

        Example: `arn:aws:cleanrooms:us-east-1:111122223333:membership/a1b2c3d4-5678-90ab-cdef-EXAMPLE11111`
        """
        return pulumi.get(self, "membership_arn")

    @property
    @pulumi.getter
    def schema(self) -> Optional['outputs.AnalysisTemplateAnalysisSchema']:
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An arbitrary set of tags (key-value pairs) for this cleanrooms analysis template.
        """
        return pulumi.get(self, "tags")


class AwaitableGetAnalysisTemplateResult(GetAnalysisTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAnalysisTemplateResult(
            analysis_template_identifier=self.analysis_template_identifier,
            arn=self.arn,
            collaboration_arn=self.collaboration_arn,
            collaboration_identifier=self.collaboration_identifier,
            description=self.description,
            membership_arn=self.membership_arn,
            schema=self.schema,
            tags=self.tags)


def get_analysis_template(analysis_template_identifier: Optional[str] = None,
                          membership_identifier: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAnalysisTemplateResult:
    """
    Represents a stored analysis within a collaboration


    :param str analysis_template_identifier: Returns the identifier for the analysis template.
           
           Example: `a1b2c3d4-5678-90ab-cdef-EXAMPLE2222`
    :param str membership_identifier: The identifier for a membership resource.
    """
    __args__ = dict()
    __args__['analysisTemplateIdentifier'] = analysis_template_identifier
    __args__['membershipIdentifier'] = membership_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cleanrooms:getAnalysisTemplate', __args__, opts=opts, typ=GetAnalysisTemplateResult).value

    return AwaitableGetAnalysisTemplateResult(
        analysis_template_identifier=pulumi.get(__ret__, 'analysis_template_identifier'),
        arn=pulumi.get(__ret__, 'arn'),
        collaboration_arn=pulumi.get(__ret__, 'collaboration_arn'),
        collaboration_identifier=pulumi.get(__ret__, 'collaboration_identifier'),
        description=pulumi.get(__ret__, 'description'),
        membership_arn=pulumi.get(__ret__, 'membership_arn'),
        schema=pulumi.get(__ret__, 'schema'),
        tags=pulumi.get(__ret__, 'tags'))
def get_analysis_template_output(analysis_template_identifier: Optional[pulumi.Input[str]] = None,
                                 membership_identifier: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAnalysisTemplateResult]:
    """
    Represents a stored analysis within a collaboration


    :param str analysis_template_identifier: Returns the identifier for the analysis template.
           
           Example: `a1b2c3d4-5678-90ab-cdef-EXAMPLE2222`
    :param str membership_identifier: The identifier for a membership resource.
    """
    __args__ = dict()
    __args__['analysisTemplateIdentifier'] = analysis_template_identifier
    __args__['membershipIdentifier'] = membership_identifier
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cleanrooms:getAnalysisTemplate', __args__, opts=opts, typ=GetAnalysisTemplateResult)
    return __ret__.apply(lambda __response__: GetAnalysisTemplateResult(
        analysis_template_identifier=pulumi.get(__response__, 'analysis_template_identifier'),
        arn=pulumi.get(__response__, 'arn'),
        collaboration_arn=pulumi.get(__response__, 'collaboration_arn'),
        collaboration_identifier=pulumi.get(__response__, 'collaboration_identifier'),
        description=pulumi.get(__response__, 'description'),
        membership_arn=pulumi.get(__response__, 'membership_arn'),
        schema=pulumi.get(__response__, 'schema'),
        tags=pulumi.get(__response__, 'tags')))
