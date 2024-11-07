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

__all__ = ['CertificateAuthorityArgs', 'CertificateAuthority']

@pulumi.input_type
class CertificateAuthorityArgs:
    def __init__(__self__, *,
                 key_algorithm: pulumi.Input[str],
                 signing_algorithm: pulumi.Input[str],
                 subject: pulumi.Input['CertificateAuthoritySubjectArgs'],
                 type: pulumi.Input[str],
                 csr_extensions: Optional[pulumi.Input['CertificateAuthorityCsrExtensionsArgs']] = None,
                 key_storage_security_standard: Optional[pulumi.Input[str]] = None,
                 revocation_configuration: Optional[pulumi.Input['CertificateAuthorityRevocationConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]] = None,
                 usage_mode: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CertificateAuthority resource.
        :param pulumi.Input[str] key_algorithm: Public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.
        :param pulumi.Input[str] signing_algorithm: Algorithm your CA uses to sign certificate requests.
        :param pulumi.Input['CertificateAuthoritySubjectArgs'] subject: Structure that contains X.500 distinguished name information for your CA.
        :param pulumi.Input[str] type: The type of the certificate authority.
        :param pulumi.Input['CertificateAuthorityCsrExtensionsArgs'] csr_extensions: Structure that contains CSR pass through extension information used by the CreateCertificateAuthority action.
        :param pulumi.Input[str] key_storage_security_standard: KeyStorageSecurityStadard defines a cryptographic key management compliance standard used for handling CA keys.
        :param pulumi.Input['CertificateAuthorityRevocationConfigurationArgs'] revocation_configuration: Certificate revocation information used by the CreateCertificateAuthority and UpdateCertificateAuthority actions.
        :param pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]] tags: Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see [Controlling Access Using IAM Tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html) .
        :param pulumi.Input[str] usage_mode: Usage mode of the ceritificate authority.
        """
        pulumi.set(__self__, "key_algorithm", key_algorithm)
        pulumi.set(__self__, "signing_algorithm", signing_algorithm)
        pulumi.set(__self__, "subject", subject)
        pulumi.set(__self__, "type", type)
        if csr_extensions is not None:
            pulumi.set(__self__, "csr_extensions", csr_extensions)
        if key_storage_security_standard is not None:
            pulumi.set(__self__, "key_storage_security_standard", key_storage_security_standard)
        if revocation_configuration is not None:
            pulumi.set(__self__, "revocation_configuration", revocation_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if usage_mode is not None:
            pulumi.set(__self__, "usage_mode", usage_mode)

    @property
    @pulumi.getter(name="keyAlgorithm")
    def key_algorithm(self) -> pulumi.Input[str]:
        """
        Public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.
        """
        return pulumi.get(self, "key_algorithm")

    @key_algorithm.setter
    def key_algorithm(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_algorithm", value)

    @property
    @pulumi.getter(name="signingAlgorithm")
    def signing_algorithm(self) -> pulumi.Input[str]:
        """
        Algorithm your CA uses to sign certificate requests.
        """
        return pulumi.get(self, "signing_algorithm")

    @signing_algorithm.setter
    def signing_algorithm(self, value: pulumi.Input[str]):
        pulumi.set(self, "signing_algorithm", value)

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Input['CertificateAuthoritySubjectArgs']:
        """
        Structure that contains X.500 distinguished name information for your CA.
        """
        return pulumi.get(self, "subject")

    @subject.setter
    def subject(self, value: pulumi.Input['CertificateAuthoritySubjectArgs']):
        pulumi.set(self, "subject", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of the certificate authority.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="csrExtensions")
    def csr_extensions(self) -> Optional[pulumi.Input['CertificateAuthorityCsrExtensionsArgs']]:
        """
        Structure that contains CSR pass through extension information used by the CreateCertificateAuthority action.
        """
        return pulumi.get(self, "csr_extensions")

    @csr_extensions.setter
    def csr_extensions(self, value: Optional[pulumi.Input['CertificateAuthorityCsrExtensionsArgs']]):
        pulumi.set(self, "csr_extensions", value)

    @property
    @pulumi.getter(name="keyStorageSecurityStandard")
    def key_storage_security_standard(self) -> Optional[pulumi.Input[str]]:
        """
        KeyStorageSecurityStadard defines a cryptographic key management compliance standard used for handling CA keys.
        """
        return pulumi.get(self, "key_storage_security_standard")

    @key_storage_security_standard.setter
    def key_storage_security_standard(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_storage_security_standard", value)

    @property
    @pulumi.getter(name="revocationConfiguration")
    def revocation_configuration(self) -> Optional[pulumi.Input['CertificateAuthorityRevocationConfigurationArgs']]:
        """
        Certificate revocation information used by the CreateCertificateAuthority and UpdateCertificateAuthority actions.
        """
        return pulumi.get(self, "revocation_configuration")

    @revocation_configuration.setter
    def revocation_configuration(self, value: Optional[pulumi.Input['CertificateAuthorityRevocationConfigurationArgs']]):
        pulumi.set(self, "revocation_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]:
        """
        Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see [Controlling Access Using IAM Tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html) .
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['_root_inputs.TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="usageMode")
    def usage_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Usage mode of the ceritificate authority.
        """
        return pulumi.get(self, "usage_mode")

    @usage_mode.setter
    def usage_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage_mode", value)


class CertificateAuthority(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 csr_extensions: Optional[pulumi.Input[Union['CertificateAuthorityCsrExtensionsArgs', 'CertificateAuthorityCsrExtensionsArgsDict']]] = None,
                 key_algorithm: Optional[pulumi.Input[str]] = None,
                 key_storage_security_standard: Optional[pulumi.Input[str]] = None,
                 revocation_configuration: Optional[pulumi.Input[Union['CertificateAuthorityRevocationConfigurationArgs', 'CertificateAuthorityRevocationConfigurationArgsDict']]] = None,
                 signing_algorithm: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[Union['CertificateAuthoritySubjectArgs', 'CertificateAuthoritySubjectArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 usage_mode: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Private certificate authority.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        root_ca = aws_native.acmpca.CertificateAuthority("rootCA",
            type="ROOT",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject={
                "country": "US",
                "organization": "string",
                "organizational_unit": "string",
                "distinguished_name_qualifier": "string",
                "state": "string",
                "common_name": "123",
                "serial_number": "string",
                "locality": "string",
                "title": "string",
                "surname": "string",
                "given_name": "string",
                "initials": "DG",
                "pseudonym": "string",
                "generation_qualifier": "DBG",
            },
            revocation_configuration={
                "crl_configuration": {
                    "enabled": False,
                },
            })
        root_ca_certificate = aws_native.acmpca.Certificate("rootCACertificate",
            certificate_authority_arn=root_ca.id,
            certificate_signing_request=root_ca.certificate_signing_request,
            signing_algorithm="SHA256WITHRSA",
            template_arn="arn:aws:acm-pca:::template/RootCACertificate/V1",
            validity={
                "type": "DAYS",
                "value": 100,
            })
        root_ca_activation = aws_native.acmpca.CertificateAuthorityActivation("rootCAActivation",
            certificate_authority_arn=root_ca.id,
            certificate=root_ca_certificate.certificate,
            status="ACTIVE")
        root_ca_permission = aws_native.acmpca.Permission("rootCAPermission",
            actions=[
                "IssueCertificate",
                "GetCertificate",
                "ListPermissions",
            ],
            certificate_authority_arn=root_ca.id,
            principal="acm.amazonaws.com")
        subordinate_ca_one = aws_native.acmpca.CertificateAuthority("subordinateCAOne",
            type="SUBORDINATE",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject={
                "country": "US",
                "organization": "string",
                "organizational_unit": "string",
                "distinguished_name_qualifier": "string",
                "state": "string",
                "common_name": "Sub1",
                "serial_number": "string",
                "locality": "string",
                "title": "string",
                "surname": "string",
                "given_name": "string",
                "initials": "DG",
                "pseudonym": "string",
                "generation_qualifier": "DBG",
            },
            revocation_configuration={},
            tags=[])
        subordinate_ca_one_ca_certificate = aws_native.acmpca.Certificate("subordinateCAOneCACertificate",
            certificate_authority_arn=root_ca.id,
            certificate_signing_request=subordinate_ca_one.certificate_signing_request,
            signing_algorithm="SHA256WITHRSA",
            template_arn="arn:aws:acm-pca:::template/SubordinateCACertificate_PathLen3/V1",
            validity={
                "type": "DAYS",
                "value": 90,
            },
            opts = pulumi.ResourceOptions(depends_on=[root_ca_activation]))
        subordinate_ca_one_activation = aws_native.acmpca.CertificateAuthorityActivation("subordinateCAOneActivation",
            certificate_authority_arn=subordinate_ca_one.id,
            certificate=subordinate_ca_one_ca_certificate.certificate,
            certificate_chain=root_ca_activation.complete_certificate_chain,
            status="ACTIVE")
        subordinate_ca_one_permission = aws_native.acmpca.Permission("subordinateCAOnePermission",
            actions=[
                "IssueCertificate",
                "GetCertificate",
                "ListPermissions",
            ],
            certificate_authority_arn=subordinate_ca_one.id,
            principal="acm.amazonaws.com")
        subordinate_ca_two = aws_native.acmpca.CertificateAuthority("subordinateCATwo",
            type="SUBORDINATE",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject={
                "country": "US",
                "organization": "string",
                "organizational_unit": "string",
                "distinguished_name_qualifier": "string",
                "state": "string",
                "serial_number": "string",
                "locality": "string",
                "title": "string",
                "surname": "string",
                "given_name": "string",
                "initials": "DG",
                "pseudonym": "string",
                "generation_qualifier": "DBG",
            },
            tags=[
                {
                    "key": "Key1",
                    "value": "Value1",
                },
                {
                    "key": "Key2",
                    "value": "Value2",
                },
            ])
        subordinate_ca_two_ca_certificate = aws_native.acmpca.Certificate("subordinateCATwoCACertificate",
            certificate_authority_arn=subordinate_ca_one.id,
            certificate_signing_request=subordinate_ca_two.certificate_signing_request,
            signing_algorithm="SHA256WITHRSA",
            template_arn="arn:aws:acm-pca:::template/SubordinateCACertificate_PathLen2/V1",
            validity={
                "type": "DAYS",
                "value": 80,
            },
            opts = pulumi.ResourceOptions(depends_on=[subordinate_ca_one_activation]))
        subordinate_ca_two_activation = aws_native.acmpca.CertificateAuthorityActivation("subordinateCATwoActivation",
            certificate_authority_arn=subordinate_ca_two.id,
            certificate=subordinate_ca_two_ca_certificate.certificate,
            certificate_chain=subordinate_ca_one_activation.complete_certificate_chain)
        subordinate_ca_two_permission = aws_native.acmpca.Permission("subordinateCATwoPermission",
            actions=[
                "IssueCertificate",
                "GetCertificate",
                "ListPermissions",
            ],
            certificate_authority_arn=subordinate_ca_two.id,
            principal="acm.amazonaws.com")
        end_entity_certificate = aws_native.acmpca.Certificate("endEntityCertificate",
            certificate_authority_arn=subordinate_ca_two.id,
            certificate_signing_request=\"\"\"-----BEGIN CERTIFICATE REQUEST-----
        MIICvDCCAaQCAQAwdzELMAkGA1UEBhMCVVMxDTALBgNVBAgMBFV0YWgxDzANBgNV
        BAcMBkxpbmRvbjEWMBQGA1UECgwNRGlnaUNlcnQgSW5jLjERMA8GA1UECwwIRGln
        aUNlcnQxHTAbBgNVBAMMFGV4YW1wbGUuZGlnaWNlcnQuY29tMIIBIjANBgkqhkiG
        9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8+To7d+2kPWeBv/orU3LVbJwDrSQbeKamCmo
        wp5bqDxIwV20zqRb7APUOKYoVEFFOEQs6T6gImnIolhbiH6m4zgZ/CPvWBOkZc+c
        1Po2EmvBz+AD5sBdT5kzGQA6NbWyZGldxRthNLOs1efOhdnWFuhI162qmcflgpiI
        WDuwq4C9f+YkeJhNn9dF5+owm8cOQmDrV8NNdiTqin8q3qYAHHJRW28glJUCZkTZ
        wIaSR6crBQ8TbYNE0dc+Caa3DOIkz1EOsHWzTx+n0zKfqcbgXi4DJx+C1bjptYPR
        BPZL8DAeWuA8ebudVT44yEp82G96/Ggcf7F33xMxe0yc+Xa6owIDAQABoAAwDQYJ
        KoZIhvcNAQEFBQADggEBAB0kcrFccSmFDmxox0Ne01UIqSsDqHgL+XmHTXJwre6D
        hJSZwbvEtOK0G3+dr4Fs11WuUNt5qcLsx5a8uk4G6AKHMzuhLsJ7XZjgmQXGECpY
        Q4mC3yT3ZoCGpIXbw+iP3lmEEXgaQL0Tx5LFl/okKbKYwIqNiyKWOMj7ZR/wxWg/
        ZDGRs55xuoeLDJ/ZRFf9bI+IaCUd1YrfYcHIl3G87Av+r49YVwqRDT0VDV7uLgqn
        29XI1PpVUNCPQGn9p/eX6Qo7vpDaPybRtA2R7XLKjQaF9oXWeCUqy1hvJac9QFO2
        97Ob1alpHPoZ7mWiEuJwjBPii6a9M9G30nUo39lBi1w=
        -----END CERTIFICATE REQUEST-----\"\"\",
            signing_algorithm="SHA256WITHRSA",
            validity={
                "type": "DAYS",
                "value": 70,
            },
            opts = pulumi.ResourceOptions(depends_on=[subordinate_ca_two_activation]))
        pulumi.export("completeCertificateChain", subordinate_ca_two_activation.complete_certificate_chain)
        pulumi.export("certificateArn", end_entity_certificate.arn)

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['CertificateAuthorityCsrExtensionsArgs', 'CertificateAuthorityCsrExtensionsArgsDict']] csr_extensions: Structure that contains CSR pass through extension information used by the CreateCertificateAuthority action.
        :param pulumi.Input[str] key_algorithm: Public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.
        :param pulumi.Input[str] key_storage_security_standard: KeyStorageSecurityStadard defines a cryptographic key management compliance standard used for handling CA keys.
        :param pulumi.Input[Union['CertificateAuthorityRevocationConfigurationArgs', 'CertificateAuthorityRevocationConfigurationArgsDict']] revocation_configuration: Certificate revocation information used by the CreateCertificateAuthority and UpdateCertificateAuthority actions.
        :param pulumi.Input[str] signing_algorithm: Algorithm your CA uses to sign certificate requests.
        :param pulumi.Input[Union['CertificateAuthoritySubjectArgs', 'CertificateAuthoritySubjectArgsDict']] subject: Structure that contains X.500 distinguished name information for your CA.
        :param pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]] tags: Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see [Controlling Access Using IAM Tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html) .
        :param pulumi.Input[str] type: The type of the certificate authority.
        :param pulumi.Input[str] usage_mode: Usage mode of the ceritificate authority.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateAuthorityArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Private certificate authority.

        ## Example Usage
        ### Example

        ```python
        import pulumi
        import pulumi_aws_native as aws_native

        root_ca = aws_native.acmpca.CertificateAuthority("rootCA",
            type="ROOT",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject={
                "country": "US",
                "organization": "string",
                "organizational_unit": "string",
                "distinguished_name_qualifier": "string",
                "state": "string",
                "common_name": "123",
                "serial_number": "string",
                "locality": "string",
                "title": "string",
                "surname": "string",
                "given_name": "string",
                "initials": "DG",
                "pseudonym": "string",
                "generation_qualifier": "DBG",
            },
            revocation_configuration={
                "crl_configuration": {
                    "enabled": False,
                },
            })
        root_ca_certificate = aws_native.acmpca.Certificate("rootCACertificate",
            certificate_authority_arn=root_ca.id,
            certificate_signing_request=root_ca.certificate_signing_request,
            signing_algorithm="SHA256WITHRSA",
            template_arn="arn:aws:acm-pca:::template/RootCACertificate/V1",
            validity={
                "type": "DAYS",
                "value": 100,
            })
        root_ca_activation = aws_native.acmpca.CertificateAuthorityActivation("rootCAActivation",
            certificate_authority_arn=root_ca.id,
            certificate=root_ca_certificate.certificate,
            status="ACTIVE")
        root_ca_permission = aws_native.acmpca.Permission("rootCAPermission",
            actions=[
                "IssueCertificate",
                "GetCertificate",
                "ListPermissions",
            ],
            certificate_authority_arn=root_ca.id,
            principal="acm.amazonaws.com")
        subordinate_ca_one = aws_native.acmpca.CertificateAuthority("subordinateCAOne",
            type="SUBORDINATE",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject={
                "country": "US",
                "organization": "string",
                "organizational_unit": "string",
                "distinguished_name_qualifier": "string",
                "state": "string",
                "common_name": "Sub1",
                "serial_number": "string",
                "locality": "string",
                "title": "string",
                "surname": "string",
                "given_name": "string",
                "initials": "DG",
                "pseudonym": "string",
                "generation_qualifier": "DBG",
            },
            revocation_configuration={},
            tags=[])
        subordinate_ca_one_ca_certificate = aws_native.acmpca.Certificate("subordinateCAOneCACertificate",
            certificate_authority_arn=root_ca.id,
            certificate_signing_request=subordinate_ca_one.certificate_signing_request,
            signing_algorithm="SHA256WITHRSA",
            template_arn="arn:aws:acm-pca:::template/SubordinateCACertificate_PathLen3/V1",
            validity={
                "type": "DAYS",
                "value": 90,
            },
            opts = pulumi.ResourceOptions(depends_on=[root_ca_activation]))
        subordinate_ca_one_activation = aws_native.acmpca.CertificateAuthorityActivation("subordinateCAOneActivation",
            certificate_authority_arn=subordinate_ca_one.id,
            certificate=subordinate_ca_one_ca_certificate.certificate,
            certificate_chain=root_ca_activation.complete_certificate_chain,
            status="ACTIVE")
        subordinate_ca_one_permission = aws_native.acmpca.Permission("subordinateCAOnePermission",
            actions=[
                "IssueCertificate",
                "GetCertificate",
                "ListPermissions",
            ],
            certificate_authority_arn=subordinate_ca_one.id,
            principal="acm.amazonaws.com")
        subordinate_ca_two = aws_native.acmpca.CertificateAuthority("subordinateCATwo",
            type="SUBORDINATE",
            key_algorithm="RSA_2048",
            signing_algorithm="SHA256WITHRSA",
            subject={
                "country": "US",
                "organization": "string",
                "organizational_unit": "string",
                "distinguished_name_qualifier": "string",
                "state": "string",
                "serial_number": "string",
                "locality": "string",
                "title": "string",
                "surname": "string",
                "given_name": "string",
                "initials": "DG",
                "pseudonym": "string",
                "generation_qualifier": "DBG",
            },
            tags=[
                {
                    "key": "Key1",
                    "value": "Value1",
                },
                {
                    "key": "Key2",
                    "value": "Value2",
                },
            ])
        subordinate_ca_two_ca_certificate = aws_native.acmpca.Certificate("subordinateCATwoCACertificate",
            certificate_authority_arn=subordinate_ca_one.id,
            certificate_signing_request=subordinate_ca_two.certificate_signing_request,
            signing_algorithm="SHA256WITHRSA",
            template_arn="arn:aws:acm-pca:::template/SubordinateCACertificate_PathLen2/V1",
            validity={
                "type": "DAYS",
                "value": 80,
            },
            opts = pulumi.ResourceOptions(depends_on=[subordinate_ca_one_activation]))
        subordinate_ca_two_activation = aws_native.acmpca.CertificateAuthorityActivation("subordinateCATwoActivation",
            certificate_authority_arn=subordinate_ca_two.id,
            certificate=subordinate_ca_two_ca_certificate.certificate,
            certificate_chain=subordinate_ca_one_activation.complete_certificate_chain)
        subordinate_ca_two_permission = aws_native.acmpca.Permission("subordinateCATwoPermission",
            actions=[
                "IssueCertificate",
                "GetCertificate",
                "ListPermissions",
            ],
            certificate_authority_arn=subordinate_ca_two.id,
            principal="acm.amazonaws.com")
        end_entity_certificate = aws_native.acmpca.Certificate("endEntityCertificate",
            certificate_authority_arn=subordinate_ca_two.id,
            certificate_signing_request=\"\"\"-----BEGIN CERTIFICATE REQUEST-----
        MIICvDCCAaQCAQAwdzELMAkGA1UEBhMCVVMxDTALBgNVBAgMBFV0YWgxDzANBgNV
        BAcMBkxpbmRvbjEWMBQGA1UECgwNRGlnaUNlcnQgSW5jLjERMA8GA1UECwwIRGln
        aUNlcnQxHTAbBgNVBAMMFGV4YW1wbGUuZGlnaWNlcnQuY29tMIIBIjANBgkqhkiG
        9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8+To7d+2kPWeBv/orU3LVbJwDrSQbeKamCmo
        wp5bqDxIwV20zqRb7APUOKYoVEFFOEQs6T6gImnIolhbiH6m4zgZ/CPvWBOkZc+c
        1Po2EmvBz+AD5sBdT5kzGQA6NbWyZGldxRthNLOs1efOhdnWFuhI162qmcflgpiI
        WDuwq4C9f+YkeJhNn9dF5+owm8cOQmDrV8NNdiTqin8q3qYAHHJRW28glJUCZkTZ
        wIaSR6crBQ8TbYNE0dc+Caa3DOIkz1EOsHWzTx+n0zKfqcbgXi4DJx+C1bjptYPR
        BPZL8DAeWuA8ebudVT44yEp82G96/Ggcf7F33xMxe0yc+Xa6owIDAQABoAAwDQYJ
        KoZIhvcNAQEFBQADggEBAB0kcrFccSmFDmxox0Ne01UIqSsDqHgL+XmHTXJwre6D
        hJSZwbvEtOK0G3+dr4Fs11WuUNt5qcLsx5a8uk4G6AKHMzuhLsJ7XZjgmQXGECpY
        Q4mC3yT3ZoCGpIXbw+iP3lmEEXgaQL0Tx5LFl/okKbKYwIqNiyKWOMj7ZR/wxWg/
        ZDGRs55xuoeLDJ/ZRFf9bI+IaCUd1YrfYcHIl3G87Av+r49YVwqRDT0VDV7uLgqn
        29XI1PpVUNCPQGn9p/eX6Qo7vpDaPybRtA2R7XLKjQaF9oXWeCUqy1hvJac9QFO2
        97Ob1alpHPoZ7mWiEuJwjBPii6a9M9G30nUo39lBi1w=
        -----END CERTIFICATE REQUEST-----\"\"\",
            signing_algorithm="SHA256WITHRSA",
            validity={
                "type": "DAYS",
                "value": 70,
            },
            opts = pulumi.ResourceOptions(depends_on=[subordinate_ca_two_activation]))
        pulumi.export("completeCertificateChain", subordinate_ca_two_activation.complete_certificate_chain)
        pulumi.export("certificateArn", end_entity_certificate.arn)

        ```

        :param str resource_name: The name of the resource.
        :param CertificateAuthorityArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateAuthorityArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 csr_extensions: Optional[pulumi.Input[Union['CertificateAuthorityCsrExtensionsArgs', 'CertificateAuthorityCsrExtensionsArgsDict']]] = None,
                 key_algorithm: Optional[pulumi.Input[str]] = None,
                 key_storage_security_standard: Optional[pulumi.Input[str]] = None,
                 revocation_configuration: Optional[pulumi.Input[Union['CertificateAuthorityRevocationConfigurationArgs', 'CertificateAuthorityRevocationConfigurationArgsDict']]] = None,
                 signing_algorithm: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[Union['CertificateAuthoritySubjectArgs', 'CertificateAuthoritySubjectArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['_root_inputs.TagArgs', '_root_inputs.TagArgsDict']]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 usage_mode: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CertificateAuthorityArgs.__new__(CertificateAuthorityArgs)

            __props__.__dict__["csr_extensions"] = csr_extensions
            if key_algorithm is None and not opts.urn:
                raise TypeError("Missing required property 'key_algorithm'")
            __props__.__dict__["key_algorithm"] = key_algorithm
            __props__.__dict__["key_storage_security_standard"] = key_storage_security_standard
            __props__.__dict__["revocation_configuration"] = revocation_configuration
            if signing_algorithm is None and not opts.urn:
                raise TypeError("Missing required property 'signing_algorithm'")
            __props__.__dict__["signing_algorithm"] = signing_algorithm
            if subject is None and not opts.urn:
                raise TypeError("Missing required property 'subject'")
            __props__.__dict__["subject"] = subject
            __props__.__dict__["tags"] = tags
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["usage_mode"] = usage_mode
            __props__.__dict__["arn"] = None
            __props__.__dict__["certificate_signing_request"] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=["csrExtensions", "keyAlgorithm", "keyStorageSecurityStandard", "signingAlgorithm", "subject", "type", "usageMode"])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(CertificateAuthority, __self__).__init__(
            'aws-native:acmpca:CertificateAuthority',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CertificateAuthority':
        """
        Get an existing CertificateAuthority resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CertificateAuthorityArgs.__new__(CertificateAuthorityArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["certificate_signing_request"] = None
        __props__.__dict__["csr_extensions"] = None
        __props__.__dict__["key_algorithm"] = None
        __props__.__dict__["key_storage_security_standard"] = None
        __props__.__dict__["revocation_configuration"] = None
        __props__.__dict__["signing_algorithm"] = None
        __props__.__dict__["subject"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["usage_mode"] = None
        return CertificateAuthority(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the certificate authority.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="certificateSigningRequest")
    def certificate_signing_request(self) -> pulumi.Output[str]:
        """
        The base64 PEM-encoded certificate signing request (CSR) for your certificate authority certificate.
        """
        return pulumi.get(self, "certificate_signing_request")

    @property
    @pulumi.getter(name="csrExtensions")
    def csr_extensions(self) -> pulumi.Output[Optional['outputs.CertificateAuthorityCsrExtensions']]:
        """
        Structure that contains CSR pass through extension information used by the CreateCertificateAuthority action.
        """
        return pulumi.get(self, "csr_extensions")

    @property
    @pulumi.getter(name="keyAlgorithm")
    def key_algorithm(self) -> pulumi.Output[str]:
        """
        Public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.
        """
        return pulumi.get(self, "key_algorithm")

    @property
    @pulumi.getter(name="keyStorageSecurityStandard")
    def key_storage_security_standard(self) -> pulumi.Output[Optional[str]]:
        """
        KeyStorageSecurityStadard defines a cryptographic key management compliance standard used for handling CA keys.
        """
        return pulumi.get(self, "key_storage_security_standard")

    @property
    @pulumi.getter(name="revocationConfiguration")
    def revocation_configuration(self) -> pulumi.Output[Optional['outputs.CertificateAuthorityRevocationConfiguration']]:
        """
        Certificate revocation information used by the CreateCertificateAuthority and UpdateCertificateAuthority actions.
        """
        return pulumi.get(self, "revocation_configuration")

    @property
    @pulumi.getter(name="signingAlgorithm")
    def signing_algorithm(self) -> pulumi.Output[str]:
        """
        Algorithm your CA uses to sign certificate requests.
        """
        return pulumi.get(self, "signing_algorithm")

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Output['outputs.CertificateAuthoritySubject']:
        """
        Structure that contains X.500 distinguished name information for your CA.
        """
        return pulumi.get(self, "subject")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['_root_outputs.Tag']]]:
        """
        Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see [Controlling Access Using IAM Tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html) .
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the certificate authority.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usageMode")
    def usage_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Usage mode of the ceritificate authority.
        """
        return pulumi.get(self, "usage_mode")

