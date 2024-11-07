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
    'CapabilityConfigurationPropertiesArgs',
    'CapabilityConfigurationPropertiesArgsDict',
    'CapabilityEdiConfigurationArgs',
    'CapabilityEdiConfigurationArgsDict',
    'CapabilityEdiTypePropertiesArgs',
    'CapabilityEdiTypePropertiesArgsDict',
    'CapabilityS3LocationArgs',
    'CapabilityS3LocationArgsDict',
    'CapabilityX12DetailsArgs',
    'CapabilityX12DetailsArgsDict',
    'PartnershipCapabilityOptionsArgs',
    'PartnershipCapabilityOptionsArgsDict',
    'PartnershipOutboundEdiOptionsPropertiesArgs',
    'PartnershipOutboundEdiOptionsPropertiesArgsDict',
    'PartnershipX12DelimitersArgs',
    'PartnershipX12DelimitersArgsDict',
    'PartnershipX12EnvelopeArgs',
    'PartnershipX12EnvelopeArgsDict',
    'PartnershipX12FunctionalGroupHeadersArgs',
    'PartnershipX12FunctionalGroupHeadersArgsDict',
    'PartnershipX12InterchangeControlHeadersArgs',
    'PartnershipX12InterchangeControlHeadersArgsDict',
    'PartnershipX12OutboundEdiHeadersArgs',
    'PartnershipX12OutboundEdiHeadersArgsDict',
    'TransformerEdiTypePropertiesArgs',
    'TransformerEdiTypePropertiesArgsDict',
    'TransformerFormatOptionsPropertiesArgs',
    'TransformerFormatOptionsPropertiesArgsDict',
    'TransformerInputConversionArgs',
    'TransformerInputConversionArgsDict',
    'TransformerMappingArgs',
    'TransformerMappingArgsDict',
    'TransformerOutputConversionArgs',
    'TransformerOutputConversionArgsDict',
    'TransformerSampleDocumentKeysArgs',
    'TransformerSampleDocumentKeysArgsDict',
    'TransformerSampleDocumentsArgs',
    'TransformerSampleDocumentsArgsDict',
    'TransformerX12DetailsArgs',
    'TransformerX12DetailsArgsDict',
]

MYPY = False

if not MYPY:
    class CapabilityConfigurationPropertiesArgsDict(TypedDict):
        edi: pulumi.Input['CapabilityEdiConfigurationArgsDict']
elif False:
    CapabilityConfigurationPropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CapabilityConfigurationPropertiesArgs:
    def __init__(__self__, *,
                 edi: pulumi.Input['CapabilityEdiConfigurationArgs']):
        pulumi.set(__self__, "edi", edi)

    @property
    @pulumi.getter
    def edi(self) -> pulumi.Input['CapabilityEdiConfigurationArgs']:
        return pulumi.get(self, "edi")

    @edi.setter
    def edi(self, value: pulumi.Input['CapabilityEdiConfigurationArgs']):
        pulumi.set(self, "edi", value)


if not MYPY:
    class CapabilityEdiConfigurationArgsDict(TypedDict):
        input_location: pulumi.Input['CapabilityS3LocationArgsDict']
        output_location: pulumi.Input['CapabilityS3LocationArgsDict']
        transformer_id: pulumi.Input[str]
        type: pulumi.Input['CapabilityEdiTypePropertiesArgsDict']
        capability_direction: NotRequired[pulumi.Input['CapabilityDirection']]
