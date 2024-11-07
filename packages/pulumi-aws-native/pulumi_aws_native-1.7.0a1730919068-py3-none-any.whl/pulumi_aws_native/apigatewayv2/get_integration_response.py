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

__all__ = [
    'GetIntegrationResponseResult',
    'AwaitableGetIntegrationResponseResult',
    'get_integration_response',
    'get_integration_response_output',
]

@pulumi.output_type
class GetIntegrationResponseResult:
    def __init__(__self__, content_handling_strategy=None, integration_response_id=None, integration_response_key=None, response_parameters=None, response_templates=None, template_selection_expression=None):
        if content_handling_strategy and not isinstance(content_handling_strategy, str):
            raise TypeError("Expected argument 'content_handling_strategy' to be a str")
        pulumi.set(__self__, "content_handling_strategy", content_handling_strategy)
        if integration_response_id and not isinstance(integration_response_id, str):
            raise TypeError("Expected argument 'integration_response_id' to be a str")
        pulumi.set(__self__, "integration_response_id", integration_response_id)
        if integration_response_key and not isinstance(integration_response_key, str):
            raise TypeError("Expected argument 'integration_response_key' to be a str")
        pulumi.set(__self__, "integration_response_key", integration_response_key)
        if response_parameters and not isinstance(response_parameters, dict):
            raise TypeError("Expected argument 'response_parameters' to be a dict")
        pulumi.set(__self__, "response_parameters", response_parameters)
        if response_templates and not isinstance(response_templates, dict):
            raise TypeError("Expected argument 'response_templates' to be a dict")
        pulumi.set(__self__, "response_templates", response_templates)
        if template_selection_expression and not isinstance(template_selection_expression, str):
            raise TypeError("Expected argument 'template_selection_expression' to be a str")
        pulumi.set(__self__, "template_selection_expression", template_selection_expression)

    @property
    @pulumi.getter(name="contentHandlingStrategy")
    def content_handling_strategy(self) -> Optional[str]:
        """
        Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT``, with the following behaviors:
          ``CONVERT_TO_BINARY``: Converts a response payload from a Base64-encoded string to the corresponding binary blob.
          ``CONVERT_TO_TEXT``: Converts a response payload from a binary blob to a Base64-encoded string.
         If this property is not defined, the response payload will be passed through from the integration response to the route response or method response without modification.
        """
        return pulumi.get(self, "content_handling_strategy")

    @property
    @pulumi.getter(name="integrationResponseId")
    def integration_response_id(self) -> Optional[str]:
        """
        The integration response ID.
        """
        return pulumi.get(self, "integration_response_id")

    @property
    @pulumi.getter(name="integrationResponseKey")
    def integration_response_key(self) -> Optional[str]:
        """
        The integration response key.
        """
        return pulumi.get(self, "integration_response_key")

    @property
    @pulumi.getter(name="responseParameters")
    def response_parameters(self) -> Optional[Any]:
        """
        A key-value map specifying response parameters that are passed to the method response from the backend. The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header.{name}``, where name is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header.{name}`` or ``integration.response.body.{JSON-expression}``, where ``{name}`` is a valid and unique response header name and ``{JSON-expression}`` is a valid JSON expression without the ``$`` prefix.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ApiGatewayV2::IntegrationResponse` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "response_parameters")

    @property
    @pulumi.getter(name="responseTemplates")
    def response_templates(self) -> Optional[Any]:
        """
        The collection of response templates for the integration response as a string-to-string map of key-value pairs. Response templates are represented as a key/value map, with a content-type as the key and a template as the value.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::ApiGatewayV2::IntegrationResponse` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "response_templates")

    @property
    @pulumi.getter(name="templateSelectionExpression")
    def template_selection_expression(self) -> Optional[str]:
        """
        The template selection expression for the integration response. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "template_selection_expression")


class AwaitableGetIntegrationResponseResult(GetIntegrationResponseResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIntegrationResponseResult(
            content_handling_strategy=self.content_handling_strategy,
            integration_response_id=self.integration_response_id,
            integration_response_key=self.integration_response_key,
            response_parameters=self.response_parameters,
            response_templates=self.response_templates,
            template_selection_expression=self.template_selection_expression)


def get_integration_response(api_id: Optional[str] = None,
                             integration_id: Optional[str] = None,
                             integration_response_id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIntegrationResponseResult:
    """
    The ``AWS::ApiGatewayV2::IntegrationResponse`` resource updates an integration response for an WebSocket API. For more information, see [Set up WebSocket API Integration Responses in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-integration-responses.html) in the *API Gateway Developer Guide*.


    :param str api_id: The API identifier.
    :param str integration_id: The integration ID.
    :param str integration_response_id: The integration response ID.
    """
    __args__ = dict()
    __args__['apiId'] = api_id
    __args__['integrationId'] = integration_id
    __args__['integrationResponseId'] = integration_response_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:apigatewayv2:getIntegrationResponse', __args__, opts=opts, typ=GetIntegrationResponseResult).value

    return AwaitableGetIntegrationResponseResult(
        content_handling_strategy=pulumi.get(__ret__, 'content_handling_strategy'),
        integration_response_id=pulumi.get(__ret__, 'integration_response_id'),
        integration_response_key=pulumi.get(__ret__, 'integration_response_key'),
        response_parameters=pulumi.get(__ret__, 'response_parameters'),
        response_templates=pulumi.get(__ret__, 'response_templates'),
        template_selection_expression=pulumi.get(__ret__, 'template_selection_expression'))
def get_integration_response_output(api_id: Optional[pulumi.Input[str]] = None,
                                    integration_id: Optional[pulumi.Input[str]] = None,
                                    integration_response_id: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIntegrationResponseResult]:
    """
    The ``AWS::ApiGatewayV2::IntegrationResponse`` resource updates an integration response for an WebSocket API. For more information, see [Set up WebSocket API Integration Responses in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-integration-responses.html) in the *API Gateway Developer Guide*.


    :param str api_id: The API identifier.
    :param str integration_id: The integration ID.
    :param str integration_response_id: The integration response ID.
    """
    __args__ = dict()
    __args__['apiId'] = api_id
    __args__['integrationId'] = integration_id
    __args__['integrationResponseId'] = integration_response_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:apigatewayv2:getIntegrationResponse', __args__, opts=opts, typ=GetIntegrationResponseResult)
    return __ret__.apply(lambda __response__: GetIntegrationResponseResult(
        content_handling_strategy=pulumi.get(__response__, 'content_handling_strategy'),
        integration_response_id=pulumi.get(__response__, 'integration_response_id'),
        integration_response_key=pulumi.get(__response__, 'integration_response_key'),
        response_parameters=pulumi.get(__response__, 'response_parameters'),
        response_templates=pulumi.get(__response__, 'response_templates'),
        template_selection_expression=pulumi.get(__response__, 'template_selection_expression')))
