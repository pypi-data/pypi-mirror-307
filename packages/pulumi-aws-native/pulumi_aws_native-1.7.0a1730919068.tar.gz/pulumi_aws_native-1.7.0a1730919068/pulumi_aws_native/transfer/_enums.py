# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AgreementStatus',
    'CertificateStatus',
    'CertificateType',
    'CertificateUsage',
    'ConnectorAs2ConfigPropertiesCompression',
    'ConnectorAs2ConfigPropertiesEncryptionAlgorithm',
    'ConnectorAs2ConfigPropertiesMdnResponse',
    'ConnectorAs2ConfigPropertiesMdnSigningAlgorithm',
    'ConnectorAs2ConfigPropertiesSigningAlgorithm',
    'ProfileType',
    'ServerAs2Transport',
    'ServerDirectoryListingOptimization',
    'ServerDomain',
    'ServerEndpointType',
    'ServerIdentityProviderType',
    'ServerProtocol',
    'ServerSetStatOption',
    'ServerSftpAuthenticationMethods',
    'ServerTlsSessionResumptionMode',
    'WorkflowStepCopyStepDetailsPropertiesOverwriteExisting',
    'WorkflowStepDecryptStepDetailsPropertiesOverwriteExisting',
    'WorkflowStepDecryptStepDetailsPropertiesType',
    'WorkflowStepType',
]


class AgreementStatus(str, Enum):
    """
    Specifies the status of the agreement.
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CertificateStatus(str, Enum):
    """
    A status description for the certificate.
    """
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    INACTIVE = "INACTIVE"


class CertificateType(str, Enum):
    """
    Describing the type of certificate. With or without a private key.
    """
    CERTIFICATE = "CERTIFICATE"
    CERTIFICATE_WITH_PRIVATE_KEY = "CERTIFICATE_WITH_PRIVATE_KEY"


class CertificateUsage(str, Enum):
    """
    Specifies the usage type for the certificate.
    """
    SIGNING = "SIGNING"
    ENCRYPTION = "ENCRYPTION"
    TLS = "TLS"


class ConnectorAs2ConfigPropertiesCompression(str, Enum):
    """
    Compression setting for this AS2 connector configuration.
    """
    ZLIB = "ZLIB"
    DISABLED = "DISABLED"


class ConnectorAs2ConfigPropertiesEncryptionAlgorithm(str, Enum):
    """
    Encryption algorithm for this AS2 connector configuration.
    """
    AES128_CBC = "AES128_CBC"
    AES192_CBC = "AES192_CBC"
    AES256_CBC = "AES256_CBC"
    NONE = "NONE"
    DES_EDE3_CBC = "DES_EDE3_CBC"


class ConnectorAs2ConfigPropertiesMdnResponse(str, Enum):
    """
    MDN Response setting for this AS2 connector configuration.
    """
    SYNC = "SYNC"
    NONE = "NONE"


class ConnectorAs2ConfigPropertiesMdnSigningAlgorithm(str, Enum):
    """
    MDN Signing algorithm for this AS2 connector configuration.
    """
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"
    SHA1 = "SHA1"
    NONE = "NONE"
    DEFAULT = "DEFAULT"


class ConnectorAs2ConfigPropertiesSigningAlgorithm(str, Enum):
    """
    Signing algorithm for this AS2 connector configuration.
    """
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"
    SHA1 = "SHA1"
    NONE = "NONE"


class ProfileType(str, Enum):
    """
    Enum specifying whether the profile is local or associated with a trading partner.
    """
    LOCAL = "LOCAL"
    PARTNER = "PARTNER"


class ServerAs2Transport(str, Enum):
    HTTP = "HTTP"


class ServerDirectoryListingOptimization(str, Enum):
    """
    Indicates whether optimization to directory listing on S3 servers is used. Disabled by default for compatibility.
    """
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ServerDomain(str, Enum):
    S3 = "S3"
    EFS = "EFS"


class ServerEndpointType(str, Enum):
    PUBLIC = "PUBLIC"
    VPC = "VPC"
    VPC_ENDPOINT = "VPC_ENDPOINT"


class ServerIdentityProviderType(str, Enum):
    SERVICE_MANAGED = "SERVICE_MANAGED"
    API_GATEWAY = "API_GATEWAY"
    AWS_DIRECTORY_SERVICE = "AWS_DIRECTORY_SERVICE"
    AWS_LAMBDA = "AWS_LAMBDA"


class ServerProtocol(str, Enum):
    SFTP = "SFTP"
    FTP = "FTP"
    FTPS = "FTPS"
    AS2 = "AS2"


class ServerSetStatOption(str, Enum):
    DEFAULT = "DEFAULT"
    ENABLE_NO_OP = "ENABLE_NO_OP"


class ServerSftpAuthenticationMethods(str, Enum):
    PASSWORD = "PASSWORD"
    PUBLIC_KEY = "PUBLIC_KEY"
    PUBLIC_KEY_OR_PASSWORD = "PUBLIC_KEY_OR_PASSWORD"
    PUBLIC_KEY_AND_PASSWORD = "PUBLIC_KEY_AND_PASSWORD"


class ServerTlsSessionResumptionMode(str, Enum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    ENFORCED = "ENFORCED"


class WorkflowStepCopyStepDetailsPropertiesOverwriteExisting(str, Enum):
    """
    A flag that indicates whether or not to overwrite an existing file of the same name. The default is FALSE.
    """
    TRUE = "TRUE"
    FALSE = "FALSE"


class WorkflowStepDecryptStepDetailsPropertiesOverwriteExisting(str, Enum):
    """
    A flag that indicates whether or not to overwrite an existing file of the same name. The default is FALSE.
    """
    TRUE = "TRUE"
    FALSE = "FALSE"


class WorkflowStepDecryptStepDetailsPropertiesType(str, Enum):
    """
    Specifies which encryption method to use.
    """
    PGP = "PGP"


class WorkflowStepType(str, Enum):
    COPY = "COPY"
    CUSTOM = "CUSTOM"
    DECRYPT = "DECRYPT"
    DELETE = "DELETE"
    TAG = "TAG"