elif False:
    CapabilityEdiConfigurationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CapabilityEdiConfigurationArgs:
    def __init__(__self__, *,
                 input_location: pulumi.Input['CapabilityS3LocationArgs'],
                 output_location: pulumi.Input['CapabilityS3LocationArgs'],
                 transformer_id: pulumi.Input[str],
                 type: pulumi.Input['CapabilityEdiTypePropertiesArgs'],
                 capability_direction: Optional[pulumi.Input['CapabilityDirection']] = None):
        pulumi.set(__self__, "input_location", input_location)
        pulumi.set(__self__, "output_location", output_location)
        pulumi.set(__self__, "transformer_id", transformer_id)
        pulumi.set(__self__, "type", type)
        if capability_direction is not None:
            pulumi.set(__self__, "capability_direction", capability_direction)

    @property
    @pulumi.getter(name="inputLocation")
    def input_location(self) -> pulumi.Input['CapabilityS3LocationArgs']:
        return pulumi.get(self, "input_location")

    @input_location.setter
    def input_location(self, value: pulumi.Input['CapabilityS3LocationArgs']):
        pulumi.set(self, "input_location", value)

    @property
    @pulumi.getter(name="outputLocation")
    def output_location(self) -> pulumi.Input['CapabilityS3LocationArgs']:
        return pulumi.get(self, "output_location")

    @output_location.setter
    def output_location(self, value: pulumi.Input['CapabilityS3LocationArgs']):
        pulumi.set(self, "output_location", value)

    @property
    @pulumi.getter(name="transformerId")
    def transformer_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "transformer_id")

    @transformer_id.setter
    def transformer_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "transformer_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['CapabilityEdiTypePropertiesArgs']:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['CapabilityEdiTypePropertiesArgs']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="capabilityDirection")
    def capability_direction(self) -> Optional[pulumi.Input['CapabilityDirection']]:
        return pulumi.get(self, "capability_direction")

    @capability_direction.setter
    def capability_direction(self, value: Optional[pulumi.Input['CapabilityDirection']]):
        pulumi.set(self, "capability_direction", value)


if not MYPY:
    class CapabilityEdiTypePropertiesArgsDict(TypedDict):
        x12_details: pulumi.Input['CapabilityX12DetailsArgsDict']
elif False:
    CapabilityEdiTypePropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CapabilityEdiTypePropertiesArgs:
    def __init__(__self__, *,
                 x12_details: pulumi.Input['CapabilityX12DetailsArgs']):
        pulumi.set(__self__, "x12_details", x12_details)

    @property
    @pulumi.getter(name="x12Details")
    def x12_details(self) -> pulumi.Input['CapabilityX12DetailsArgs']:
        return pulumi.get(self, "x12_details")

    @x12_details.setter
    def x12_details(self, value: pulumi.Input['CapabilityX12DetailsArgs']):
        pulumi.set(self, "x12_details", value)


if not MYPY:
    class CapabilityS3LocationArgsDict(TypedDict):
        bucket_name: NotRequired[pulumi.Input[str]]
        key: NotRequired[pulumi.Input[str]]
elif False:
    CapabilityS3LocationArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CapabilityS3LocationArgs:
    def __init__(__self__, *,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None):
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if key is not None:
            pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)


if not MYPY:
    class CapabilityX12DetailsArgsDict(TypedDict):
        transaction_set: NotRequired[pulumi.Input['CapabilityX12TransactionSet']]
        version: NotRequired[pulumi.Input['CapabilityX12Version']]
elif False:
    CapabilityX12DetailsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CapabilityX12DetailsArgs:
    def __init__(__self__, *,
                 transaction_set: Optional[pulumi.Input['CapabilityX12TransactionSet']] = None,
                 version: Optional[pulumi.Input['CapabilityX12Version']] = None):
        if transaction_set is not None:
            pulumi.set(__self__, "transaction_set", transaction_set)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="transactionSet")
    def transaction_set(self) -> Optional[pulumi.Input['CapabilityX12TransactionSet']]:
        return pulumi.get(self, "transaction_set")

    @transaction_set.setter
    def transaction_set(self, value: Optional[pulumi.Input['CapabilityX12TransactionSet']]):
        pulumi.set(self, "transaction_set", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input['CapabilityX12Version']]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input['CapabilityX12Version']]):
        pulumi.set(self, "version", value)


if not MYPY:
    class PartnershipCapabilityOptionsArgsDict(TypedDict):
        outbound_edi: NotRequired[pulumi.Input['PartnershipOutboundEdiOptionsPropertiesArgsDict']]
        """
        A structure that contains the outbound EDI options.
        """
