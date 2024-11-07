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
    'AppEventSubscriptionArgs',
    'AppEventSubscriptionArgsDict',
    'AppPermissionModelArgs',
    'AppPermissionModelArgsDict',
    'AppPhysicalResourceIdArgs',
    'AppPhysicalResourceIdArgsDict',
    'AppResourceMappingArgs',
    'AppResourceMappingArgsDict',
    'ResiliencyPolicyFailurePolicyArgs',
    'ResiliencyPolicyFailurePolicyArgsDict',
    'ResiliencyPolicyPolicyMapArgs',
    'ResiliencyPolicyPolicyMapArgsDict',
]

MYPY = False

if not MYPY:
    class AppEventSubscriptionArgsDict(TypedDict):
        """
        Indicates an event you would like to subscribe and get notification for.
        """
        event_type: pulumi.Input['AppEventSubscriptionEventType']
        """
        The type of event you would like to subscribe and get notification for.
        """
        name: pulumi.Input[str]
        """
        Unique name to identify an event subscription.
        """
        sns_topic_arn: NotRequired[pulumi.Input[str]]
        """
        Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic.
        """
elif False:
    AppEventSubscriptionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppEventSubscriptionArgs:
    def __init__(__self__, *,
                 event_type: pulumi.Input['AppEventSubscriptionEventType'],
                 name: pulumi.Input[str],
                 sns_topic_arn: Optional[pulumi.Input[str]] = None):
        """
        Indicates an event you would like to subscribe and get notification for.
        :param pulumi.Input['AppEventSubscriptionEventType'] event_type: The type of event you would like to subscribe and get notification for.
        :param pulumi.Input[str] name: Unique name to identify an event subscription.
        :param pulumi.Input[str] sns_topic_arn: Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic.
        """
        pulumi.set(__self__, "event_type", event_type)
        pulumi.set(__self__, "name", name)
        if sns_topic_arn is not None:
            pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> pulumi.Input['AppEventSubscriptionEventType']:
        """
        The type of event you would like to subscribe and get notification for.
        """
        return pulumi.get(self, "event_type")

    @event_type.setter
    def event_type(self, value: pulumi.Input['AppEventSubscriptionEventType']):
        pulumi.set(self, "event_type", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name to identify an event subscription.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic.
        """
        return pulumi.get(self, "sns_topic_arn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sns_topic_arn", value)


if not MYPY:
    class AppPermissionModelArgsDict(TypedDict):
        """
        Defines the roles and credentials that AWS Resilience Hub would use while creating the application, importing its resources, and running an assessment.
        """
        type: pulumi.Input['AppPermissionModelType']
        """
        Defines how AWS Resilience Hub scans your resources. It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.
        """
        cross_account_role_arns: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts. These ARNs are used for querying purposes while importing resources and assessing your application.
        """
        invoker_role_name: NotRequired[pulumi.Input[str]]
        """
        Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment.
        """
elif False:
    AppPermissionModelArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppPermissionModelArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['AppPermissionModelType'],
                 cross_account_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 invoker_role_name: Optional[pulumi.Input[str]] = None):
        """
        Defines the roles and credentials that AWS Resilience Hub would use while creating the application, importing its resources, and running an assessment.
        :param pulumi.Input['AppPermissionModelType'] type: Defines how AWS Resilience Hub scans your resources. It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] cross_account_role_arns: Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts. These ARNs are used for querying purposes while importing resources and assessing your application.
        :param pulumi.Input[str] invoker_role_name: Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment.
        """
        pulumi.set(__self__, "type", type)
        if cross_account_role_arns is not None:
            pulumi.set(__self__, "cross_account_role_arns", cross_account_role_arns)
        if invoker_role_name is not None:
            pulumi.set(__self__, "invoker_role_name", invoker_role_name)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['AppPermissionModelType']:
        """
        Defines how AWS Resilience Hub scans your resources. It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['AppPermissionModelType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="crossAccountRoleArns")
    def cross_account_role_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts. These ARNs are used for querying purposes while importing resources and assessing your application.
        """
        return pulumi.get(self, "cross_account_role_arns")

    @cross_account_role_arns.setter
    def cross_account_role_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "cross_account_role_arns", value)

    @property
    @pulumi.getter(name="invokerRoleName")
    def invoker_role_name(self) -> Optional[pulumi.Input[str]]:
        """
        Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment.
        """
        return pulumi.get(self, "invoker_role_name")

    @invoker_role_name.setter
    def invoker_role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invoker_role_name", value)


