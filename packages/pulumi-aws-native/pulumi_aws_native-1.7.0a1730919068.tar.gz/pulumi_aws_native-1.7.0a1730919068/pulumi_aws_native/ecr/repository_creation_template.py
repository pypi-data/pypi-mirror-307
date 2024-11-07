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
from ._enums import *
from ._inputs import *

__all__ = ['RepositoryCreationTemplateArgs', 'RepositoryCreationTemplate']

@pulumi.input_type
class RepositoryCreationTemplateArgs:
    def __init__(__self__, *,
                 applied_for: pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]],
                 prefix: pulumi.Input[str],
                 custom_role_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input['RepositoryCreationTemplateEncryptionConfigurationArgs']] = None,
                 image_tag_mutability: Optional[pulumi.Input['RepositoryCreationTemplateImageTagMutability']] = None,
                 lifecycle_policy: Optional[pulumi.Input[str]] = None,
                 repository_policy: Optional[pulumi.Input[str]] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateTagArgs']]]] = None):
        """
        The set of arguments for constructing a RepositoryCreationTemplate resource.
        :param pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]] applied_for: A list of enumerable Strings representing the repository creation scenarios that the template will apply towards.
        :param pulumi.Input[str] prefix: The prefix use to match the repository name and apply the template.
        :param pulumi.Input[str] custom_role_arn: The ARN of the role to be assumed by ECR. This role must be in the same account as the registry that you are configuring.
        :param pulumi.Input[str] description: The description of the template.
        :param pulumi.Input['RepositoryCreationTemplateEncryptionConfigurationArgs'] encryption_configuration: The encryption configuration associated with the repository creation template.
        :param pulumi.Input['RepositoryCreationTemplateImageTagMutability'] image_tag_mutability: The image tag mutability setting for the repository.
        :param pulumi.Input[str] lifecycle_policy: The JSON lifecycle policy text to apply to the repository. For information about lifecycle policy syntax, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html
        :param pulumi.Input[str] repository_policy: The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html
        :param pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateTagArgs']]] resource_tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "applied_for", applied_for)
        pulumi.set(__self__, "prefix", prefix)
        if custom_role_arn is not None:
            pulumi.set(__self__, "custom_role_arn", custom_role_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encryption_configuration is not None:
            pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        if image_tag_mutability is not None:
            pulumi.set(__self__, "image_tag_mutability", image_tag_mutability)
        if lifecycle_policy is not None:
            pulumi.set(__self__, "lifecycle_policy", lifecycle_policy)
        if repository_policy is not None:
            pulumi.set(__self__, "repository_policy", repository_policy)
        if resource_tags is not None:
            pulumi.set(__self__, "resource_tags", resource_tags)

    @property
    @pulumi.getter(name="appliedFor")
    def applied_for(self) -> pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]]:
        """
        A list of enumerable Strings representing the repository creation scenarios that the template will apply towards.
        """
        return pulumi.get(self, "applied_for")

    @applied_for.setter
    def applied_for(self, value: pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]]):
        pulumi.set(self, "applied_for", value)

    @property
    @pulumi.getter
    def prefix(self) -> pulumi.Input[str]:
        """
        The prefix use to match the repository name and apply the template.
        """
        return pulumi.get(self, "prefix")

    @prefix.setter
    def prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "prefix", value)

    @property
    @pulumi.getter(name="customRoleArn")
    def custom_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the role to be assumed by ECR. This role must be in the same account as the registry that you are configuring.
        """
        return pulumi.get(self, "custom_role_arn")

    @custom_role_arn.setter
    def custom_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_role_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the template.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> Optional[pulumi.Input['RepositoryCreationTemplateEncryptionConfigurationArgs']]:
        """
        The encryption configuration associated with the repository creation template.
        """
        return pulumi.get(self, "encryption_configuration")

    @encryption_configuration.setter
    def encryption_configuration(self, value: Optional[pulumi.Input['RepositoryCreationTemplateEncryptionConfigurationArgs']]):
        pulumi.set(self, "encryption_configuration", value)

    @property
    @pulumi.getter(name="imageTagMutability")
    def image_tag_mutability(self) -> Optional[pulumi.Input['RepositoryCreationTemplateImageTagMutability']]:
        """
        The image tag mutability setting for the repository.
        """
        return pulumi.get(self, "image_tag_mutability")

    @image_tag_mutability.setter
    def image_tag_mutability(self, value: Optional[pulumi.Input['RepositoryCreationTemplateImageTagMutability']]):
        pulumi.set(self, "image_tag_mutability", value)

    @property
    @pulumi.getter(name="lifecyclePolicy")
    def lifecycle_policy(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON lifecycle policy text to apply to the repository. For information about lifecycle policy syntax, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html
        """
        return pulumi.get(self, "lifecycle_policy")

    @lifecycle_policy.setter
    def lifecycle_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lifecycle_policy", value)

    @property
    @pulumi.getter(name="repositoryPolicy")
    def repository_policy(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html
        """
        return pulumi.get(self, "repository_policy")

    @repository_policy.setter
    def repository_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository_policy", value)

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "resource_tags")

    @resource_tags.setter
    def resource_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateTagArgs']]]]):
        pulumi.set(self, "resource_tags", value)