elif False:
    PartnershipCapabilityOptionsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipCapabilityOptionsArgs:
    def __init__(__self__, *,
                 outbound_edi: Optional[pulumi.Input['PartnershipOutboundEdiOptionsPropertiesArgs']] = None):
        """
        :param pulumi.Input['PartnershipOutboundEdiOptionsPropertiesArgs'] outbound_edi: A structure that contains the outbound EDI options.
        """
        if outbound_edi is not None:
            pulumi.set(__self__, "outbound_edi", outbound_edi)

    @property
    @pulumi.getter(name="outboundEdi")
    def outbound_edi(self) -> Optional[pulumi.Input['PartnershipOutboundEdiOptionsPropertiesArgs']]:
        """
        A structure that contains the outbound EDI options.
        """
        return pulumi.get(self, "outbound_edi")

    @outbound_edi.setter
    def outbound_edi(self, value: Optional[pulumi.Input['PartnershipOutboundEdiOptionsPropertiesArgs']]):
        pulumi.set(self, "outbound_edi", value)


if not MYPY:
    class PartnershipOutboundEdiOptionsPropertiesArgsDict(TypedDict):
        x12: pulumi.Input['PartnershipX12EnvelopeArgsDict']
elif False:
    PartnershipOutboundEdiOptionsPropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipOutboundEdiOptionsPropertiesArgs:
    def __init__(__self__, *,
                 x12: pulumi.Input['PartnershipX12EnvelopeArgs']):
        pulumi.set(__self__, "x12", x12)

    @property
    @pulumi.getter
    def x12(self) -> pulumi.Input['PartnershipX12EnvelopeArgs']:
        return pulumi.get(self, "x12")

    @x12.setter
    def x12(self, value: pulumi.Input['PartnershipX12EnvelopeArgs']):
        pulumi.set(self, "x12", value)


if not MYPY:
    class PartnershipX12DelimitersArgsDict(TypedDict):
        component_separator: NotRequired[pulumi.Input[str]]
        data_element_separator: NotRequired[pulumi.Input[str]]
        segment_terminator: NotRequired[pulumi.Input[str]]
elif False:
    PartnershipX12DelimitersArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipX12DelimitersArgs:
    def __init__(__self__, *,
                 component_separator: Optional[pulumi.Input[str]] = None,
                 data_element_separator: Optional[pulumi.Input[str]] = None,
                 segment_terminator: Optional[pulumi.Input[str]] = None):
        if component_separator is not None:
            pulumi.set(__self__, "component_separator", component_separator)
        if data_element_separator is not None:
            pulumi.set(__self__, "data_element_separator", data_element_separator)
        if segment_terminator is not None:
            pulumi.set(__self__, "segment_terminator", segment_terminator)

    @property
    @pulumi.getter(name="componentSeparator")
    def component_separator(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "component_separator")

    @component_separator.setter
    def component_separator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "component_separator", value)

    @property
    @pulumi.getter(name="dataElementSeparator")
    def data_element_separator(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "data_element_separator")

    @data_element_separator.setter
    def data_element_separator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_element_separator", value)

    @property
    @pulumi.getter(name="segmentTerminator")
    def segment_terminator(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "segment_terminator")

    @segment_terminator.setter
    def segment_terminator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "segment_terminator", value)


if not MYPY:
    class PartnershipX12EnvelopeArgsDict(TypedDict):
        common: NotRequired[pulumi.Input['PartnershipX12OutboundEdiHeadersArgsDict']]
elif False:
    PartnershipX12EnvelopeArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipX12EnvelopeArgs:
    def __init__(__self__, *,
                 common: Optional[pulumi.Input['PartnershipX12OutboundEdiHeadersArgs']] = None):
        if common is not None:
            pulumi.set(__self__, "common", common)

    @property
    @pulumi.getter
    def common(self) -> Optional[pulumi.Input['PartnershipX12OutboundEdiHeadersArgs']]:
        return pulumi.get(self, "common")

    @common.setter
    def common(self, value: Optional[pulumi.Input['PartnershipX12OutboundEdiHeadersArgs']]):
        pulumi.set(self, "common", value)


