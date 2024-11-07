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
    'GetInputResult',
    'AwaitableGetInputResult',
    'get_input',
    'get_input_output',
]

@pulumi.output_type
class GetInputResult:
    def __init__(__self__, input_definition=None, input_description=None, tags=None):
        if input_definition and not isinstance(input_definition, dict):
            raise TypeError("Expected argument 'input_definition' to be a dict")
        pulumi.set(__self__, "input_definition", input_definition)
        if input_description and not isinstance(input_description, str):
            raise TypeError("Expected argument 'input_description' to be a str")
        pulumi.set(__self__, "input_description", input_description)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="inputDefinition")
    def input_definition(self) -> Optional['outputs.InputDefinition']:
        """
        The definition of the input.
        """
        return pulumi.get(self, "input_definition")

    @property
    @pulumi.getter(name="inputDescription")
    def input_description(self) -> Optional[str]:
        """
        A brief description of the input.
        """
        return pulumi.get(self, "input_description")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
         For more information, see [Tag](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html).
        """
        return pulumi.get(self, "tags")


class AwaitableGetInputResult(GetInputResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInputResult(
            input_definition=self.input_definition,
            input_description=self.input_description,
            tags=self.tags)


def get_input(input_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInputResult:
    """
    The AWS::IoTEvents::Input resource creates an input. To monitor your devices and processes, they must have a way to get telemetry data into ITE. This is done by sending messages as *inputs* to ITE. For more information, see [How to Use](https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html) in the *Developer Guide*.


    :param str input_name: The name of the input.
    """
    __args__ = dict()
    __args__['inputName'] = input_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iotevents:getInput', __args__, opts=opts, typ=GetInputResult).value

    return AwaitableGetInputResult(
        input_definition=pulumi.get(__ret__, 'input_definition'),
        input_description=pulumi.get(__ret__, 'input_description'),
        tags=pulumi.get(__ret__, 'tags'))
def get_input_output(input_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInputResult]:
    """
    The AWS::IoTEvents::Input resource creates an input. To monitor your devices and processes, they must have a way to get telemetry data into ITE. This is done by sending messages as *inputs* to ITE. For more information, see [How to Use](https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html) in the *Developer Guide*.


    :param str input_name: The name of the input.
    """
    __args__ = dict()
    __args__['inputName'] = input_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iotevents:getInput', __args__, opts=opts, typ=GetInputResult)
    return __ret__.apply(lambda __response__: GetInputResult(
        input_definition=pulumi.get(__response__, 'input_definition'),
        input_description=pulumi.get(__response__, 'input_description'),
        tags=pulumi.get(__response__, 'tags')))
