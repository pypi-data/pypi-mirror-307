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
from ._inputs import *

__all__ = ['IntegrationArgs', 'Integration']

@pulumi.input_type
class IntegrationArgs:
    def __init__(__self__, *,
                 api_id: pulumi.Input[str],
                 integration_type: pulumi.Input[str],
                 connection_id: Optional[pulumi.Input[str]] = None,
                 connection_type: Optional[pulumi.Input[str]] = None,
                 content_handling_strategy: Optional[pulumi.Input[str]] = None,
                 credentials_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 integration_method: Optional[pulumi.Input[str]] = None,
                 integration_subtype: Optional[pulumi.Input[str]] = None,
                 integration_uri: Optional[pulumi.Input[str]] = None,
                 passthrough_behavior: Optional[pulumi.Input[str]] = None,
                 payload_format_version: Optional[pulumi.Input[str]] = None,
                 request_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 request_templates: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 response_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input['IntegrationResponseParameterMapArgs']]]] = None,
                 template_selection_expression: Optional[pulumi.Input[str]] = None,
                 timeout_in_millis: Optional[pulumi.Input[int]] = None,
                 tls_config: Optional[pulumi.Input['IntegrationTlsConfigArgs']] = None):
        """
        The set of arguments for constructing a Integration resource.
        :param pulumi.Input[str] api_id: The API identifier.
        :param pulumi.Input[str] integration_type: The integration type of an integration.
        :param pulumi.Input[str] connection_id: The ID of the VPC link for a private integration. Supported only for HTTP APIs.
        :param pulumi.Input[str] connection_type: The type of the network connection to the integration endpoint. Specify INTERNET for connections through the public routable internet or VPC_LINK for private connections between API Gateway and resources in a VPC. The default value is INTERNET.
        :param pulumi.Input[str] content_handling_strategy: Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are CONVERT_TO_BINARY and CONVERT_TO_TEXT.
        :param pulumi.Input[str] credentials_arn: Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string arn:aws:iam::*:user/*. To use resource-based permissions on supported AWS services, don't specify this parameter.
        :param pulumi.Input[str] description: The description of the integration.
        :param pulumi.Input[str] integration_method: Specifies the integration's HTTP method type.
        :param pulumi.Input[str] integration_subtype: Supported only for HTTP API AWS_PROXY integrations. Specifies the AWS service action to invoke.
        :param pulumi.Input[str] integration_uri: For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration, specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service.
        :param pulumi.Input[str] passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER. Supported only for WebSocket APIs.
        :param pulumi.Input[str] payload_format_version: Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are 1.0 and 2.0 For all other integrations, 1.0 is the only supported value.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] request_parameters: A key-value map specifying parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] request_templates: A map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.
        :param pulumi.Input[Mapping[str, pulumi.Input['IntegrationResponseParameterMapArgs']]] response_parameters: Parameters that transform the HTTP response from a backend integration before returning the response to clients. Supported only for HTTP APIs.
        :param pulumi.Input[str] template_selection_expression: The template selection expression for the integration. Supported only for WebSocket APIs.
        :param pulumi.Input[int] timeout_in_millis: Custom timeout between 50 and 29000 milliseconds for WebSocket APIs and between 50 and 30000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.
        :param pulumi.Input['IntegrationTlsConfigArgs'] tls_config: The TLS configuration for a private integration. If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.
        """
        pulumi.set(__self__, "api_id", api_id)
        pulumi.set(__self__, "integration_type", integration_type)
        if connection_id is not None:
            pulumi.set(__self__, "connection_id", connection_id)
        if connection_type is not None:
            pulumi.set(__self__, "connection_type", connection_type)
        if content_handling_strategy is not None:
            pulumi.set(__self__, "content_handling_strategy", content_handling_strategy)
        if credentials_arn is not None:
            pulumi.set(__self__, "credentials_arn", credentials_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if integration_method is not None:
            pulumi.set(__self__, "integration_method", integration_method)
        if integration_subtype is not None:
            pulumi.set(__self__, "integration_subtype", integration_subtype)
        if integration_uri is not None:
            pulumi.set(__self__, "integration_uri", integration_uri)
        if passthrough_behavior is not None:
            pulumi.set(__self__, "passthrough_behavior", passthrough_behavior)
        if payload_format_version is not None:
            pulumi.set(__self__, "payload_format_version", payload_format_version)
        if request_parameters is not None:
            pulumi.set(__self__, "request_parameters", request_parameters)
        if request_templates is not None:
            pulumi.set(__self__, "request_templates", request_templates)
        if response_parameters is not None:
            pulumi.set(__self__, "response_parameters", response_parameters)
        if template_selection_expression is not None:
            pulumi.set(__self__, "template_selection_expression", template_selection_expression)
        if timeout_in_millis is not None:
            pulumi.set(__self__, "timeout_in_millis", timeout_in_millis)
        if tls_config is not None:
            pulumi.set(__self__, "tls_config", tls_config)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> pulumi.Input[str]:
        """
        The API identifier.
        """
        return pulumi.get(self, "api_id")

    @api_id.setter
    def api_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_id", value)

    @property
    @pulumi.getter(name="integrationType")
    def integration_type(self) -> pulumi.Input[str]:
        """
        The integration type of an integration.
        """
        return pulumi.get(self, "integration_type")

    @integration_type.setter
    def integration_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "integration_type", value)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC link for a private integration. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "connection_id")

    @connection_id.setter
    def connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_id", value)

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the network connection to the integration endpoint. Specify INTERNET for connections through the public routable internet or VPC_LINK for private connections between API Gateway and resources in a VPC. The default value is INTERNET.
        """
        return pulumi.get(self, "connection_type")

    @connection_type.setter
    def connection_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_type", value)

    @property
    @pulumi.getter(name="contentHandlingStrategy")
    def content_handling_strategy(self) -> Optional[pulumi.Input[str]]:
        """
        Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are CONVERT_TO_BINARY and CONVERT_TO_TEXT.
        """
        return pulumi.get(self, "content_handling_strategy")

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_handling_strategy", value)

    @property
    @pulumi.getter(name="credentialsArn")
    def credentials_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string arn:aws:iam::*:user/*. To use resource-based permissions on supported AWS services, don't specify this parameter.
        """
        return pulumi.get(self, "credentials_arn")

    @credentials_arn.setter
    def credentials_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "credentials_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the integration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="integrationMethod")
    def integration_method(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the integration's HTTP method type.
        """
        return pulumi.get(self, "integration_method")

    @integration_method.setter
    def integration_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_method", value)

    @property
    @pulumi.getter(name="integrationSubtype")
    def integration_subtype(self) -> Optional[pulumi.Input[str]]:
        """
        Supported only for HTTP API AWS_PROXY integrations. Specifies the AWS service action to invoke.
        """
        return pulumi.get(self, "integration_subtype")

    @integration_subtype.setter
    def integration_subtype(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_subtype", value)

    @property
    @pulumi.getter(name="integrationUri")
    def integration_uri(self) -> Optional[pulumi.Input[str]]:
        """
        For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration, specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service.
        """
        return pulumi.get(self, "integration_uri")

    @integration_uri.setter
    def integration_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_uri", value)

    @property
    @pulumi.getter(name="passthroughBehavior")
    def passthrough_behavior(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "passthrough_behavior")

    @passthrough_behavior.setter
    def passthrough_behavior(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "passthrough_behavior", value)

    @property
    @pulumi.getter(name="payloadFormatVersion")
    def payload_format_version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are 1.0 and 2.0 For all other integrations, 1.0 is the only supported value.
        """
        return pulumi.get(self, "payload_format_version")

    @payload_format_version.setter
    def payload_format_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "payload_format_version", value)

    @property
    @pulumi.getter(name="requestParameters")
    def request_parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A key-value map specifying parameters.
        """
        return pulumi.get(self, "request_parameters")

    @request_parameters.setter
    def request_parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "request_parameters", value)

    @property
    @pulumi.getter(name="requestTemplates")
    def request_templates(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.
        """
        return pulumi.get(self, "request_templates")

    @request_templates.setter
    def request_templates(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "request_templates", value)

    @property
    @pulumi.getter(name="responseParameters")
    def response_parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['IntegrationResponseParameterMapArgs']]]]:
        """
        Parameters that transform the HTTP response from a backend integration before returning the response to clients. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "response_parameters")

    @response_parameters.setter
    def response_parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['IntegrationResponseParameterMapArgs']]]]):
        pulumi.set(self, "response_parameters", value)

    @property
    @pulumi.getter(name="templateSelectionExpression")
    def template_selection_expression(self) -> Optional[pulumi.Input[str]]:
        """
        The template selection expression for the integration. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "template_selection_expression")

    @template_selection_expression.setter
    def template_selection_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_selection_expression", value)

    @property
    @pulumi.getter(name="timeoutInMillis")
    def timeout_in_millis(self) -> Optional[pulumi.Input[int]]:
        """
        Custom timeout between 50 and 29000 milliseconds for WebSocket APIs and between 50 and 30000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.
        """
        return pulumi.get(self, "timeout_in_millis")

    @timeout_in_millis.setter
    def timeout_in_millis(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_in_millis", value)

    @property
    @pulumi.getter(name="tlsConfig")
    def tls_config(self) -> Optional[pulumi.Input['IntegrationTlsConfigArgs']]:
        """
        The TLS configuration for a private integration. If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "tls_config")

    @tls_config.setter
    def tls_config(self, value: Optional[pulumi.Input['IntegrationTlsConfigArgs']]):
        pulumi.set(self, "tls_config", value)


class Integration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 connection_type: Optional[pulumi.Input[str]] = None,
                 content_handling_strategy: Optional[pulumi.Input[str]] = None,
                 credentials_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 integration_method: Optional[pulumi.Input[str]] = None,
                 integration_subtype: Optional[pulumi.Input[str]] = None,
                 integration_type: Optional[pulumi.Input[str]] = None,
                 integration_uri: Optional[pulumi.Input[str]] = None,
                 passthrough_behavior: Optional[pulumi.Input[str]] = None,
                 payload_format_version: Optional[pulumi.Input[str]] = None,
                 request_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 request_templates: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 response_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[Union['IntegrationResponseParameterMapArgs', 'IntegrationResponseParameterMapArgsDict']]]]] = None,
                 template_selection_expression: Optional[pulumi.Input[str]] = None,
                 timeout_in_millis: Optional[pulumi.Input[int]] = None,
                 tls_config: Optional[pulumi.Input[Union['IntegrationTlsConfigArgs', 'IntegrationTlsConfigArgsDict']]] = None,
                 __props__=None):
        """
        An example resource schema demonstrating some basic constructs and validation rules.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: The API identifier.
        :param pulumi.Input[str] connection_id: The ID of the VPC link for a private integration. Supported only for HTTP APIs.
        :param pulumi.Input[str] connection_type: The type of the network connection to the integration endpoint. Specify INTERNET for connections through the public routable internet or VPC_LINK for private connections between API Gateway and resources in a VPC. The default value is INTERNET.
        :param pulumi.Input[str] content_handling_strategy: Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are CONVERT_TO_BINARY and CONVERT_TO_TEXT.
        :param pulumi.Input[str] credentials_arn: Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string arn:aws:iam::*:user/*. To use resource-based permissions on supported AWS services, don't specify this parameter.
        :param pulumi.Input[str] description: The description of the integration.
        :param pulumi.Input[str] integration_method: Specifies the integration's HTTP method type.
        :param pulumi.Input[str] integration_subtype: Supported only for HTTP API AWS_PROXY integrations. Specifies the AWS service action to invoke.
        :param pulumi.Input[str] integration_type: The integration type of an integration.
        :param pulumi.Input[str] integration_uri: For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration, specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service.
        :param pulumi.Input[str] passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER. Supported only for WebSocket APIs.
        :param pulumi.Input[str] payload_format_version: Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are 1.0 and 2.0 For all other integrations, 1.0 is the only supported value.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] request_parameters: A key-value map specifying parameters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] request_templates: A map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.
        :param pulumi.Input[Mapping[str, pulumi.Input[Union['IntegrationResponseParameterMapArgs', 'IntegrationResponseParameterMapArgsDict']]]] response_parameters: Parameters that transform the HTTP response from a backend integration before returning the response to clients. Supported only for HTTP APIs.
        :param pulumi.Input[str] template_selection_expression: The template selection expression for the integration. Supported only for WebSocket APIs.
        :param pulumi.Input[int] timeout_in_millis: Custom timeout between 50 and 29000 milliseconds for WebSocket APIs and between 50 and 30000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.
        :param pulumi.Input[Union['IntegrationTlsConfigArgs', 'IntegrationTlsConfigArgsDict']] tls_config: The TLS configuration for a private integration. If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IntegrationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An example resource schema demonstrating some basic constructs and validation rules.

        :param str resource_name: The name of the resource.
        :param IntegrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 connection_type: Optional[pulumi.Input[str]] = None,
                 content_handling_strategy: Optional[pulumi.Input[str]] = None,
                 credentials_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 integration_method: Optional[pulumi.Input[str]] = None,
                 integration_subtype: Optional[pulumi.Input[str]] = None,
                 integration_type: Optional[pulumi.Input[str]] = None,
                 integration_uri: Optional[pulumi.Input[str]] = None,
                 passthrough_behavior: Optional[pulumi.Input[str]] = None,
                 payload_format_version: Optional[pulumi.Input[str]] = None,
                 request_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 request_templates: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 response_parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[Union['IntegrationResponseParameterMapArgs', 'IntegrationResponseParameterMapArgsDict']]]]] = None,
                 template_selection_expression: Optional[pulumi.Input[str]] = None,
                 timeout_in_millis: Optional[pulumi.Input[int]] = None,
                 tls_config: Optional[pulumi.Input[Union['IntegrationTlsConfigArgs', 'IntegrationTlsConfigArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationArgs.__new__(IntegrationArgs)

            if api_id is None and not opts.urn:
                raise TypeError("Missing required property 'api_id'")
            __props__.__dict__["api_id"] = api_id
            __props__.__dict__["connection_id"] = connection_id
            __props__.__dict__["connection_type"] = connection_type
            __props__.__dict__["content_handling_strategy"] = content_handling_strategy
            __props__.__dict__["credentials_arn"] = credentials_arn
            __props__.__dict__["description"] = description
            __props__.__dict__["integration_method"] = integration_method
            __props__.__dict__["integration_subtype"] = integration_subtype
            if integration_type is None and not opts.urn:
                raise TypeError("Missing required property 'integration_type'")
            __props__.__dict__["integration_type"] = integration_type
            __props__.__dict__["integration_uri"] = integration_uri
            __props__.__dict__["passthrough_behavior"] = passthrough_behavior
            __props__.__dict__["payload_format_version"] = payload_format_version
            __props__.__dict__["request_parameters"] = request_parameters
            __props__.__dict__["request_templates"] = request_templates
            __props__.__dict__["response_parameters"] = response_parameters
            __props__.__dict__["template_selection_expression"] = template_selection_expression
            __props__.__dict__["timeout_in_millis"] = timeout_in_millis
            __props__.__dict__["tls_config"] = tls_config
            __props__.__dict__["integration_id"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["apiId"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Integration, __self__).__init__(
            'aws-native:apigatewayv2:Integration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Integration':
        """
        Get an existing Integration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IntegrationArgs.__new__(IntegrationArgs)

        __props__.__dict__["api_id"] = None
        __props__.__dict__["connection_id"] = None
        __props__.__dict__["connection_type"] = None
        __props__.__dict__["content_handling_strategy"] = None
        __props__.__dict__["credentials_arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["integration_id"] = None
        __props__.__dict__["integration_method"] = None
        __props__.__dict__["integration_subtype"] = None
        __props__.__dict__["integration_type"] = None
        __props__.__dict__["integration_uri"] = None
        __props__.__dict__["passthrough_behavior"] = None
        __props__.__dict__["payload_format_version"] = None
        __props__.__dict__["request_parameters"] = None
        __props__.__dict__["request_templates"] = None
        __props__.__dict__["response_parameters"] = None
        __props__.__dict__["template_selection_expression"] = None
        __props__.__dict__["timeout_in_millis"] = None
        __props__.__dict__["tls_config"] = None
        return Integration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> pulumi.Output[str]:
        """
        The API identifier.
        """
        return pulumi.get(self, "api_id")

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the VPC link for a private integration. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of the network connection to the integration endpoint. Specify INTERNET for connections through the public routable internet or VPC_LINK for private connections between API Gateway and resources in a VPC. The default value is INTERNET.
        """
        return pulumi.get(self, "connection_type")

    @property
    @pulumi.getter(name="contentHandlingStrategy")
    def content_handling_strategy(self) -> pulumi.Output[Optional[str]]:
        """
        Supported only for WebSocket APIs. Specifies how to handle response payload content type conversions. Supported values are CONVERT_TO_BINARY and CONVERT_TO_TEXT.
        """
        return pulumi.get(self, "content_handling_strategy")

    @property
    @pulumi.getter(name="credentialsArn")
    def credentials_arn(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string arn:aws:iam::*:user/*. To use resource-based permissions on supported AWS services, don't specify this parameter.
        """
        return pulumi.get(self, "credentials_arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the integration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="integrationId")
    def integration_id(self) -> pulumi.Output[str]:
        """
        The integration ID.
        """
        return pulumi.get(self, "integration_id")

    @property
    @pulumi.getter(name="integrationMethod")
    def integration_method(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the integration's HTTP method type.
        """
        return pulumi.get(self, "integration_method")

    @property
    @pulumi.getter(name="integrationSubtype")
    def integration_subtype(self) -> pulumi.Output[Optional[str]]:
        """
        Supported only for HTTP API AWS_PROXY integrations. Specifies the AWS service action to invoke.
        """
        return pulumi.get(self, "integration_subtype")

    @property
    @pulumi.getter(name="integrationType")
    def integration_type(self) -> pulumi.Output[str]:
        """
        The integration type of an integration.
        """
        return pulumi.get(self, "integration_type")

    @property
    @pulumi.getter(name="integrationUri")
    def integration_uri(self) -> pulumi.Output[Optional[str]]:
        """
        For a Lambda integration, specify the URI of a Lambda function. For an HTTP integration, specify a fully-qualified URL. For an HTTP API private integration, specify the ARN of an Application Load Balancer listener, Network Load Balancer listener, or AWS Cloud Map service.
        """
        return pulumi.get(self, "integration_uri")

    @property
    @pulumi.getter(name="passthroughBehavior")
    def passthrough_behavior(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the pass-through behavior for incoming requests based on the Content-Type header in the request, and the available mapping templates specified as the requestTemplates property on the Integration resource. There are three valid values: WHEN_NO_MATCH, WHEN_NO_TEMPLATES, and NEVER. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "passthrough_behavior")

    @property
    @pulumi.getter(name="payloadFormatVersion")
    def payload_format_version(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the format of the payload sent to an integration. Required for HTTP APIs. For HTTP APIs, supported values for Lambda proxy integrations are 1.0 and 2.0 For all other integrations, 1.0 is the only supported value.
        """
        return pulumi.get(self, "payload_format_version")

    @property
    @pulumi.getter(name="requestParameters")
    def request_parameters(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A key-value map specifying parameters.
        """
        return pulumi.get(self, "request_parameters")

    @property
    @pulumi.getter(name="requestTemplates")
    def request_templates(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.
        """
        return pulumi.get(self, "request_templates")

    @property
    @pulumi.getter(name="responseParameters")
    def response_parameters(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.IntegrationResponseParameterMap']]]:
        """
        Parameters that transform the HTTP response from a backend integration before returning the response to clients. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "response_parameters")

    @property
    @pulumi.getter(name="templateSelectionExpression")
    def template_selection_expression(self) -> pulumi.Output[Optional[str]]:
        """
        The template selection expression for the integration. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "template_selection_expression")

    @property
    @pulumi.getter(name="timeoutInMillis")
    def timeout_in_millis(self) -> pulumi.Output[Optional[int]]:
        """
        Custom timeout between 50 and 29000 milliseconds for WebSocket APIs and between 50 and 30000 milliseconds for HTTP APIs. The default timeout is 29 seconds for WebSocket APIs and 30 seconds for HTTP APIs.
        """
        return pulumi.get(self, "timeout_in_millis")

    @property
    @pulumi.getter(name="tlsConfig")
    def tls_config(self) -> pulumi.Output[Optional['outputs.IntegrationTlsConfig']]:
        """
        The TLS configuration for a private integration. If you specify a TLS configuration, private integration traffic uses the HTTPS protocol. Supported only for HTTP APIs.
        """
        return pulumi.get(self, "tls_config")