if not MYPY:
    class PartnershipX12FunctionalGroupHeadersArgsDict(TypedDict):
        application_receiver_code: NotRequired[pulumi.Input[str]]
        application_sender_code: NotRequired[pulumi.Input[str]]
        responsible_agency_code: NotRequired[pulumi.Input[str]]
elif False:
    PartnershipX12FunctionalGroupHeadersArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipX12FunctionalGroupHeadersArgs:
    def __init__(__self__, *,
                 application_receiver_code: Optional[pulumi.Input[str]] = None,
                 application_sender_code: Optional[pulumi.Input[str]] = None,
                 responsible_agency_code: Optional[pulumi.Input[str]] = None):
        if application_receiver_code is not None:
            pulumi.set(__self__, "application_receiver_code", application_receiver_code)
        if application_sender_code is not None:
            pulumi.set(__self__, "application_sender_code", application_sender_code)
        if responsible_agency_code is not None:
            pulumi.set(__self__, "responsible_agency_code", responsible_agency_code)

    @property
    @pulumi.getter(name="applicationReceiverCode")
    def application_receiver_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "application_receiver_code")

    @application_receiver_code.setter
    def application_receiver_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_receiver_code", value)

    @property
    @pulumi.getter(name="applicationSenderCode")
    def application_sender_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "application_sender_code")

    @application_sender_code.setter
    def application_sender_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_sender_code", value)

    @property
    @pulumi.getter(name="responsibleAgencyCode")
    def responsible_agency_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "responsible_agency_code")

    @responsible_agency_code.setter
    def responsible_agency_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "responsible_agency_code", value)


if not MYPY:
    class PartnershipX12InterchangeControlHeadersArgsDict(TypedDict):
        acknowledgment_requested_code: NotRequired[pulumi.Input[str]]
        receiver_id: NotRequired[pulumi.Input[str]]
        receiver_id_qualifier: NotRequired[pulumi.Input[str]]
        repetition_separator: NotRequired[pulumi.Input[str]]
        sender_id: NotRequired[pulumi.Input[str]]
        sender_id_qualifier: NotRequired[pulumi.Input[str]]
        usage_indicator_code: NotRequired[pulumi.Input[str]]
elif False:
    PartnershipX12InterchangeControlHeadersArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipX12InterchangeControlHeadersArgs:
    def __init__(__self__, *,
                 acknowledgment_requested_code: Optional[pulumi.Input[str]] = None,
                 receiver_id: Optional[pulumi.Input[str]] = None,
                 receiver_id_qualifier: Optional[pulumi.Input[str]] = None,
                 repetition_separator: Optional[pulumi.Input[str]] = None,
                 sender_id: Optional[pulumi.Input[str]] = None,
                 sender_id_qualifier: Optional[pulumi.Input[str]] = None,
                 usage_indicator_code: Optional[pulumi.Input[str]] = None):
        if acknowledgment_requested_code is not None:
            pulumi.set(__self__, "acknowledgment_requested_code", acknowledgment_requested_code)
        if receiver_id is not None:
            pulumi.set(__self__, "receiver_id", receiver_id)
        if receiver_id_qualifier is not None:
            pulumi.set(__self__, "receiver_id_qualifier", receiver_id_qualifier)
        if repetition_separator is not None:
            pulumi.set(__self__, "repetition_separator", repetition_separator)
        if sender_id is not None:
            pulumi.set(__self__, "sender_id", sender_id)
        if sender_id_qualifier is not None:
            pulumi.set(__self__, "sender_id_qualifier", sender_id_qualifier)
        if usage_indicator_code is not None:
            pulumi.set(__self__, "usage_indicator_code", usage_indicator_code)

    @property
    @pulumi.getter(name="acknowledgmentRequestedCode")
    def acknowledgment_requested_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "acknowledgment_requested_code")

    @acknowledgment_requested_code.setter
    def acknowledgment_requested_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acknowledgment_requested_code", value)

    @property
    @pulumi.getter(name="receiverId")
    def receiver_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "receiver_id")

    @receiver_id.setter
    def receiver_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "receiver_id", value)

    @property
    @pulumi.getter(name="receiverIdQualifier")
    def receiver_id_qualifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "receiver_id_qualifier")

    @receiver_id_qualifier.setter
    def receiver_id_qualifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "receiver_id_qualifier", value)

    @property
    @pulumi.getter(name="repetitionSeparator")
    def repetition_separator(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "repetition_separator")

    @repetition_separator.setter
    def repetition_separator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repetition_separator", value)

    @property
    @pulumi.getter(name="senderId")
    def sender_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "sender_id")

    @sender_id.setter
    def sender_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sender_id", value)

    @property
    @pulumi.getter(name="senderIdQualifier")
    def sender_id_qualifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "sender_id_qualifier")

    @sender_id_qualifier.setter
    def sender_id_qualifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sender_id_qualifier", value)

    @property
    @pulumi.getter(name="usageIndicatorCode")
    def usage_indicator_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "usage_indicator_code")

    @usage_indicator_code.setter
    def usage_indicator_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage_indicator_code", value)


