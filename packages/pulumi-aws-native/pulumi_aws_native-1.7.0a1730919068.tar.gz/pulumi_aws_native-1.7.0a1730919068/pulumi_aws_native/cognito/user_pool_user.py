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

__all__ = ['UserPoolUserArgs', 'UserPoolUser']

@pulumi.input_type
class UserPoolUserArgs:
    def __init__(__self__, *,
                 user_pool_id: pulumi.Input[str],
                 client_metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 desired_delivery_mediums: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 force_alias_creation: Optional[pulumi.Input[bool]] = None,
                 message_action: Optional[pulumi.Input[str]] = None,
                 user_attributes: Optional[pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 validation_data: Optional[pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]]] = None):
        """
        The set of arguments for constructing a UserPoolUser resource.
        :param pulumi.Input[str] user_pool_id: The user pool ID for the user pool where the user will be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] client_metadata: A map of custom key-value pairs that you can provide as input for any custom workflows that this action triggers.
               
               You create custom workflows by assigning AWS Lambda functions to user pool triggers. When you use the AdminCreateUser API action, Amazon Cognito invokes the function that is assigned to the *pre sign-up* trigger. When Amazon Cognito invokes this function, it passes a JSON payload, which the function receives as input. This payload contains a `clientMetadata` attribute, which provides the data that you assigned to the ClientMetadata parameter in your AdminCreateUser request. In your function code in AWS Lambda , you can process the `clientMetadata` value to enhance your workflow for your specific needs.
               
               For more information, see [Customizing user pool Workflows with Lambda Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html) in the *Amazon Cognito Developer Guide* .
               
               > When you use the ClientMetadata parameter, remember that Amazon Cognito won't do the following:
               > 
               > - Store the ClientMetadata value. This data is available only to AWS Lambda triggers that are assigned to a user pool to support custom workflows. If your user pool configuration doesn't include triggers, the ClientMetadata parameter serves no purpose.
               > - Validate the ClientMetadata value.
               > - Encrypt the ClientMetadata value. Don't use Amazon Cognito to provide sensitive information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] desired_delivery_mediums: Specify `"EMAIL"` if email will be used to send the welcome message. Specify `"SMS"` if the phone number will be used. The default value is `"SMS"` . You can specify more than one value.
        :param pulumi.Input[bool] force_alias_creation: This parameter is used only if the `phone_number_verified` or `email_verified` attribute is set to `True` . Otherwise, it is ignored.
               
               If this parameter is set to `True` and the phone number or email address specified in the UserAttributes parameter already exists as an alias with a different user, the API call will migrate the alias from the previous user to the newly created user. The previous user will no longer be able to log in using that alias.
               
               If this parameter is set to `False` , the API throws an `AliasExistsException` error if the alias already exists. The default value is `False` .
        :param pulumi.Input[str] message_action: Set to `RESEND` to resend the invitation message to a user that already exists and reset the expiration limit on the user's account. Set to `SUPPRESS` to suppress sending the message. You can specify only one value.
        :param pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]] user_attributes: An array of name-value pairs that contain user attributes and attribute values to be set for the user to be created. You can create a user without specifying any attributes other than `Username` . However, any attributes that you specify as required (when creating a user pool or in the *Attributes* tab of the console) either you should supply (in your call to `AdminCreateUser` ) or the user should supply (when they sign up in response to your welcome message).
               
               For custom attributes, you must prepend the `custom:` prefix to the attribute name.
               
               To send a message inviting the user to sign up, you must specify the user's email address or phone number. You can do this in your call to AdminCreateUser or in the *Users* tab of the Amazon Cognito console for managing your user pools.
               
               In your call to `AdminCreateUser` , you can set the `email_verified` attribute to `True` , and you can set the `phone_number_verified` attribute to `True` . You can also do this by calling [AdminUpdateUserAttributes](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminUpdateUserAttributes.html) .
               
               - *email* : The email address of the user to whom the message that contains the code and username will be sent. Required if the `email_verified` attribute is set to `True` , or if `"EMAIL"` is specified in the `DesiredDeliveryMediums` parameter.
               - *phone_number* : The phone number of the user to whom the message that contains the code and username will be sent. Required if the `phone_number_verified` attribute is set to `True` , or if `"SMS"` is specified in the `DesiredDeliveryMediums` parameter.
        :param pulumi.Input[str] username: The value that you want to set as the username sign-in attribute. The following conditions apply to the username parameter.
               
               - The username can't be a duplicate of another username in the same user pool.
               - You can't change the value of a username after you create it.
               - You can only provide a value if usernames are a valid sign-in attribute for your user pool. If your user pool only supports phone numbers or email addresses as sign-in attributes, Amazon Cognito automatically generates a username value. For more information, see [Customizing sign-in attributes](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases) .
        :param pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]] validation_data: Temporary user attributes that contribute to the outcomes of your pre sign-up Lambda trigger. This set of key-value pairs are for custom validation of information that you collect from your users but don't need to retain.
               
               Your Lambda function can analyze this additional data and act on it. Your function might perform external API operations like logging user attributes and validation data to Amazon CloudWatch Logs. Validation data might also affect the response that your function returns to Amazon Cognito, like automatically confirming the user if they sign up from within your network.
               
               For more information about the pre sign-up Lambda trigger, see [Pre sign-up Lambda trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html) .
        """
        pulumi.set(__self__, "user_pool_id", user_pool_id)
        if client_metadata is not None:
            pulumi.set(__self__, "client_metadata", client_metadata)
        if desired_delivery_mediums is not None:
            pulumi.set(__self__, "desired_delivery_mediums", desired_delivery_mediums)
        if force_alias_creation is not None:
            pulumi.set(__self__, "force_alias_creation", force_alias_creation)
        if message_action is not None:
            pulumi.set(__self__, "message_action", message_action)
        if user_attributes is not None:
            pulumi.set(__self__, "user_attributes", user_attributes)
        if username is not None:
            pulumi.set(__self__, "username", username)
        if validation_data is not None:
            pulumi.set(__self__, "validation_data", validation_data)

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Input[str]:
        """
        The user pool ID for the user pool where the user will be created.
        """
        return pulumi.get(self, "user_pool_id")

    @user_pool_id.setter
    def user_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_pool_id", value)

    @property
    @pulumi.getter(name="clientMetadata")
    def client_metadata(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of custom key-value pairs that you can provide as input for any custom workflows that this action triggers.

        You create custom workflows by assigning AWS Lambda functions to user pool triggers. When you use the AdminCreateUser API action, Amazon Cognito invokes the function that is assigned to the *pre sign-up* trigger. When Amazon Cognito invokes this function, it passes a JSON payload, which the function receives as input. This payload contains a `clientMetadata` attribute, which provides the data that you assigned to the ClientMetadata parameter in your AdminCreateUser request. In your function code in AWS Lambda , you can process the `clientMetadata` value to enhance your workflow for your specific needs.

        For more information, see [Customizing user pool Workflows with Lambda Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html) in the *Amazon Cognito Developer Guide* .

        > When you use the ClientMetadata parameter, remember that Amazon Cognito won't do the following:
        > 
        > - Store the ClientMetadata value. This data is available only to AWS Lambda triggers that are assigned to a user pool to support custom workflows. If your user pool configuration doesn't include triggers, the ClientMetadata parameter serves no purpose.
        > - Validate the ClientMetadata value.
        > - Encrypt the ClientMetadata value. Don't use Amazon Cognito to provide sensitive information.
        """
        return pulumi.get(self, "client_metadata")

    @client_metadata.setter
    def client_metadata(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "client_metadata", value)

    @property
    @pulumi.getter(name="desiredDeliveryMediums")
    def desired_delivery_mediums(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specify `"EMAIL"` if email will be used to send the welcome message. Specify `"SMS"` if the phone number will be used. The default value is `"SMS"` . You can specify more than one value.
        """
        return pulumi.get(self, "desired_delivery_mediums")

    @desired_delivery_mediums.setter
    def desired_delivery_mediums(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "desired_delivery_mediums", value)

    @property
    @pulumi.getter(name="forceAliasCreation")
    def force_alias_creation(self) -> Optional[pulumi.Input[bool]]:
        """
        This parameter is used only if the `phone_number_verified` or `email_verified` attribute is set to `True` . Otherwise, it is ignored.

        If this parameter is set to `True` and the phone number or email address specified in the UserAttributes parameter already exists as an alias with a different user, the API call will migrate the alias from the previous user to the newly created user. The previous user will no longer be able to log in using that alias.

        If this parameter is set to `False` , the API throws an `AliasExistsException` error if the alias already exists. The default value is `False` .
        """
        return pulumi.get(self, "force_alias_creation")

    @force_alias_creation.setter
    def force_alias_creation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_alias_creation", value)

    @property
    @pulumi.getter(name="messageAction")
    def message_action(self) -> Optional[pulumi.Input[str]]:
        """
        Set to `RESEND` to resend the invitation message to a user that already exists and reset the expiration limit on the user's account. Set to `SUPPRESS` to suppress sending the message. You can specify only one value.
        """
        return pulumi.get(self, "message_action")

    @message_action.setter
    def message_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message_action", value)

    @property
    @pulumi.getter(name="userAttributes")
    def user_attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]]]:
        """
        An array of name-value pairs that contain user attributes and attribute values to be set for the user to be created. You can create a user without specifying any attributes other than `Username` . However, any attributes that you specify as required (when creating a user pool or in the *Attributes* tab of the console) either you should supply (in your call to `AdminCreateUser` ) or the user should supply (when they sign up in response to your welcome message).

        For custom attributes, you must prepend the `custom:` prefix to the attribute name.

        To send a message inviting the user to sign up, you must specify the user's email address or phone number. You can do this in your call to AdminCreateUser or in the *Users* tab of the Amazon Cognito console for managing your user pools.

        In your call to `AdminCreateUser` , you can set the `email_verified` attribute to `True` , and you can set the `phone_number_verified` attribute to `True` . You can also do this by calling [AdminUpdateUserAttributes](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminUpdateUserAttributes.html) .

        - *email* : The email address of the user to whom the message that contains the code and username will be sent. Required if the `email_verified` attribute is set to `True` , or if `"EMAIL"` is specified in the `DesiredDeliveryMediums` parameter.
        - *phone_number* : The phone number of the user to whom the message that contains the code and username will be sent. Required if the `phone_number_verified` attribute is set to `True` , or if `"SMS"` is specified in the `DesiredDeliveryMediums` parameter.
        """
        return pulumi.get(self, "user_attributes")

    @user_attributes.setter
    def user_attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]]]):
        pulumi.set(self, "user_attributes", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The value that you want to set as the username sign-in attribute. The following conditions apply to the username parameter.

        - The username can't be a duplicate of another username in the same user pool.
        - You can't change the value of a username after you create it.
        - You can only provide a value if usernames are a valid sign-in attribute for your user pool. If your user pool only supports phone numbers or email addresses as sign-in attributes, Amazon Cognito automatically generates a username value. For more information, see [Customizing sign-in attributes](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases) .
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter(name="validationData")
    def validation_data(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]]]:
        """
        Temporary user attributes that contribute to the outcomes of your pre sign-up Lambda trigger. This set of key-value pairs are for custom validation of information that you collect from your users but don't need to retain.

        Your Lambda function can analyze this additional data and act on it. Your function might perform external API operations like logging user attributes and validation data to Amazon CloudWatch Logs. Validation data might also affect the response that your function returns to Amazon Cognito, like automatically confirming the user if they sign up from within your network.

        For more information about the pre sign-up Lambda trigger, see [Pre sign-up Lambda trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html) .
        """
        return pulumi.get(self, "validation_data")

    @validation_data.setter
    def validation_data(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserPoolUserAttributeTypeArgs']]]]):
        pulumi.set(self, "validation_data", value)


class UserPoolUser(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 desired_delivery_mediums: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 force_alias_creation: Optional[pulumi.Input[bool]] = None,
                 message_action: Optional[pulumi.Input[str]] = None,
                 user_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[Union['UserPoolUserAttributeTypeArgs', 'UserPoolUserAttributeTypeArgsDict']]]]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 validation_data: Optional[pulumi.Input[Sequence[pulumi.Input[Union['UserPoolUserAttributeTypeArgs', 'UserPoolUserAttributeTypeArgsDict']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Cognito::UserPoolUser

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] client_metadata: A map of custom key-value pairs that you can provide as input for any custom workflows that this action triggers.
               
               You create custom workflows by assigning AWS Lambda functions to user pool triggers. When you use the AdminCreateUser API action, Amazon Cognito invokes the function that is assigned to the *pre sign-up* trigger. When Amazon Cognito invokes this function, it passes a JSON payload, which the function receives as input. This payload contains a `clientMetadata` attribute, which provides the data that you assigned to the ClientMetadata parameter in your AdminCreateUser request. In your function code in AWS Lambda , you can process the `clientMetadata` value to enhance your workflow for your specific needs.
               
               For more information, see [Customizing user pool Workflows with Lambda Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html) in the *Amazon Cognito Developer Guide* .
               
               > When you use the ClientMetadata parameter, remember that Amazon Cognito won't do the following:
               > 
               > - Store the ClientMetadata value. This data is available only to AWS Lambda triggers that are assigned to a user pool to support custom workflows. If your user pool configuration doesn't include triggers, the ClientMetadata parameter serves no purpose.
               > - Validate the ClientMetadata value.
               > - Encrypt the ClientMetadata value. Don't use Amazon Cognito to provide sensitive information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] desired_delivery_mediums: Specify `"EMAIL"` if email will be used to send the welcome message. Specify `"SMS"` if the phone number will be used. The default value is `"SMS"` . You can specify more than one value.
        :param pulumi.Input[bool] force_alias_creation: This parameter is used only if the `phone_number_verified` or `email_verified` attribute is set to `True` . Otherwise, it is ignored.
               
               If this parameter is set to `True` and the phone number or email address specified in the UserAttributes parameter already exists as an alias with a different user, the API call will migrate the alias from the previous user to the newly created user. The previous user will no longer be able to log in using that alias.
               
               If this parameter is set to `False` , the API throws an `AliasExistsException` error if the alias already exists. The default value is `False` .
        :param pulumi.Input[str] message_action: Set to `RESEND` to resend the invitation message to a user that already exists and reset the expiration limit on the user's account. Set to `SUPPRESS` to suppress sending the message. You can specify only one value.
        :param pulumi.Input[Sequence[pulumi.Input[Union['UserPoolUserAttributeTypeArgs', 'UserPoolUserAttributeTypeArgsDict']]]] user_attributes: An array of name-value pairs that contain user attributes and attribute values to be set for the user to be created. You can create a user without specifying any attributes other than `Username` . However, any attributes that you specify as required (when creating a user pool or in the *Attributes* tab of the console) either you should supply (in your call to `AdminCreateUser` ) or the user should supply (when they sign up in response to your welcome message).
               
               For custom attributes, you must prepend the `custom:` prefix to the attribute name.
               
               To send a message inviting the user to sign up, you must specify the user's email address or phone number. You can do this in your call to AdminCreateUser or in the *Users* tab of the Amazon Cognito console for managing your user pools.
               
               In your call to `AdminCreateUser` , you can set the `email_verified` attribute to `True` , and you can set the `phone_number_verified` attribute to `True` . You can also do this by calling [AdminUpdateUserAttributes](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminUpdateUserAttributes.html) .
               
               - *email* : The email address of the user to whom the message that contains the code and username will be sent. Required if the `email_verified` attribute is set to `True` , or if `"EMAIL"` is specified in the `DesiredDeliveryMediums` parameter.
               - *phone_number* : The phone number of the user to whom the message that contains the code and username will be sent. Required if the `phone_number_verified` attribute is set to `True` , or if `"SMS"` is specified in the `DesiredDeliveryMediums` parameter.
        :param pulumi.Input[str] user_pool_id: The user pool ID for the user pool where the user will be created.
        :param pulumi.Input[str] username: The value that you want to set as the username sign-in attribute. The following conditions apply to the username parameter.
               
               - The username can't be a duplicate of another username in the same user pool.
               - You can't change the value of a username after you create it.
               - You can only provide a value if usernames are a valid sign-in attribute for your user pool. If your user pool only supports phone numbers or email addresses as sign-in attributes, Amazon Cognito automatically generates a username value. For more information, see [Customizing sign-in attributes](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases) .
        :param pulumi.Input[Sequence[pulumi.Input[Union['UserPoolUserAttributeTypeArgs', 'UserPoolUserAttributeTypeArgsDict']]]] validation_data: Temporary user attributes that contribute to the outcomes of your pre sign-up Lambda trigger. This set of key-value pairs are for custom validation of information that you collect from your users but don't need to retain.
               
               Your Lambda function can analyze this additional data and act on it. Your function might perform external API operations like logging user attributes and validation data to Amazon CloudWatch Logs. Validation data might also affect the response that your function returns to Amazon Cognito, like automatically confirming the user if they sign up from within your network.
               
               For more information about the pre sign-up Lambda trigger, see [Pre sign-up Lambda trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html) .
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserPoolUserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Cognito::UserPoolUser

        :param str resource_name: The name of the resource.
        :param UserPoolUserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserPoolUserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 desired_delivery_mediums: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 force_alias_creation: Optional[pulumi.Input[bool]] = None,
                 message_action: Optional[pulumi.Input[str]] = None,
                 user_attributes: Optional[pulumi.Input[Sequence[pulumi.Input[Union['UserPoolUserAttributeTypeArgs', 'UserPoolUserAttributeTypeArgsDict']]]]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 validation_data: Optional[pulumi.Input[Sequence[pulumi.Input[Union['UserPoolUserAttributeTypeArgs', 'UserPoolUserAttributeTypeArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserPoolUserArgs.__new__(UserPoolUserArgs)

            __props__.__dict__["client_metadata"] = client_metadata
            __props__.__dict__["desired_delivery_mediums"] = desired_delivery_mediums
            __props__.__dict__["force_alias_creation"] = force_alias_creation
            __props__.__dict__["message_action"] = message_action
            __props__.__dict__["user_attributes"] = user_attributes
            if user_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_pool_id'")
            __props__.__dict__["user_pool_id"] = user_pool_id
            __props__.__dict__["username"] = username
            __props__.__dict__["validation_data"] = validation_data
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["clientMetadata.*", "desiredDeliveryMediums[*]", "forceAliasCreation", "messageAction", "userAttributes[*]", "userPoolId", "username", "validationData[*]"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(UserPoolUser, __self__).__init__(
            'aws-native:cognito:UserPoolUser',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'UserPoolUser':
        """
        Get an existing UserPoolUser resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = UserPoolUserArgs.__new__(UserPoolUserArgs)

        __props__.__dict__["client_metadata"] = None
        __props__.__dict__["desired_delivery_mediums"] = None
        __props__.__dict__["force_alias_creation"] = None
        __props__.__dict__["message_action"] = None
        __props__.__dict__["user_attributes"] = None
        __props__.__dict__["user_pool_id"] = None
        __props__.__dict__["username"] = None
        __props__.__dict__["validation_data"] = None
        return UserPoolUser(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clientMetadata")
    def client_metadata(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of custom key-value pairs that you can provide as input for any custom workflows that this action triggers.

        You create custom workflows by assigning AWS Lambda functions to user pool triggers. When you use the AdminCreateUser API action, Amazon Cognito invokes the function that is assigned to the *pre sign-up* trigger. When Amazon Cognito invokes this function, it passes a JSON payload, which the function receives as input. This payload contains a `clientMetadata` attribute, which provides the data that you assigned to the ClientMetadata parameter in your AdminCreateUser request. In your function code in AWS Lambda , you can process the `clientMetadata` value to enhance your workflow for your specific needs.

        For more information, see [Customizing user pool Workflows with Lambda Triggers](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html) in the *Amazon Cognito Developer Guide* .

        > When you use the ClientMetadata parameter, remember that Amazon Cognito won't do the following:
        > 
        > - Store the ClientMetadata value. This data is available only to AWS Lambda triggers that are assigned to a user pool to support custom workflows. If your user pool configuration doesn't include triggers, the ClientMetadata parameter serves no purpose.
        > - Validate the ClientMetadata value.
        > - Encrypt the ClientMetadata value. Don't use Amazon Cognito to provide sensitive information.
        """
        return pulumi.get(self, "client_metadata")

    @property
    @pulumi.getter(name="desiredDeliveryMediums")
    def desired_delivery_mediums(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specify `"EMAIL"` if email will be used to send the welcome message. Specify `"SMS"` if the phone number will be used. The default value is `"SMS"` . You can specify more than one value.
        """
        return pulumi.get(self, "desired_delivery_mediums")

    @property
    @pulumi.getter(name="forceAliasCreation")
    def force_alias_creation(self) -> pulumi.Output[Optional[bool]]:
        """
        This parameter is used only if the `phone_number_verified` or `email_verified` attribute is set to `True` . Otherwise, it is ignored.

        If this parameter is set to `True` and the phone number or email address specified in the UserAttributes parameter already exists as an alias with a different user, the API call will migrate the alias from the previous user to the newly created user. The previous user will no longer be able to log in using that alias.

        If this parameter is set to `False` , the API throws an `AliasExistsException` error if the alias already exists. The default value is `False` .
        """
        return pulumi.get(self, "force_alias_creation")

    @property
    @pulumi.getter(name="messageAction")
    def message_action(self) -> pulumi.Output[Optional[str]]:
        """
        Set to `RESEND` to resend the invitation message to a user that already exists and reset the expiration limit on the user's account. Set to `SUPPRESS` to suppress sending the message. You can specify only one value.
        """
        return pulumi.get(self, "message_action")

    @property
    @pulumi.getter(name="userAttributes")
    def user_attributes(self) -> pulumi.Output[Optional[Sequence['outputs.UserPoolUserAttributeType']]]:
        """
        An array of name-value pairs that contain user attributes and attribute values to be set for the user to be created. You can create a user without specifying any attributes other than `Username` . However, any attributes that you specify as required (when creating a user pool or in the *Attributes* tab of the console) either you should supply (in your call to `AdminCreateUser` ) or the user should supply (when they sign up in response to your welcome message).

        For custom attributes, you must prepend the `custom:` prefix to the attribute name.

        To send a message inviting the user to sign up, you must specify the user's email address or phone number. You can do this in your call to AdminCreateUser or in the *Users* tab of the Amazon Cognito console for managing your user pools.

        In your call to `AdminCreateUser` , you can set the `email_verified` attribute to `True` , and you can set the `phone_number_verified` attribute to `True` . You can also do this by calling [AdminUpdateUserAttributes](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_AdminUpdateUserAttributes.html) .

        - *email* : The email address of the user to whom the message that contains the code and username will be sent. Required if the `email_verified` attribute is set to `True` , or if `"EMAIL"` is specified in the `DesiredDeliveryMediums` parameter.
        - *phone_number* : The phone number of the user to whom the message that contains the code and username will be sent. Required if the `phone_number_verified` attribute is set to `True` , or if `"SMS"` is specified in the `DesiredDeliveryMediums` parameter.
        """
        return pulumi.get(self, "user_attributes")

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Output[str]:
        """
        The user pool ID for the user pool where the user will be created.
        """
        return pulumi.get(self, "user_pool_id")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[Optional[str]]:
        """
        The value that you want to set as the username sign-in attribute. The following conditions apply to the username parameter.

        - The username can't be a duplicate of another username in the same user pool.
        - You can't change the value of a username after you create it.
        - You can only provide a value if usernames are a valid sign-in attribute for your user pool. If your user pool only supports phone numbers or email addresses as sign-in attributes, Amazon Cognito automatically generates a username value. For more information, see [Customizing sign-in attributes](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#user-pool-settings-aliases) .
        """
        return pulumi.get(self, "username")

    @property
    @pulumi.getter(name="validationData")
    def validation_data(self) -> pulumi.Output[Optional[Sequence['outputs.UserPoolUserAttributeType']]]:
        """
        Temporary user attributes that contribute to the outcomes of your pre sign-up Lambda trigger. This set of key-value pairs are for custom validation of information that you collect from your users but don't need to retain.

        Your Lambda function can analyze this additional data and act on it. Your function might perform external API operations like logging user attributes and validation data to Amazon CloudWatch Logs. Validation data might also affect the response that your function returns to Amazon Cognito, like automatically confirming the user if they sign up from within your network.

        For more information about the pre sign-up Lambda trigger, see [Pre sign-up Lambda trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html) .
        """
        return pulumi.get(self, "validation_data")