if not MYPY:
    class AppPhysicalResourceIdArgsDict(TypedDict):
        identifier: pulumi.Input[str]
        """
        Identifier of the physical resource.
        """
        type: pulumi.Input[str]
        """
        Specifies the type of physical resource identifier.

        - **Arn** - The resource identifier is an Amazon Resource Name (ARN) and it can identify the following list of resources:

        - `AWS::ECS::Service`
        - `AWS::EFS::FileSystem`
        - `AWS::ElasticLoadBalancingV2::LoadBalancer`
        - `AWS::Lambda::Function`
        - `AWS::SNS::Topic`
        - **Native** - The resource identifier is an AWS Resilience Hub -native identifier and it can identify the following list of resources:

        - `AWS::ApiGateway::RestApi`
        - `AWS::ApiGatewayV2::Api`
        - `AWS::AutoScaling::AutoScalingGroup`
        - `AWS::DocDB::DBCluster`
        - `AWS::DocDB::DBGlobalCluster`
        - `AWS::DocDB::DBInstance`
        - `AWS::DynamoDB::GlobalTable`
        - `AWS::DynamoDB::Table`
        - `AWS::EC2::EC2Fleet`
        - `AWS::EC2::Instance`
        - `AWS::EC2::NatGateway`
        - `AWS::EC2::Volume`
        - `AWS::ElasticLoadBalancing::LoadBalancer`
        - `AWS::RDS::DBCluster`
        - `AWS::RDS::DBInstance`
        - `AWS::RDS::GlobalCluster`
        - `AWS::Route53::RecordSet`
        - `AWS::S3::Bucket`
        - `AWS::SQS::Queue`
        """
        aws_account_id: NotRequired[pulumi.Input[str]]
        """
        The AWS account that owns the physical resource.
        """
        aws_region: NotRequired[pulumi.Input[str]]
        """
        The AWS Region that the physical resource is located in.
        """