if not MYPY:
    class PartnershipX12OutboundEdiHeadersArgsDict(TypedDict):
        delimiters: NotRequired[pulumi.Input['PartnershipX12DelimitersArgsDict']]
        functional_group_headers: NotRequired[pulumi.Input['PartnershipX12FunctionalGroupHeadersArgsDict']]
        interchange_control_headers: NotRequired[pulumi.Input['PartnershipX12InterchangeControlHeadersArgsDict']]
        validate_edi: NotRequired[pulumi.Input[bool]]
elif False:
    PartnershipX12OutboundEdiHeadersArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class PartnershipX12OutboundEdiHeadersArgs:
    def __init__(__self__, *,
                 delimiters: Optional[pulumi.Input['PartnershipX12DelimitersArgs']] = None,
                 functional_group_headers: Optional[pulumi.Input['PartnershipX12FunctionalGroupHeadersArgs']] = None,
                 interchange_control_headers: Optional[pulumi.Input['PartnershipX12InterchangeControlHeadersArgs']] = None,
                 validate_edi: Optional[pulumi.Input[bool]] = None):
        if delimiters is not None:
            pulumi.set(__self__, "delimiters", delimiters)
        if functional_group_headers is not None:
            pulumi.set(__self__, "functional_group_headers", functional_group_headers)
        if interchange_control_headers is not None:
            pulumi.set(__self__, "interchange_control_headers", interchange_control_headers)
        if validate_edi is not None:
            pulumi.set(__self__, "validate_edi", validate_edi)

    @property
    @pulumi.getter
    def delimiters(self) -> Optional[pulumi.Input['PartnershipX12DelimitersArgs']]:
        return pulumi.get(self, "delimiters")

    @delimiters.setter
    def delimiters(self, value: Optional[pulumi.Input['PartnershipX12DelimitersArgs']]):
        pulumi.set(self, "delimiters", value)

    @property
    @pulumi.getter(name="functionalGroupHeaders")
    def functional_group_headers(self) -> Optional[pulumi.Input['PartnershipX12FunctionalGroupHeadersArgs']]:
        return pulumi.get(self, "functional_group_headers")

    @functional_group_headers.setter
    def functional_group_headers(self, value: Optional[pulumi.Input['PartnershipX12FunctionalGroupHeadersArgs']]):
        pulumi.set(self, "functional_group_headers", value)

    @property
    @pulumi.getter(name="interchangeControlHeaders")
    def interchange_control_headers(self) -> Optional[pulumi.Input['PartnershipX12InterchangeControlHeadersArgs']]:
        return pulumi.get(self, "interchange_control_headers")

    @interchange_control_headers.setter
    def interchange_control_headers(self, value: Optional[pulumi.Input['PartnershipX12InterchangeControlHeadersArgs']]):
        pulumi.set(self, "interchange_control_headers", value)

    @property
    @pulumi.getter(name="validateEdi")
    def validate_edi(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "validate_edi")

    @validate_edi.setter
    def validate_edi(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "validate_edi", value)