class RepositoryCreationTemplate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 applied_for: Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]]] = None,
                 custom_role_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input[Union['RepositoryCreationTemplateEncryptionConfigurationArgs', 'RepositoryCreationTemplateEncryptionConfigurationArgsDict']]] = None,
                 image_tag_mutability: Optional[pulumi.Input['RepositoryCreationTemplateImageTagMutability']] = None,
                 lifecycle_policy: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
                 repository_policy: Optional[pulumi.Input[str]] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RepositoryCreationTemplateTagArgs', 'RepositoryCreationTemplateTagArgsDict']]]]] = None,
                 __props__=None):
        """
        AWS::ECR::RepositoryCreationTemplate is used to create repository with configuration from a pre-defined template.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]] applied_for: A list of enumerable Strings representing the repository creation scenarios that the template will apply towards.
        :param pulumi.Input[str] custom_role_arn: The ARN of the role to be assumed by ECR. This role must be in the same account as the registry that you are configuring.
        :param pulumi.Input[str] description: The description of the template.
        :param pulumi.Input[Union['RepositoryCreationTemplateEncryptionConfigurationArgs', 'RepositoryCreationTemplateEncryptionConfigurationArgsDict']] encryption_configuration: The encryption configuration associated with the repository creation template.
        :param pulumi.Input['RepositoryCreationTemplateImageTagMutability'] image_tag_mutability: The image tag mutability setting for the repository.
        :param pulumi.Input[str] lifecycle_policy: The JSON lifecycle policy text to apply to the repository. For information about lifecycle policy syntax, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html
        :param pulumi.Input[str] prefix: The prefix use to match the repository name and apply the template.
        :param pulumi.Input[str] repository_policy: The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html
        :param pulumi.Input[Sequence[pulumi.Input[Union['RepositoryCreationTemplateTagArgs', 'RepositoryCreationTemplateTagArgsDict']]]] resource_tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RepositoryCreationTemplateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        AWS::ECR::RepositoryCreationTemplate is used to create repository with configuration from a pre-defined template.

        :param str resource_name: The name of the resource.
        :param RepositoryCreationTemplateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RepositoryCreationTemplateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 applied_for: Optional[pulumi.Input[Sequence[pulumi.Input['RepositoryCreationTemplateAppliedForItem']]]] = None,
                 custom_role_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input[Union['RepositoryCreationTemplateEncryptionConfigurationArgs', 'RepositoryCreationTemplateEncryptionConfigurationArgsDict']]] = None,
                 image_tag_mutability: Optional[pulumi.Input['RepositoryCreationTemplateImageTagMutability']] = None,
                 lifecycle_policy: Optional[pulumi.Input[str]] = None,
                 prefix: Optional[pulumi.Input[str]] = None,
                 repository_policy: Optional[pulumi.Input[str]] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RepositoryCreationTemplateTagArgs', 'RepositoryCreationTemplateTagArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RepositoryCreationTemplateArgs.__new__(RepositoryCreationTemplateArgs)

            if applied_for is None and not opts.urn:
                raise TypeError("Missing required property 'applied_for'")
            __props__.__dict__["applied_for"] = applied_for
            __props__.__dict__["custom_role_arn"] = custom_role_arn
            __props__.__dict__["description"] = description
            __props__.__dict__["encryption_configuration"] = encryption_configuration
            __props__.__dict__["image_tag_mutability"] = image_tag_mutability
            __props__.__dict__["lifecycle_policy"] = lifecycle_policy
            if prefix is None and not opts.urn:
                raise TypeError("Missing required property 'prefix'")
            __props__.__dict__["prefix"] = prefix
            __props__.__dict__["repository_policy"] = repository_policy
            __props__.__dict__["resource_tags"] = resource_tags
            __props__.__dict__["created_at"] = None
            __props__.__dict__["updated_at"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["prefix"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(RepositoryCreationTemplate, __self__).__init__(
            'aws-native:ecr:RepositoryCreationTemplate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RepositoryCreationTemplate':
        """
        Get an existing RepositoryCreationTemplate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RepositoryCreationTemplateArgs.__new__(RepositoryCreationTemplateArgs)

        __props__.__dict__["applied_for"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["custom_role_arn"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["encryption_configuration"] = None
        __props__.__dict__["image_tag_mutability"] = None
        __props__.__dict__["lifecycle_policy"] = None
        __props__.__dict__["prefix"] = None
        __props__.__dict__["repository_policy"] = None
        __props__.__dict__["resource_tags"] = None
        __props__.__dict__["updated_at"] = None
        return RepositoryCreationTemplate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appliedFor")
    def applied_for(self) -> pulumi.Output[Sequence['RepositoryCreationTemplateAppliedForItem']]:
        """
        A list of enumerable Strings representing the repository creation scenarios that the template will apply towards.
        """
        return pulumi.get(self, "applied_for")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Create timestamp of the template.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="customRoleArn")
    def custom_role_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of the role to be assumed by ECR. This role must be in the same account as the registry that you are configuring.
        """
        return pulumi.get(self, "custom_role_arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the template.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> pulumi.Output[Optional['outputs.RepositoryCreationTemplateEncryptionConfiguration']]:
        """
        The encryption configuration associated with the repository creation template.
        """
        return pulumi.get(self, "encryption_configuration")

    @property
    @pulumi.getter(name="imageTagMutability")
    def image_tag_mutability(self) -> pulumi.Output[Optional['RepositoryCreationTemplateImageTagMutability']]:
        """
        The image tag mutability setting for the repository.
        """
        return pulumi.get(self, "image_tag_mutability")

    @property
    @pulumi.getter(name="lifecyclePolicy")
    def lifecycle_policy(self) -> pulumi.Output[Optional[str]]:
        """
        The JSON lifecycle policy text to apply to the repository. For information about lifecycle policy syntax, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html
        """
        return pulumi.get(self, "lifecycle_policy")

    @property
    @pulumi.getter
    def prefix(self) -> pulumi.Output[str]:
        """
        The prefix use to match the repository name and apply the template.
        """
        return pulumi.get(self, "prefix")

    @property
    @pulumi.getter(name="repositoryPolicy")
    def repository_policy(self) -> pulumi.Output[Optional[str]]:
        """
        The JSON repository policy text to apply to the repository. For more information, see https://docs.aws.amazon.com/AmazonECR/latest/userguide/RepositoryPolicyExamples.html
        """
        return pulumi.get(self, "repository_policy")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> pulumi.Output[Optional[Sequence['outputs.RepositoryCreationTemplateTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "resource_tags")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        Update timestamp of the template.
        """
        return pulumi.get(self, "updated_at")