elif False:
    AppPhysicalResourceIdArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppPhysicalResourceIdArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 type: pulumi.Input[str],
                 aws_account_id: Optional[pulumi.Input[str]] = None,
                 aws_region: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] identifier: Identifier of the physical resource.
        :param pulumi.Input[str] type: Specifies the type of physical resource identifier.
               
               - **Arn** - The resource identifier is an Amazon Resource Name (ARN) and it can identify the following list of resources:
               
               - `AWS::ECS::Service`
               - `AWS::EFS::FileSystem`
               - `AWS::ElasticLoadBalancingV2::LoadBalancer`
               - `AWS::Lambda::Function`
               - `AWS::SNS::Topic`
               - **Native** - The resource identifier is an AWS Resilience Hub -native identifier and it can identify the following list of resources:
               
               - `AWS::ApiGateway::RestApi`
               - `AWS::ApiGatewayV2::Api`
               - `AWS::AutoScaling::AutoScalingGroup`
               - `AWS::DocDB::DBCluster`
               - `AWS::DocDB::DBGlobalCluster`
               - `AWS::DocDB::DBInstance`
               - `AWS::DynamoDB::GlobalTable`
               - `AWS::DynamoDB::Table`
               - `AWS::EC2::EC2Fleet`
               - `AWS::EC2::Instance`
               - `AWS::EC2::NatGateway`
               - `AWS::EC2::Volume`
               - `AWS::ElasticLoadBalancing::LoadBalancer`
               - `AWS::RDS::DBCluster`
               - `AWS::RDS::DBInstance`
               - `AWS::RDS::GlobalCluster`
               - `AWS::Route53::RecordSet`
               - `AWS::S3::Bucket`
               - `AWS::SQS::Queue`
        :param pulumi.Input[str] aws_account_id: The AWS account that owns the physical resource.
        :param pulumi.Input[str] aws_region: The AWS Region that the physical resource is located in.
        """
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "type", type)
        if aws_account_id is not None:
            pulumi.set(__self__, "aws_account_id", aws_account_id)
        if aws_region is not None:
            pulumi.set(__self__, "aws_region", aws_region)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        """
        Identifier of the physical resource.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Specifies the type of physical resource identifier.

        - **Arn** - The resource identifier is an Amazon Resource Name (ARN) and it can identify the following list of resources:

        - `AWS::ECS::Service`
        - `AWS::EFS::FileSystem`
        - `AWS::ElasticLoadBalancingV2::LoadBalancer`
        - `AWS::Lambda::Function`
        - `AWS::SNS::Topic`
        - **Native** - The resource identifier is an AWS Resilience Hub -native identifier and it can identify the following list of resources:

        - `AWS::ApiGateway::RestApi`
        - `AWS::ApiGatewayV2::Api`
        - `AWS::AutoScaling::AutoScalingGroup`
        - `AWS::DocDB::DBCluster`
        - `AWS::DocDB::DBGlobalCluster`
        - `AWS::DocDB::DBInstance`
        - `AWS::DynamoDB::GlobalTable`
        - `AWS::DynamoDB::Table`
        - `AWS::EC2::EC2Fleet`
        - `AWS::EC2::Instance`
        - `AWS::EC2::NatGateway`
        - `AWS::EC2::Volume`
        - `AWS::ElasticLoadBalancing::LoadBalancer`
        - `AWS::RDS::DBCluster`
        - `AWS::RDS::DBInstance`
        - `AWS::RDS::GlobalCluster`
        - `AWS::Route53::RecordSet`
        - `AWS::S3::Bucket`
        - `AWS::SQS::Queue`
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS account that owns the physical resource.
        """
        return pulumi.get(self, "aws_account_id")

    @aws_account_id.setter
    def aws_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_account_id", value)

    @property
    @pulumi.getter(name="awsRegion")
    def aws_region(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS Region that the physical resource is located in.
        """
        return pulumi.get(self, "aws_region")

    @aws_region.setter
    def aws_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aws_region", value)


if not MYPY:
    class AppResourceMappingArgsDict(TypedDict):
        """
        Resource mapping is used to map logical resources from template to physical resource
        """
        mapping_type: pulumi.Input[str]
        """
        Specifies the type of resource mapping.
        """
        physical_resource_id: pulumi.Input['AppPhysicalResourceIdArgsDict']
        """
        Identifier of the physical resource.
        """
        eks_source_name: NotRequired[pulumi.Input[str]]
        """
        Name of the Amazon Elastic Kubernetes Service cluster and namespace that this resource is mapped to when the `mappingType` is `EKS` .

        > This parameter accepts values in "eks-cluster/namespace" format.
        """
        logical_stack_name: NotRequired[pulumi.Input[str]]
        """
        Name of the AWS CloudFormation stack this resource is mapped to when the `mappingType` is `CfnStack` .
        """
        resource_name: NotRequired[pulumi.Input[str]]
        """
        Name of the resource that this resource is mapped to when the `mappingType` is `Resource` .
        """
        terraform_source_name: NotRequired[pulumi.Input[str]]
        """
        Name of the Terraform source that this resource is mapped to when the `mappingType` is `Terraform` .
        """