if not MYPY:
    class TransformerEdiTypePropertiesArgsDict(TypedDict):
        x12_details: pulumi.Input['TransformerX12DetailsArgsDict']
elif False:
    TransformerEdiTypePropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerEdiTypePropertiesArgs:
    def __init__(__self__, *,
                 x12_details: pulumi.Input['TransformerX12DetailsArgs']):
        pulumi.set(__self__, "x12_details", x12_details)

    @property
    @pulumi.getter(name="x12Details")
    def x12_details(self) -> pulumi.Input['TransformerX12DetailsArgs']:
        return pulumi.get(self, "x12_details")

    @x12_details.setter
    def x12_details(self, value: pulumi.Input['TransformerX12DetailsArgs']):
        pulumi.set(self, "x12_details", value)


if not MYPY:
    class TransformerFormatOptionsPropertiesArgsDict(TypedDict):
        x12: pulumi.Input['TransformerX12DetailsArgsDict']
elif False:
    TransformerFormatOptionsPropertiesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerFormatOptionsPropertiesArgs:
    def __init__(__self__, *,
                 x12: pulumi.Input['TransformerX12DetailsArgs']):
        pulumi.set(__self__, "x12", x12)

    @property
    @pulumi.getter
    def x12(self) -> pulumi.Input['TransformerX12DetailsArgs']:
        return pulumi.get(self, "x12")

    @x12.setter
    def x12(self, value: pulumi.Input['TransformerX12DetailsArgs']):
        pulumi.set(self, "x12", value)


if not MYPY:
    class TransformerInputConversionArgsDict(TypedDict):
        from_format: pulumi.Input['TransformerFromFormat']
        format_options: NotRequired[pulumi.Input['TransformerFormatOptionsPropertiesArgsDict']]
elif False:
    TransformerInputConversionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerInputConversionArgs:
    def __init__(__self__, *,
                 from_format: pulumi.Input['TransformerFromFormat'],
                 format_options: Optional[pulumi.Input['TransformerFormatOptionsPropertiesArgs']] = None):
        pulumi.set(__self__, "from_format", from_format)
        if format_options is not None:
            pulumi.set(__self__, "format_options", format_options)

    @property
    @pulumi.getter(name="fromFormat")
    def from_format(self) -> pulumi.Input['TransformerFromFormat']:
        return pulumi.get(self, "from_format")

    @from_format.setter
    def from_format(self, value: pulumi.Input['TransformerFromFormat']):
        pulumi.set(self, "from_format", value)

    @property
    @pulumi.getter(name="formatOptions")
    def format_options(self) -> Optional[pulumi.Input['TransformerFormatOptionsPropertiesArgs']]:
        return pulumi.get(self, "format_options")

    @format_options.setter
    def format_options(self, value: Optional[pulumi.Input['TransformerFormatOptionsPropertiesArgs']]):
        pulumi.set(self, "format_options", value)


if not MYPY:
    class TransformerMappingArgsDict(TypedDict):
        template_language: pulumi.Input['TransformerMappingTemplateLanguage']
        template: NotRequired[pulumi.Input[str]]
