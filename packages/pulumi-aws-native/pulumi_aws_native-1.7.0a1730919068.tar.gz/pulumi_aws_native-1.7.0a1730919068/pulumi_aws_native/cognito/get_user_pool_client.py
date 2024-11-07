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

__all__ = [
    'GetUserPoolClientResult',
    'AwaitableGetUserPoolClientResult',
    'get_user_pool_client',
    'get_user_pool_client_output',
]

@pulumi.output_type
class GetUserPoolClientResult:
    def __init__(__self__, access_token_validity=None, allowed_o_auth_flows=None, allowed_o_auth_flows_user_pool_client=None, allowed_o_auth_scopes=None, analytics_configuration=None, auth_session_validity=None, callback_urls=None, client_id=None, client_name=None, client_secret=None, default_redirect_uri=None, enable_propagate_additional_user_context_data=None, enable_token_revocation=None, explicit_auth_flows=None, id_token_validity=None, logout_urls=None, name=None, prevent_user_existence_errors=None, read_attributes=None, refresh_token_validity=None, supported_identity_providers=None, token_validity_units=None, write_attributes=None):
        if access_token_validity and not isinstance(access_token_validity, int):
            raise TypeError("Expected argument 'access_token_validity' to be a int")
        pulumi.set(__self__, "access_token_validity", access_token_validity)
        if allowed_o_auth_flows and not isinstance(allowed_o_auth_flows, list):
            raise TypeError("Expected argument 'allowed_o_auth_flows' to be a list")
        pulumi.set(__self__, "allowed_o_auth_flows", allowed_o_auth_flows)
        if allowed_o_auth_flows_user_pool_client and not isinstance(allowed_o_auth_flows_user_pool_client, bool):
            raise TypeError("Expected argument 'allowed_o_auth_flows_user_pool_client' to be a bool")
        pulumi.set(__self__, "allowed_o_auth_flows_user_pool_client", allowed_o_auth_flows_user_pool_client)
        if allowed_o_auth_scopes and not isinstance(allowed_o_auth_scopes, list):
            raise TypeError("Expected argument 'allowed_o_auth_scopes' to be a list")
        pulumi.set(__self__, "allowed_o_auth_scopes", allowed_o_auth_scopes)
        if analytics_configuration and not isinstance(analytics_configuration, dict):
            raise TypeError("Expected argument 'analytics_configuration' to be a dict")
        pulumi.set(__self__, "analytics_configuration", analytics_configuration)
        if auth_session_validity and not isinstance(auth_session_validity, int):
            raise TypeError("Expected argument 'auth_session_validity' to be a int")
        pulumi.set(__self__, "auth_session_validity", auth_session_validity)
        if callback_urls and not isinstance(callback_urls, list):
            raise TypeError("Expected argument 'callback_urls' to be a list")
        pulumi.set(__self__, "callback_urls", callback_urls)
        if client_id and not isinstance(client_id, str):
            raise TypeError("Expected argument 'client_id' to be a str")
        pulumi.set(__self__, "client_id", client_id)
        if client_name and not isinstance(client_name, str):
            raise TypeError("Expected argument 'client_name' to be a str")
        pulumi.set(__self__, "client_name", client_name)
        if client_secret and not isinstance(client_secret, str):
            raise TypeError("Expected argument 'client_secret' to be a str")
        pulumi.set(__self__, "client_secret", client_secret)
        if default_redirect_uri and not isinstance(default_redirect_uri, str):
            raise TypeError("Expected argument 'default_redirect_uri' to be a str")
        pulumi.set(__self__, "default_redirect_uri", default_redirect_uri)
        if enable_propagate_additional_user_context_data and not isinstance(enable_propagate_additional_user_context_data, bool):
            raise TypeError("Expected argument 'enable_propagate_additional_user_context_data' to be a bool")
        pulumi.set(__self__, "enable_propagate_additional_user_context_data", enable_propagate_additional_user_context_data)
        if enable_token_revocation and not isinstance(enable_token_revocation, bool):
            raise TypeError("Expected argument 'enable_token_revocation' to be a bool")
        pulumi.set(__self__, "enable_token_revocation", enable_token_revocation)
        if explicit_auth_flows and not isinstance(explicit_auth_flows, list):
            raise TypeError("Expected argument 'explicit_auth_flows' to be a list")
        pulumi.set(__self__, "explicit_auth_flows", explicit_auth_flows)
        if id_token_validity and not isinstance(id_token_validity, int):
            raise TypeError("Expected argument 'id_token_validity' to be a int")
        pulumi.set(__self__, "id_token_validity", id_token_validity)
        if logout_urls and not isinstance(logout_urls, list):
            raise TypeError("Expected argument 'logout_urls' to be a list")
        pulumi.set(__self__, "logout_urls", logout_urls)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if prevent_user_existence_errors and not isinstance(prevent_user_existence_errors, str):
            raise TypeError("Expected argument 'prevent_user_existence_errors' to be a str")
        pulumi.set(__self__, "prevent_user_existence_errors", prevent_user_existence_errors)
        if read_attributes and not isinstance(read_attributes, list):
            raise TypeError("Expected argument 'read_attributes' to be a list")
        pulumi.set(__self__, "read_attributes", read_attributes)
        if refresh_token_validity and not isinstance(refresh_token_validity, int):
            raise TypeError("Expected argument 'refresh_token_validity' to be a int")
        pulumi.set(__self__, "refresh_token_validity", refresh_token_validity)
        if supported_identity_providers and not isinstance(supported_identity_providers, list):
            raise TypeError("Expected argument 'supported_identity_providers' to be a list")
        pulumi.set(__self__, "supported_identity_providers", supported_identity_providers)
        if token_validity_units and not isinstance(token_validity_units, dict):
            raise TypeError("Expected argument 'token_validity_units' to be a dict")
        pulumi.set(__self__, "token_validity_units", token_validity_units)
        if write_attributes and not isinstance(write_attributes, list):
            raise TypeError("Expected argument 'write_attributes' to be a list")
        pulumi.set(__self__, "write_attributes", write_attributes)

    @property
    @pulumi.getter(name="accessTokenValidity")
    def access_token_validity(self) -> Optional[int]:
        """
        The access token time limit. After this limit expires, your user can't use their access token. To specify the time unit for `AccessTokenValidity` as `seconds` , `minutes` , `hours` , or `days` , set a `TokenValidityUnits` value in your API request.

        For example, when you set `AccessTokenValidity` to `10` and `TokenValidityUnits` to `hours` , your user can authorize access with
        their access token for 10 hours.

        The default time unit for `AccessTokenValidity` in an API request is hours. *Valid range* is displayed below in seconds.

        If you don't specify otherwise in the configuration of your app client, your access
        tokens are valid for one hour.
        """
        return pulumi.get(self, "access_token_validity")

    @property
    @pulumi.getter(name="allowedOAuthFlows")
    def allowed_o_auth_flows(self) -> Optional[Sequence[str]]:
        """
        The OAuth grant types that you want your app client to generate. To create an app client that generates client credentials grants, you must add `client_credentials` as the only allowed OAuth flow.

        - **code** - Use a code grant flow, which provides an authorization code as the response. This code can be exchanged for access tokens with the `/oauth2/token` endpoint.
        - **implicit** - Issue the access token (and, optionally, ID token, based on scopes) directly to your user.
        - **client_credentials** - Issue the access token from the `/oauth2/token` endpoint directly to a non-person user using a combination of the client ID and client secret.
        """
        return pulumi.get(self, "allowed_o_auth_flows")

    @property
    @pulumi.getter(name="allowedOAuthFlowsUserPoolClient")
    def allowed_o_auth_flows_user_pool_client(self) -> Optional[bool]:
        """
        Set to `true` to use OAuth 2.0 features in your user pool app client.

        `AllowedOAuthFlowsUserPoolClient` must be `true` before you can configure the following features in your app client.

        - `CallBackURLs` : Callback URLs.
        - `LogoutURLs` : Sign-out redirect URLs.
        - `AllowedOAuthScopes` : OAuth 2.0 scopes.
        - `AllowedOAuthFlows` : Support for authorization code, implicit, and client credentials OAuth 2.0 grants.

        To use OAuth 2.0 features, configure one of these features in the Amazon Cognito console or set `AllowedOAuthFlowsUserPoolClient` to `true` in a `CreateUserPoolClient` or `UpdateUserPoolClient` API request. If you don't set a value for `AllowedOAuthFlowsUserPoolClient` in a request with the AWS CLI or SDKs, it defaults to `false` .
        """
        return pulumi.get(self, "allowed_o_auth_flows_user_pool_client")

    @property
    @pulumi.getter(name="allowedOAuthScopes")
    def allowed_o_auth_scopes(self) -> Optional[Sequence[str]]:
        """
        The allowed OAuth scopes. Possible values provided by OAuth are `phone` , `email` , `openid` , and `profile` . Possible values provided by AWS are `aws.cognito.signin.user.admin` . Custom scopes created in Resource Servers are also supported.
        """
        return pulumi.get(self, "allowed_o_auth_scopes")

    @property
    @pulumi.getter(name="analyticsConfiguration")
    def analytics_configuration(self) -> Optional['outputs.UserPoolClientAnalyticsConfiguration']:
        """
        The user pool analytics configuration for collecting metrics and sending them to your Amazon Pinpoint campaign.

        > In AWS Regions where Amazon Pinpoint isn't available, user pools only support sending events to Amazon Pinpoint projects in AWS Region us-east-1. In Regions where Amazon Pinpoint is available, user pools support sending events to Amazon Pinpoint projects within that same Region.
        """
        return pulumi.get(self, "analytics_configuration")

    @property
    @pulumi.getter(name="authSessionValidity")
    def auth_session_validity(self) -> Optional[int]:
        """
        Amazon Cognito creates a session token for each API request in an authentication flow. `AuthSessionValidity` is the duration, in minutes, of that session token. Your user pool native user must respond to each authentication challenge before the session expires.
        """
        return pulumi.get(self, "auth_session_validity")

    @property
    @pulumi.getter(name="callbackUrls")
    def callback_urls(self) -> Optional[Sequence[str]]:
        """
        A list of allowed redirect (callback) URLs for the IdPs.

        A redirect URI must:

        - Be an absolute URI.
        - Be registered with the authorization server.
        - Not include a fragment component.

        See [OAuth 2.0 - Redirection Endpoint](https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6749#section-3.1.2) .

        Amazon Cognito requires HTTPS over HTTP except for http://localhost for testing purposes only.

        App callback URLs such as myapp://example are also supported.
        """
        return pulumi.get(self, "callback_urls")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[str]:
        """
        The ID of the app client, for example `1example23456789` .
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientName")
    def client_name(self) -> Optional[str]:
        """
        The client name for the user pool client you would like to create.
        """
        return pulumi.get(self, "client_name")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[str]:
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="defaultRedirectUri")
    def default_redirect_uri(self) -> Optional[str]:
        """
        The default redirect URI. In app clients with one assigned IdP, replaces `redirect_uri` in authentication requests. Must be in the `CallbackURLs` list.

        A redirect URI must:

        - Be an absolute URI.
        - Be registered with the authorization server.
        - Not include a fragment component.

        For more information, see [Default redirect URI](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html#cognito-user-pools-app-idp-settings-about) .

        Amazon Cognito requires HTTPS over HTTP except for http://localhost for testing purposes only.

        App callback URLs such as myapp://example are also supported.
        """
        return pulumi.get(self, "default_redirect_uri")

    @property
    @pulumi.getter(name="enablePropagateAdditionalUserContextData")
    def enable_propagate_additional_user_context_data(self) -> Optional[bool]:
        """
        Activates the propagation of additional user context data. For more information about propagation of user context data, see [Adding advanced security to a user pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-advanced-security.html) . If you don’t include this parameter, you can't send device fingerprint information, including source IP address, to Amazon Cognito advanced security. You can only activate `EnablePropagateAdditionalUserContextData` in an app client that has a client secret.
        """
        return pulumi.get(self, "enable_propagate_additional_user_context_data")

    @property
    @pulumi.getter(name="enableTokenRevocation")
    def enable_token_revocation(self) -> Optional[bool]:
        """
        Activates or deactivates token revocation. For more information about revoking tokens, see [RevokeToken](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_RevokeToken.html) .

        If you don't include this parameter, token revocation is automatically activated for the new user pool client.
        """
        return pulumi.get(self, "enable_token_revocation")

    @property
    @pulumi.getter(name="explicitAuthFlows")
    def explicit_auth_flows(self) -> Optional[Sequence[str]]:
        """
        The authentication flows that you want your user pool client to support. For each app client in your user pool, you can sign in your users with any combination of one or more flows, including with a user name and Secure Remote Password (SRP), a user name and password, or a custom authentication process that you define with Lambda functions.

        > If you don't specify a value for `ExplicitAuthFlows` , your user client supports `ALLOW_REFRESH_TOKEN_AUTH` , `ALLOW_USER_SRP_AUTH` , and `ALLOW_CUSTOM_AUTH` . 

        Valid values include:

        - `ALLOW_ADMIN_USER_PASSWORD_AUTH` : Enable admin based user password authentication flow `ADMIN_USER_PASSWORD_AUTH` . This setting replaces the `ADMIN_NO_SRP_AUTH` setting. With this authentication flow, your app passes a user name and password to Amazon Cognito in the request, instead of using the Secure Remote Password (SRP) protocol to securely transmit the password.
        - `ALLOW_CUSTOM_AUTH` : Enable Lambda trigger based authentication.
        - `ALLOW_USER_PASSWORD_AUTH` : Enable user password-based authentication. In this flow, Amazon Cognito receives the password in the request instead of using the SRP protocol to verify passwords.
        - `ALLOW_USER_SRP_AUTH` : Enable SRP-based authentication.
        - `ALLOW_REFRESH_TOKEN_AUTH` : Enable authflow to refresh tokens.

        In some environments, you will see the values `ADMIN_NO_SRP_AUTH` , `CUSTOM_AUTH_FLOW_ONLY` , or `USER_PASSWORD_AUTH` . You can't assign these legacy `ExplicitAuthFlows` values to user pool clients at the same time as values that begin with `ALLOW_` ,
        like `ALLOW_USER_SRP_AUTH` .
        """
        return pulumi.get(self, "explicit_auth_flows")

    @property
    @pulumi.getter(name="idTokenValidity")
    def id_token_validity(self) -> Optional[int]:
        """
        The ID token time limit. After this limit expires, your user can't use their ID token. To specify the time unit for `IdTokenValidity` as `seconds` , `minutes` , `hours` , or `days` , set a `TokenValidityUnits` value in your API request.

        For example, when you set `IdTokenValidity` as `10` and `TokenValidityUnits` as `hours` , your user can authenticate their session with their ID token for 10 hours.

        The default time unit for `IdTokenValidity` in an API request is hours. *Valid range* is displayed below in seconds.

        If you don't specify otherwise in the configuration of your app client, your ID
        tokens are valid for one hour.
        """
        return pulumi.get(self, "id_token_validity")

    @property
    @pulumi.getter(name="logoutUrls")
    def logout_urls(self) -> Optional[Sequence[str]]:
        """
        A list of allowed logout URLs for the IdPs.
        """
        return pulumi.get(self, "logout_urls")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="preventUserExistenceErrors")
    def prevent_user_existence_errors(self) -> Optional[str]:
        """
        Errors and responses that you want Amazon Cognito APIs to return during authentication, account confirmation, and password recovery when the user doesn't exist in the user pool. When set to `ENABLED` and the user doesn't exist, authentication returns an error indicating either the username or password was incorrect. Account confirmation and password recovery return a response indicating a code was sent to a simulated destination. When set to `LEGACY` , those APIs return a `UserNotFoundException` exception if the user doesn't exist in the user pool.

        Valid values include:

        - `ENABLED` - This prevents user existence-related errors.
        - `LEGACY` - This represents the early behavior of Amazon Cognito where user existence related errors aren't prevented.

        Defaults to `LEGACY` when you don't provide a value.
        """
        return pulumi.get(self, "prevent_user_existence_errors")

    @property
    @pulumi.getter(name="readAttributes")
    def read_attributes(self) -> Optional[Sequence[str]]:
        """
        The list of user attributes that you want your app client to have read access to. After your user authenticates in your app, their access token authorizes them to read their own attribute value for any attribute in this list. An example of this kind of activity is when your user selects a link to view their profile information. Your app makes a [GetUser](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_GetUser.html) API request to retrieve and display your user's profile data.

        When you don't specify the `ReadAttributes` for your app client, your app can read the values of `email_verified` , `phone_number_verified` , and the Standard attributes of your user pool. When your user pool app client has read access to these default attributes, `ReadAttributes` doesn't return any information. Amazon Cognito only populates `ReadAttributes` in the API response if you have specified your own custom set of read attributes.
        """
        return pulumi.get(self, "read_attributes")

    @property
    @pulumi.getter(name="refreshTokenValidity")
    def refresh_token_validity(self) -> Optional[int]:
        """
        The refresh token time limit. After this limit expires, your user can't use their refresh token. To specify the time unit for `RefreshTokenValidity` as `seconds` , `minutes` , `hours` , or `days` , set a `TokenValidityUnits` value in your API request.

        For example, when you set `RefreshTokenValidity` as `10` and `TokenValidityUnits` as `days` , your user can refresh their session
        and retrieve new access and ID tokens for 10 days.

        The default time unit for `RefreshTokenValidity` in an API request is days. You can't set `RefreshTokenValidity` to 0. If you do, Amazon Cognito overrides the value with the default value of 30 days. *Valid range* is displayed below in seconds.

        If you don't specify otherwise in the configuration of your app client, your refresh
        tokens are valid for 30 days.
        """
        return pulumi.get(self, "refresh_token_validity")

    @property
    @pulumi.getter(name="supportedIdentityProviders")
    def supported_identity_providers(self) -> Optional[Sequence[str]]:
        """
        A list of provider names for the identity providers (IdPs) that are supported on this client. The following are supported: `COGNITO` , `Facebook` , `Google` , `SignInWithApple` , and `LoginWithAmazon` . You can also specify the names that you configured for the SAML and OIDC IdPs in your user pool, for example `MySAMLIdP` or `MyOIDCIdP` .
        """
        return pulumi.get(self, "supported_identity_providers")

    @property
    @pulumi.getter(name="tokenValidityUnits")
    def token_validity_units(self) -> Optional['outputs.UserPoolClientTokenValidityUnits']:
        """
        The units in which the validity times are represented. The default unit for RefreshToken is days, and default for ID and access tokens are hours.
        """
        return pulumi.get(self, "token_validity_units")

    @property
    @pulumi.getter(name="writeAttributes")
    def write_attributes(self) -> Optional[Sequence[str]]:
        """
        The list of user attributes that you want your app client to have write access to. After your user authenticates in your app, their access token authorizes them to set or modify their own attribute value for any attribute in this list. An example of this kind of activity is when you present your user with a form to update their profile information and they change their last name. Your app then makes an [UpdateUserAttributes](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserAttributes.html) API request and sets `family_name` to the new value.

        When you don't specify the `WriteAttributes` for your app client, your app can write the values of the Standard attributes of your user pool. When your user pool has write access to these default attributes, `WriteAttributes` doesn't return any information. Amazon Cognito only populates `WriteAttributes` in the API response if you have specified your own custom set of write attributes.

        If your app client allows users to sign in through an IdP, this array must include all attributes that you have mapped to IdP attributes. Amazon Cognito updates mapped attributes when users sign in to your application through an IdP. If your app client does not have write access to a mapped attribute, Amazon Cognito throws an error when it tries to update the attribute. For more information, see [Specifying IdP Attribute Mappings for Your user pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html) .
        """
        return pulumi.get(self, "write_attributes")


class AwaitableGetUserPoolClientResult(GetUserPoolClientResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserPoolClientResult(
            access_token_validity=self.access_token_validity,
            allowed_o_auth_flows=self.allowed_o_auth_flows,
            allowed_o_auth_flows_user_pool_client=self.allowed_o_auth_flows_user_pool_client,
            allowed_o_auth_scopes=self.allowed_o_auth_scopes,
            analytics_configuration=self.analytics_configuration,
            auth_session_validity=self.auth_session_validity,
            callback_urls=self.callback_urls,
            client_id=self.client_id,
            client_name=self.client_name,
            client_secret=self.client_secret,
            default_redirect_uri=self.default_redirect_uri,
            enable_propagate_additional_user_context_data=self.enable_propagate_additional_user_context_data,
            enable_token_revocation=self.enable_token_revocation,
            explicit_auth_flows=self.explicit_auth_flows,
            id_token_validity=self.id_token_validity,
            logout_urls=self.logout_urls,
            name=self.name,
            prevent_user_existence_errors=self.prevent_user_existence_errors,
            read_attributes=self.read_attributes,
            refresh_token_validity=self.refresh_token_validity,
            supported_identity_providers=self.supported_identity_providers,
            token_validity_units=self.token_validity_units,
            write_attributes=self.write_attributes)


def get_user_pool_client(client_id: Optional[str] = None,
                         user_pool_id: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserPoolClientResult:
    """
    Resource Type definition for AWS::Cognito::UserPoolClient


    :param str client_id: The ID of the app client, for example `1example23456789` .
    :param str user_pool_id: The user pool ID for the user pool where you want to create a user pool client.
    """
    __args__ = dict()
    __args__['clientId'] = client_id
    __args__['userPoolId'] = user_pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cognito:getUserPoolClient', __args__, opts=opts, typ=GetUserPoolClientResult).value

    return AwaitableGetUserPoolClientResult(
        access_token_validity=pulumi.get(__ret__, 'access_token_validity'),
        allowed_o_auth_flows=pulumi.get(__ret__, 'allowed_o_auth_flows'),
        allowed_o_auth_flows_user_pool_client=pulumi.get(__ret__, 'allowed_o_auth_flows_user_pool_client'),
        allowed_o_auth_scopes=pulumi.get(__ret__, 'allowed_o_auth_scopes'),
        analytics_configuration=pulumi.get(__ret__, 'analytics_configuration'),
        auth_session_validity=pulumi.get(__ret__, 'auth_session_validity'),
        callback_urls=pulumi.get(__ret__, 'callback_urls'),
        client_id=pulumi.get(__ret__, 'client_id'),
        client_name=pulumi.get(__ret__, 'client_name'),
        client_secret=pulumi.get(__ret__, 'client_secret'),
        default_redirect_uri=pulumi.get(__ret__, 'default_redirect_uri'),
        enable_propagate_additional_user_context_data=pulumi.get(__ret__, 'enable_propagate_additional_user_context_data'),
        enable_token_revocation=pulumi.get(__ret__, 'enable_token_revocation'),
        explicit_auth_flows=pulumi.get(__ret__, 'explicit_auth_flows'),
        id_token_validity=pulumi.get(__ret__, 'id_token_validity'),
        logout_urls=pulumi.get(__ret__, 'logout_urls'),
        name=pulumi.get(__ret__, 'name'),
        prevent_user_existence_errors=pulumi.get(__ret__, 'prevent_user_existence_errors'),
        read_attributes=pulumi.get(__ret__, 'read_attributes'),
        refresh_token_validity=pulumi.get(__ret__, 'refresh_token_validity'),
        supported_identity_providers=pulumi.get(__ret__, 'supported_identity_providers'),
        token_validity_units=pulumi.get(__ret__, 'token_validity_units'),
        write_attributes=pulumi.get(__ret__, 'write_attributes'))
def get_user_pool_client_output(client_id: Optional[pulumi.Input[str]] = None,
                                user_pool_id: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserPoolClientResult]:
    """
    Resource Type definition for AWS::Cognito::UserPoolClient


    :param str client_id: The ID of the app client, for example `1example23456789` .
    :param str user_pool_id: The user pool ID for the user pool where you want to create a user pool client.
    """
    __args__ = dict()
    __args__['clientId'] = client_id
    __args__['userPoolId'] = user_pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cognito:getUserPoolClient', __args__, opts=opts, typ=GetUserPoolClientResult)
    return __ret__.apply(lambda __response__: GetUserPoolClientResult(
        access_token_validity=pulumi.get(__response__, 'access_token_validity'),
        allowed_o_auth_flows=pulumi.get(__response__, 'allowed_o_auth_flows'),
        allowed_o_auth_flows_user_pool_client=pulumi.get(__response__, 'allowed_o_auth_flows_user_pool_client'),
        allowed_o_auth_scopes=pulumi.get(__response__, 'allowed_o_auth_scopes'),
        analytics_configuration=pulumi.get(__response__, 'analytics_configuration'),
        auth_session_validity=pulumi.get(__response__, 'auth_session_validity'),
        callback_urls=pulumi.get(__response__, 'callback_urls'),
        client_id=pulumi.get(__response__, 'client_id'),
        client_name=pulumi.get(__response__, 'client_name'),
        client_secret=pulumi.get(__response__, 'client_secret'),
        default_redirect_uri=pulumi.get(__response__, 'default_redirect_uri'),
        enable_propagate_additional_user_context_data=pulumi.get(__response__, 'enable_propagate_additional_user_context_data'),
        enable_token_revocation=pulumi.get(__response__, 'enable_token_revocation'),
        explicit_auth_flows=pulumi.get(__response__, 'explicit_auth_flows'),
        id_token_validity=pulumi.get(__response__, 'id_token_validity'),
        logout_urls=pulumi.get(__response__, 'logout_urls'),
        name=pulumi.get(__response__, 'name'),
        prevent_user_existence_errors=pulumi.get(__response__, 'prevent_user_existence_errors'),
        read_attributes=pulumi.get(__response__, 'read_attributes'),
        refresh_token_validity=pulumi.get(__response__, 'refresh_token_validity'),
        supported_identity_providers=pulumi.get(__response__, 'supported_identity_providers'),
        token_validity_units=pulumi.get(__response__, 'token_validity_units'),
        write_attributes=pulumi.get(__response__, 'write_attributes')))