elif False:
    AppResourceMappingArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class AppResourceMappingArgs:
    def __init__(__self__, *,
                 mapping_type: pulumi.Input[str],
                 physical_resource_id: pulumi.Input['AppPhysicalResourceIdArgs'],
                 eks_source_name: Optional[pulumi.Input[str]] = None,
                 logical_stack_name: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 terraform_source_name: Optional[pulumi.Input[str]] = None):
        """
        Resource mapping is used to map logical resources from template to physical resource
        :param pulumi.Input[str] mapping_type: Specifies the type of resource mapping.
        :param pulumi.Input['AppPhysicalResourceIdArgs'] physical_resource_id: Identifier of the physical resource.
        :param pulumi.Input[str] eks_source_name: Name of the Amazon Elastic Kubernetes Service cluster and namespace that this resource is mapped to when the `mappingType` is `EKS` .
               
               > This parameter accepts values in "eks-cluster/namespace" format.
        :param pulumi.Input[str] logical_stack_name: Name of the AWS CloudFormation stack this resource is mapped to when the `mappingType` is `CfnStack` .
        :param pulumi.Input[str] resource_name: Name of the resource that this resource is mapped to when the `mappingType` is `Resource` .
        :param pulumi.Input[str] terraform_source_name: Name of the Terraform source that this resource is mapped to when the `mappingType` is `Terraform` .
        """
        pulumi.set(__self__, "mapping_type", mapping_type)
        pulumi.set(__self__, "physical_resource_id", physical_resource_id)
        if eks_source_name is not None:
            pulumi.set(__self__, "eks_source_name", eks_source_name)
        if logical_stack_name is not None:
            pulumi.set(__self__, "logical_stack_name", logical_stack_name)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if terraform_source_name is not None:
            pulumi.set(__self__, "terraform_source_name", terraform_source_name)

    @property
    @pulumi.getter(name="mappingType")
    def mapping_type(self) -> pulumi.Input[str]:
        """
        Specifies the type of resource mapping.
        """
        return pulumi.get(self, "mapping_type")

    @mapping_type.setter
    def mapping_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "mapping_type", value)

    @property
    @pulumi.getter(name="physicalResourceId")
    def physical_resource_id(self) -> pulumi.Input['AppPhysicalResourceIdArgs']:
        """
        Identifier of the physical resource.
        """
        return pulumi.get(self, "physical_resource_id")

    @physical_resource_id.setter
    def physical_resource_id(self, value: pulumi.Input['AppPhysicalResourceIdArgs']):
        pulumi.set(self, "physical_resource_id", value)

    @property
    @pulumi.getter(name="eksSourceName")
    def eks_source_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Amazon Elastic Kubernetes Service cluster and namespace that this resource is mapped to when the `mappingType` is `EKS` .

        > This parameter accepts values in "eks-cluster/namespace" format.
        """
        return pulumi.get(self, "eks_source_name")

    @eks_source_name.setter
    def eks_source_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "eks_source_name", value)

    @property
    @pulumi.getter(name="logicalStackName")
    def logical_stack_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the AWS CloudFormation stack this resource is mapped to when the `mappingType` is `CfnStack` .
        """
        return pulumi.get(self, "logical_stack_name")

    @logical_stack_name.setter
    def logical_stack_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "logical_stack_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource that this resource is mapped to when the `mappingType` is `Resource` .
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="terraformSourceName")
    def terraform_source_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Terraform source that this resource is mapped to when the `mappingType` is `Terraform` .
        """
        return pulumi.get(self, "terraform_source_name")

    @terraform_source_name.setter
    def terraform_source_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "terraform_source_name", value)


if not MYPY:
    class ResiliencyPolicyFailurePolicyArgsDict(TypedDict):
        """
        Failure Policy.
        """
        rpo_in_secs: pulumi.Input[int]
        """
        RPO in seconds.
        """
        rto_in_secs: pulumi.Input[int]
        """
        RTO in seconds.
        """
elif False:
    ResiliencyPolicyFailurePolicyArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ResiliencyPolicyFailurePolicyArgs:
    def __init__(__self__, *,
                 rpo_in_secs: pulumi.Input[int],
                 rto_in_secs: pulumi.Input[int]):
        """
        Failure Policy.
        :param pulumi.Input[int] rpo_in_secs: RPO in seconds.
        :param pulumi.Input[int] rto_in_secs: RTO in seconds.
        """
        pulumi.set(__self__, "rpo_in_secs", rpo_in_secs)
        pulumi.set(__self__, "rto_in_secs", rto_in_secs)

    @property
    @pulumi.getter(name="rpoInSecs")
    def rpo_in_secs(self) -> pulumi.Input[int]:
        """
        RPO in seconds.
        """
        return pulumi.get(self, "rpo_in_secs")

    @rpo_in_secs.setter
    def rpo_in_secs(self, value: pulumi.Input[int]):
        pulumi.set(self, "rpo_in_secs", value)

    @property
    @pulumi.getter(name="rtoInSecs")
    def rto_in_secs(self) -> pulumi.Input[int]:
        """
        RTO in seconds.
        """
        return pulumi.get(self, "rto_in_secs")

    @rto_in_secs.setter
    def rto_in_secs(self, value: pulumi.Input[int]):
        pulumi.set(self, "rto_in_secs", value)


if not MYPY:
    class ResiliencyPolicyPolicyMapArgsDict(TypedDict):
        az: pulumi.Input['ResiliencyPolicyFailurePolicyArgsDict']
        """
        Defines the RTO and RPO targets for Availability Zone disruption.
        """
        hardware: pulumi.Input['ResiliencyPolicyFailurePolicyArgsDict']
        """
        Defines the RTO and RPO targets for hardware disruption.
        """
        software: pulumi.Input['ResiliencyPolicyFailurePolicyArgsDict']
        """
        Defines the RTO and RPO targets for software disruption.
        """
        region: NotRequired[pulumi.Input['ResiliencyPolicyFailurePolicyArgsDict']]
        """
        Defines the RTO and RPO targets for Regional disruption.
        """
elif False:
    ResiliencyPolicyPolicyMapArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ResiliencyPolicyPolicyMapArgs:
    def __init__(__self__, *,
                 az: pulumi.Input['ResiliencyPolicyFailurePolicyArgs'],
                 hardware: pulumi.Input['ResiliencyPolicyFailurePolicyArgs'],
                 software: pulumi.Input['ResiliencyPolicyFailurePolicyArgs'],
                 region: Optional[pulumi.Input['ResiliencyPolicyFailurePolicyArgs']] = None):
        """
        :param pulumi.Input['ResiliencyPolicyFailurePolicyArgs'] az: Defines the RTO and RPO targets for Availability Zone disruption.
        :param pulumi.Input['ResiliencyPolicyFailurePolicyArgs'] hardware: Defines the RTO and RPO targets for hardware disruption.
        :param pulumi.Input['ResiliencyPolicyFailurePolicyArgs'] software: Defines the RTO and RPO targets for software disruption.
        :param pulumi.Input['ResiliencyPolicyFailurePolicyArgs'] region: Defines the RTO and RPO targets for Regional disruption.
        """
        pulumi.set(__self__, "az", az)
        pulumi.set(__self__, "hardware", hardware)
        pulumi.set(__self__, "software", software)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def az(self) -> pulumi.Input['ResiliencyPolicyFailurePolicyArgs']:
        """
        Defines the RTO and RPO targets for Availability Zone disruption.
        """
        return pulumi.get(self, "az")

    @az.setter
    def az(self, value: pulumi.Input['ResiliencyPolicyFailurePolicyArgs']):
        pulumi.set(self, "az", value)

    @property
    @pulumi.getter
    def hardware(self) -> pulumi.Input['ResiliencyPolicyFailurePolicyArgs']:
        """
        Defines the RTO and RPO targets for hardware disruption.
        """
        return pulumi.get(self, "hardware")

    @hardware.setter
    def hardware(self, value: pulumi.Input['ResiliencyPolicyFailurePolicyArgs']):
        pulumi.set(self, "hardware", value)

    @property
    @pulumi.getter
    def software(self) -> pulumi.Input['ResiliencyPolicyFailurePolicyArgs']:
        """
        Defines the RTO and RPO targets for software disruption.
        """
        return pulumi.get(self, "software")

    @software.setter
    def software(self, value: pulumi.Input['ResiliencyPolicyFailurePolicyArgs']):
        pulumi.set(self, "software", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input['ResiliencyPolicyFailurePolicyArgs']]:
        """
        Defines the RTO and RPO targets for Regional disruption.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input['ResiliencyPolicyFailurePolicyArgs']]):
        pulumi.set(self, "region", value)