elif False:
    TransformerMappingArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerMappingArgs:
    def __init__(__self__, *,
                 template_language: pulumi.Input['TransformerMappingTemplateLanguage'],
                 template: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "template_language", template_language)
        if template is not None:
            pulumi.set(__self__, "template", template)

    @property
    @pulumi.getter(name="templateLanguage")
    def template_language(self) -> pulumi.Input['TransformerMappingTemplateLanguage']:
        return pulumi.get(self, "template_language")

    @template_language.setter
    def template_language(self, value: pulumi.Input['TransformerMappingTemplateLanguage']):
        pulumi.set(self, "template_language", value)

    @property
    @pulumi.getter
    def template(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template", value)


if not MYPY:
    class TransformerOutputConversionArgsDict(TypedDict):
        to_format: pulumi.Input['TransformerToFormat']
        format_options: NotRequired[pulumi.Input['TransformerFormatOptionsPropertiesArgsDict']]
elif False:
    TransformerOutputConversionArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerOutputConversionArgs:
    def __init__(__self__, *,
                 to_format: pulumi.Input['TransformerToFormat'],
                 format_options: Optional[pulumi.Input['TransformerFormatOptionsPropertiesArgs']] = None):
        pulumi.set(__self__, "to_format", to_format)
        if format_options is not None:
            pulumi.set(__self__, "format_options", format_options)

    @property
    @pulumi.getter(name="toFormat")
    def to_format(self) -> pulumi.Input['TransformerToFormat']:
        return pulumi.get(self, "to_format")

    @to_format.setter
    def to_format(self, value: pulumi.Input['TransformerToFormat']):
        pulumi.set(self, "to_format", value)

    @property
    @pulumi.getter(name="formatOptions")
    def format_options(self) -> Optional[pulumi.Input['TransformerFormatOptionsPropertiesArgs']]:
        return pulumi.get(self, "format_options")

    @format_options.setter
    def format_options(self, value: Optional[pulumi.Input['TransformerFormatOptionsPropertiesArgs']]):
        pulumi.set(self, "format_options", value)


if not MYPY:
    class TransformerSampleDocumentKeysArgsDict(TypedDict):
        input: NotRequired[pulumi.Input[str]]
        output: NotRequired[pulumi.Input[str]]
elif False:
    TransformerSampleDocumentKeysArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerSampleDocumentKeysArgs:
    def __init__(__self__, *,
                 input: Optional[pulumi.Input[str]] = None,
                 output: Optional[pulumi.Input[str]] = None):
        if input is not None:
            pulumi.set(__self__, "input", input)
        if output is not None:
            pulumi.set(__self__, "output", output)

    @property
    @pulumi.getter
    def input(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "input")

    @input.setter
    def input(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "input", value)

    @property
    @pulumi.getter
    def output(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "output")

    @output.setter
    def output(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output", value)


if not MYPY:
    class TransformerSampleDocumentsArgsDict(TypedDict):
        bucket_name: pulumi.Input[str]
        keys: pulumi.Input[Sequence[pulumi.Input['TransformerSampleDocumentKeysArgsDict']]]
elif False:
    TransformerSampleDocumentsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerSampleDocumentsArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str],
                 keys: pulumi.Input[Sequence[pulumi.Input['TransformerSampleDocumentKeysArgs']]]):
        pulumi.set(__self__, "bucket_name", bucket_name)
        pulumi.set(__self__, "keys", keys)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter
    def keys(self) -> pulumi.Input[Sequence[pulumi.Input['TransformerSampleDocumentKeysArgs']]]:
        return pulumi.get(self, "keys")

    @keys.setter
    def keys(self, value: pulumi.Input[Sequence[pulumi.Input['TransformerSampleDocumentKeysArgs']]]):
        pulumi.set(self, "keys", value)


if not MYPY:
    class TransformerX12DetailsArgsDict(TypedDict):
        transaction_set: NotRequired[pulumi.Input['TransformerX12TransactionSet']]
        version: NotRequired[pulumi.Input['TransformerX12Version']]
elif False:
    TransformerX12DetailsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class TransformerX12DetailsArgs:
    def __init__(__self__, *,
                 transaction_set: Optional[pulumi.Input['TransformerX12TransactionSet']] = None,
                 version: Optional[pulumi.Input['TransformerX12Version']] = None):
        if transaction_set is not None:
            pulumi.set(__self__, "transaction_set", transaction_set)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="transactionSet")
    def transaction_set(self) -> Optional[pulumi.Input['TransformerX12TransactionSet']]:
        return pulumi.get(self, "transaction_set")

    @transaction_set.setter
    def transaction_set(self, value: Optional[pulumi.Input['TransformerX12TransactionSet']]):
        pulumi.set(self, "transaction_set", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input['TransformerX12Version']]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input['TransformerX12Version']]):
        pulumi.set(self, "version", value)


