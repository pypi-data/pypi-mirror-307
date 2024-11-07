# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'CapacityReservationFleetInstanceMatchCriteria',
    'CapacityReservationFleetTenancy',
    'Ec2FleetCapacityRebalanceReplacementStrategy',
    'Ec2FleetCapacityReservationOptionsRequestUsageStrategy',
    'Ec2FleetExcessCapacityTerminationPolicy',
    'Ec2FleetInstanceRequirementsRequestAcceleratorManufacturersItem',
    'Ec2FleetInstanceRequirementsRequestAcceleratorNamesItem',
    'Ec2FleetInstanceRequirementsRequestAcceleratorTypesItem',
    'Ec2FleetInstanceRequirementsRequestBareMetal',
    'Ec2FleetInstanceRequirementsRequestBurstablePerformance',
    'Ec2FleetInstanceRequirementsRequestCpuManufacturersItem',
    'Ec2FleetInstanceRequirementsRequestInstanceGenerationsItem',
    'Ec2FleetInstanceRequirementsRequestLocalStorage',
    'Ec2FleetInstanceRequirementsRequestLocalStorageTypesItem',
    'Ec2FleetSpotOptionsRequestAllocationStrategy',
    'Ec2FleetSpotOptionsRequestInstanceInterruptionBehavior',
    'Ec2FleetTagSpecificationResourceType',
    'Ec2FleetTargetCapacitySpecificationRequestDefaultTargetCapacityType',
    'Ec2FleetTargetCapacitySpecificationRequestTargetCapacityUnitType',
    'Ec2FleetType',
    'FlowLogDestinationOptionsPropertiesFileFormat',
    'FlowLogLogDestinationType',
    'FlowLogResourceType',
    'FlowLogTrafficType',
    'InstanceAffinity',
    'InstancePrivateDnsNameOptionsHostnameType',
    'IpamPoolAwsService',
    'IpamPoolIpamScopeType',
    'IpamPoolPublicIpSource',
    'IpamPoolState',
    'IpamScopeType',
    'IpamTier',
    'KeyPairKeyFormat',
    'KeyPairKeyType',
    'LaunchTemplateCpuOptionsAmdSevSnp',
    'NetworkInsightsAccessScopeAnalysisFindingsFound',
    'NetworkInsightsAccessScopeAnalysisStatus',
    'NetworkInsightsAccessScopeProtocol',
    'NetworkInsightsAnalysisStatus',
    'NetworkInsightsPathProtocol',
    'PrefixListAddressFamily',
    'SnapshotBlockPublicAccessState',
    'SpotFleetEbsBlockDeviceVolumeType',
    'SpotFleetInstanceRequirementsRequestAcceleratorManufacturersItem',
    'SpotFleetInstanceRequirementsRequestAcceleratorNamesItem',
    'SpotFleetInstanceRequirementsRequestAcceleratorTypesItem',
    'SpotFleetInstanceRequirementsRequestBareMetal',
    'SpotFleetInstanceRequirementsRequestBurstablePerformance',
    'SpotFleetInstanceRequirementsRequestCpuManufacturersItem',
    'SpotFleetInstanceRequirementsRequestInstanceGenerationsItem',
    'SpotFleetInstanceRequirementsRequestLocalStorage',
    'SpotFleetInstanceRequirementsRequestLocalStorageTypesItem',
    'SpotFleetRequestConfigDataAllocationStrategy',
    'SpotFleetRequestConfigDataExcessCapacityTerminationPolicy',
    'SpotFleetRequestConfigDataInstanceInterruptionBehavior',
    'SpotFleetRequestConfigDataTargetCapacityUnitType',
    'SpotFleetRequestConfigDataType',
    'SpotFleetSpotCapacityRebalanceReplacementStrategy',
    'SpotFleetSpotPlacementTenancy',
    'SpotFleetTagSpecificationResourceType',
    'VpcEndpointType',
    'VpnConnectionCloudwatchLogOptionsSpecificationLogOutputFormat',
    'VpnConnectionIkeVersionsRequestListValueValue',
    'VpnConnectionPhase1EncryptionAlgorithmsRequestListValueValue',
    'VpnConnectionPhase1IntegrityAlgorithmsRequestListValueValue',
    'VpnConnectionPhase2EncryptionAlgorithmsRequestListValueValue',
    'VpnConnectionPhase2IntegrityAlgorithmsRequestListValueValue',
    'VpnConnectionVpnTunnelOptionsSpecificationDpdTimeoutAction',
    'VpnConnectionVpnTunnelOptionsSpecificationStartupAction',
]


class CapacityReservationFleetInstanceMatchCriteria(str, Enum):
    """
    Indicates the type of instance launches that the Capacity Reservation Fleet accepts. All Capacity Reservations in the Fleet inherit this instance matching criteria.

    Currently, Capacity Reservation Fleets support `open` instance matching criteria only. This means that instances that have matching attributes (instance type, platform, and Availability Zone) run in the Capacity Reservations automatically. Instances do not need to explicitly target a Capacity Reservation Fleet to use its reserved capacity.
    """
    OPEN = "open"


class CapacityReservationFleetTenancy(str, Enum):
    """
    Indicates the tenancy of the Capacity Reservation Fleet. All Capacity Reservations in the Fleet inherit this tenancy. The Capacity Reservation Fleet can have one of the following tenancy settings:

    - `default` - The Capacity Reservation Fleet is created on hardware that is shared with other AWS accounts .
    - `dedicated` - The Capacity Reservations are created on single-tenant hardware that is dedicated to a single AWS account .
    """
    DEFAULT = "default"


class Ec2FleetCapacityRebalanceReplacementStrategy(str, Enum):
    """
    The replacement strategy to use. Only available for fleets of type `maintain` .

    `launch` - EC2 Fleet launches a replacement Spot Instance when a rebalance notification is emitted for an existing Spot Instance in the fleet. EC2 Fleet does not terminate the instances that receive a rebalance notification. You can terminate the old instances, or you can leave them running. You are charged for all instances while they are running.

    `launch-before-terminate` - EC2 Fleet launches a replacement Spot Instance when a rebalance notification is emitted for an existing Spot Instance in the fleet, and then, after a delay that you specify (in `TerminationDelay` ), terminates the instances that received a rebalance notification.
    """
    LAUNCH = "launch"
    LAUNCH_BEFORE_TERMINATE = "launch-before-terminate"


class Ec2FleetCapacityReservationOptionsRequestUsageStrategy(str, Enum):
    """
    Indicates whether to use unused Capacity Reservations for fulfilling On-Demand capacity.

    If you specify `use-capacity-reservations-first` , the fleet uses unused Capacity Reservations to fulfill On-Demand capacity up to the target On-Demand capacity. If multiple instance pools have unused Capacity Reservations, the On-Demand allocation strategy ( `lowest-price` or `prioritized` ) is applied. If the number of unused Capacity Reservations is less than the On-Demand target capacity, the remaining On-Demand target capacity is launched according to the On-Demand allocation strategy ( `lowest-price` or `prioritized` ).

    If you do not specify a value, the fleet fulfils the On-Demand capacity according to the chosen On-Demand allocation strategy.
    """
    USE_CAPACITY_RESERVATIONS_FIRST = "use-capacity-reservations-first"


class Ec2FleetExcessCapacityTerminationPolicy(str, Enum):
    """
    Indicates whether running instances should be terminated if the total target capacity of the EC2 Fleet is decreased below the current size of the EC2 Fleet.

    Supported only for fleets of type `maintain` .
    """
    TERMINATION = "termination"
    NO_TERMINATION = "no-termination"


class Ec2FleetInstanceRequirementsRequestAcceleratorManufacturersItem(str, Enum):
    AMAZON_WEB_SERVICES = "amazon-web-services"
    AMD = "amd"
    HABANA = "habana"
    NVIDIA = "nvidia"
    XILINX = "xilinx"


class Ec2FleetInstanceRequirementsRequestAcceleratorNamesItem(str, Enum):
    A10G = "a10g"
    A100 = "a100"
    H100 = "h100"
    INFERENTIA = "inferentia"
    K520 = "k520"
    K80 = "k80"
    M60 = "m60"
    RADEON_PRO_V520 = "radeon-pro-v520"
    T4 = "t4"
    T4G = "t4g"
    VU9P = "vu9p"
    V100 = "v100"


class Ec2FleetInstanceRequirementsRequestAcceleratorTypesItem(str, Enum):
    GPU = "gpu"
    FPGA = "fpga"
    INFERENCE = "inference"


class Ec2FleetInstanceRequirementsRequestBareMetal(str, Enum):
    """
    Indicates whether bare metal instance types must be included, excluded, or required.

    - To include bare metal instance types, specify `included` .
    - To require only bare metal instance types, specify `required` .
    - To exclude bare metal instance types, specify `excluded` .

    Default: `excluded`
    """
    INCLUDED = "included"
    REQUIRED = "required"
    EXCLUDED = "excluded"


class Ec2FleetInstanceRequirementsRequestBurstablePerformance(str, Enum):
    """
    Indicates whether burstable performance T instance types are included, excluded, or required. For more information, see [Burstable performance instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html) .

    - To include burstable performance instance types, specify `included` .
    - To require only burstable performance instance types, specify `required` .
    - To exclude burstable performance instance types, specify `excluded` .

    Default: `excluded`
    """
    INCLUDED = "included"
    REQUIRED = "required"
    EXCLUDED = "excluded"


class Ec2FleetInstanceRequirementsRequestCpuManufacturersItem(str, Enum):
    INTEL = "intel"
    AMD = "amd"
    AMAZON_WEB_SERVICES = "amazon-web-services"


class Ec2FleetInstanceRequirementsRequestInstanceGenerationsItem(str, Enum):
    CURRENT = "current"
    PREVIOUS = "previous"


class Ec2FleetInstanceRequirementsRequestLocalStorage(str, Enum):
    """
    Indicates whether instance types with instance store volumes are included, excluded, or required. For more information, [Amazon EC2 instance store](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html) in the *Amazon EC2 User Guide* .

    - To include instance types with instance store volumes, specify `included` .
    - To require only instance types with instance store volumes, specify `required` .
    - To exclude instance types with instance store volumes, specify `excluded` .

    Default: `included`
    """
    INCLUDED = "included"
    REQUIRED = "required"
    EXCLUDED = "excluded"


class Ec2FleetInstanceRequirementsRequestLocalStorageTypesItem(str, Enum):
    HDD = "hdd"
    SSD = "ssd"


class Ec2FleetSpotOptionsRequestAllocationStrategy(str, Enum):
    """
    Indicates how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the EC2 Fleet.

    If the allocation strategy is `lowestPrice` , EC2 Fleet launches instances from the Spot Instance pools with the lowest price. This is the default allocation strategy.

    If the allocation strategy is `diversified` , EC2 Fleet launches instances from all the Spot Instance pools that you specify.

    If the allocation strategy is `capacityOptimized` , EC2 Fleet launches instances from Spot Instance pools that are optimally chosen based on the available Spot Instance capacity.

    *Allowed Values* : `lowestPrice` | `diversified` | `capacityOptimized` | `capacityOptimizedPrioritized`
    """
    LOWEST_PRICE = "lowest-price"
    DIVERSIFIED = "diversified"
    CAPACITY_OPTIMIZED = "capacityOptimized"
    CAPACITY_OPTIMIZED_PRIORITIZED = "capacityOptimizedPrioritized"
    PRICE_CAPACITY_OPTIMIZED = "priceCapacityOptimized"


class Ec2FleetSpotOptionsRequestInstanceInterruptionBehavior(str, Enum):
    """
    The behavior when a Spot Instance is interrupted.

    Default: `terminate`
    """
    HIBERNATE = "hibernate"
    STOP = "stop"
    TERMINATE = "terminate"


class Ec2FleetTagSpecificationResourceType(str, Enum):
    """
    The type of resource to tag.
    """
    CLIENT_VPN_ENDPOINT = "client-vpn-endpoint"
    CUSTOMER_GATEWAY = "customer-gateway"
    DEDICATED_HOST = "dedicated-host"
    DHCP_OPTIONS = "dhcp-options"
    EGRESS_ONLY_INTERNET_GATEWAY = "egress-only-internet-gateway"
    ELASTIC_GPU = "elastic-gpu"
    ELASTIC_IP = "elastic-ip"
    EXPORT_IMAGE_TASK = "export-image-task"
    EXPORT_INSTANCE_TASK = "export-instance-task"
    FLEET = "fleet"
    FPGA_IMAGE = "fpga-image"
    HOST_RESERVATION = "host-reservation"
    IMAGE = "image"
    IMPORT_IMAGE_TASK = "import-image-task"
    IMPORT_SNAPSHOT_TASK = "import-snapshot-task"
    INSTANCE = "instance"
    INTERNET_GATEWAY = "internet-gateway"
    KEY_PAIR = "key-pair"
    LAUNCH_TEMPLATE = "launch-template"
    LOCAL_GATEWAY_ROUTE_TABLE_VPC_ASSOCIATION = "local-gateway-route-table-vpc-association"
    NATGATEWAY = "natgateway"
    NETWORK_ACL = "network-acl"
    NETWORK_INSIGHTS_ANALYSIS = "network-insights-analysis"
    NETWORK_INSIGHTS_PATH = "network-insights-path"
    NETWORK_INTERFACE = "network-interface"
    PLACEMENT_GROUP = "placement-group"
    RESERVED_INSTANCES = "reserved-instances"
    ROUTE_TABLE = "route-table"
    SECURITY_GROUP = "security-group"
    SNAPSHOT = "snapshot"
    SPOT_FLEET_REQUEST = "spot-fleet-request"
    SPOT_INSTANCES_REQUEST = "spot-instances-request"
    SUBNET = "subnet"
    TRAFFIC_MIRROR_FILTER = "traffic-mirror-filter"
    TRAFFIC_MIRROR_SESSION = "traffic-mirror-session"
    TRAFFIC_MIRROR_TARGET = "traffic-mirror-target"
    TRANSIT_GATEWAY = "transit-gateway"
    TRANSIT_GATEWAY_ATTACHMENT = "transit-gateway-attachment"
    TRANSIT_GATEWAY_CONNECT_PEER = "transit-gateway-connect-peer"
    TRANSIT_GATEWAY_MULTICAST_DOMAIN = "transit-gateway-multicast-domain"
    TRANSIT_GATEWAY_ROUTE_TABLE = "transit-gateway-route-table"
    VOLUME = "volume"
    VPC = "vpc"
    VPC_FLOW_LOG = "vpc-flow-log"
    VPC_PEERING_CONNECTION = "vpc-peering-connection"
    VPN_CONNECTION = "vpn-connection"
    VPN_GATEWAY = "vpn-gateway"


class Ec2FleetTargetCapacitySpecificationRequestDefaultTargetCapacityType(str, Enum):
    """
    The default target capacity type.
    """
    ON_DEMAND = "on-demand"
    SPOT = "spot"


class Ec2FleetTargetCapacitySpecificationRequestTargetCapacityUnitType(str, Enum):
    """
    The unit for the target capacity. You can specify this parameter only when using attributed-based instance type selection.

    Default: `units` (the number of instances)
    """
    VCPU = "vcpu"
    MEMORY_MIB = "memory-mib"
    UNITS = "units"


class Ec2FleetType(str, Enum):
    """
    The fleet type. The default value is `maintain` .

    - `maintain` - The EC2 Fleet places an asynchronous request for your desired capacity, and continues to maintain your desired Spot capacity by replenishing interrupted Spot Instances.
    - `request` - The EC2 Fleet places an asynchronous one-time request for your desired capacity, but does submit Spot requests in alternative capacity pools if Spot capacity is unavailable, and does not maintain Spot capacity if Spot Instances are interrupted.
    - `instant` - The EC2 Fleet places a synchronous one-time request for your desired capacity, and returns errors for any instances that could not be launched.

    For more information, see [EC2 Fleet request types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-request-type.html) in the *Amazon EC2 User Guide* .
    """
    MAINTAIN = "maintain"
    REQUEST = "request"
    INSTANT = "instant"


class FlowLogDestinationOptionsPropertiesFileFormat(str, Enum):
    """
    The format for the flow log. The default is `plain-text` .
    """
    PLAIN_TEXT = "plain-text"
    PARQUET = "parquet"


class FlowLogLogDestinationType(str, Enum):
    """
    Specifies the type of destination to which the flow log data is to be published. Flow log data can be published to CloudWatch Logs or Amazon S3.
    """
    CLOUD_WATCH_LOGS = "cloud-watch-logs"
    S3 = "s3"
    KINESIS_DATA_FIREHOSE = "kinesis-data-firehose"


class FlowLogResourceType(str, Enum):
    """
    The type of resource for which to create the flow log. For example, if you specified a VPC ID for the ResourceId property, specify VPC for this property.
    """
    NETWORK_INTERFACE = "NetworkInterface"
    SUBNET = "Subnet"
    VPC = "VPC"
    TRANSIT_GATEWAY = "TransitGateway"
    TRANSIT_GATEWAY_ATTACHMENT = "TransitGatewayAttachment"


class FlowLogTrafficType(str, Enum):
    """
    The type of traffic to log. You can log traffic that the resource accepts or rejects, or all traffic.
    """
    ACCEPT = "ACCEPT"
    ALL = "ALL"
    REJECT = "REJECT"


class InstanceAffinity(str, Enum):
    """
    Indicates whether the instance is associated with a dedicated host. If you want the instance to always restart on the same host on which it was launched, specify host. If you want the instance to restart on any available host, but try to launch onto the last host it ran on (on a best-effort basis), specify default.
    """
    DEFAULT = "default"
    HOST = "host"


class InstancePrivateDnsNameOptionsHostnameType(str, Enum):
    """
    The type of hostnames to assign to instances in the subnet at launch. For IPv4 only subnets, an instance DNS name must be based on the instance IPv4 address. For IPv6 only subnets, an instance DNS name must be based on the instance ID. For dual-stack subnets, you can specify whether DNS names use the instance IPv4 address or the instance ID. For more information, see Amazon EC2 instance hostname types in the Amazon Elastic Compute Cloud User Guide.
    """
    IP_NAME = "ip-name"
    RESOURCE_NAME = "resource-name"


class IpamPoolAwsService(str, Enum):
    """
    Limits which service in Amazon Web Services that the pool can be used in.
    """
    EC2 = "ec2"


class IpamPoolIpamScopeType(str, Enum):
    """
    Determines whether this scope contains publicly routable space or space for a private network
    """
    PUBLIC = "public"
    PRIVATE = "private"


class IpamPoolPublicIpSource(str, Enum):
    """
    The IP address source for pools in the public scope. Only used for provisioning IP address CIDRs to pools in the public scope. Default is `byoip`.
    """
    BYOIP = "byoip"
    AMAZON = "amazon"


class IpamPoolState(str, Enum):
    """
    The state of this pool. This can be one of the following values: "create-in-progress", "create-complete", "modify-in-progress", "modify-complete", "delete-in-progress", or "delete-complete"
    """
    CREATE_IN_PROGRESS = "create-in-progress"
    CREATE_COMPLETE = "create-complete"
    MODIFY_IN_PROGRESS = "modify-in-progress"
    MODIFY_COMPLETE = "modify-complete"
    DELETE_IN_PROGRESS = "delete-in-progress"
    DELETE_COMPLETE = "delete-complete"


class IpamScopeType(str, Enum):
    """
    Determines whether this scope contains publicly routable space or space for a private network
    """
    PUBLIC = "public"
    PRIVATE = "private"


class IpamTier(str, Enum):
    """
    The tier of the IPAM.
    """
    FREE = "free"
    ADVANCED = "advanced"


class KeyPairKeyFormat(str, Enum):
    """
    The format of the key pair.
     Default: ``pem``
    """
    PEM = "pem"
    PPK = "ppk"


class KeyPairKeyType(str, Enum):
    """
    The type of key pair. Note that ED25519 keys are not supported for Windows instances.
     If the ``PublicKeyMaterial`` property is specified, the ``KeyType`` property is ignored, and the key type is inferred from the ``PublicKeyMaterial`` value.
     Default: ``rsa``
    """
    RSA = "rsa"
    ED25519 = "ed25519"


class LaunchTemplateCpuOptionsAmdSevSnp(str, Enum):
    """
    Indicates whether to enable the instance for AMD SEV-SNP. AMD SEV-SNP is supported with M6a, R6a, and C6a instance types only. For more information, see [AMD SEV-SNP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sev-snp.html).
    """
    ENABLED = "enabled"
    DISABLED = "disabled"


class NetworkInsightsAccessScopeAnalysisFindingsFound(str, Enum):
    """
    Indicates whether there are findings (true | false | unknown).
    """
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class NetworkInsightsAccessScopeAnalysisStatus(str, Enum):
    """
    The status of the analysis (running | succeeded | failed).
    """
    RUNNING = "running"
    FAILED = "failed"
    SUCCEEDED = "succeeded"


class NetworkInsightsAccessScopeProtocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class NetworkInsightsAnalysisStatus(str, Enum):
    """
    The status of the network insights analysis.
    """
    RUNNING = "running"
    FAILED = "failed"
    SUCCEEDED = "succeeded"


class NetworkInsightsPathProtocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class PrefixListAddressFamily(str, Enum):
    """
    Ip Version of Prefix List.
    """
    I_PV4 = "IPv4"
    I_PV6 = "IPv6"


class SnapshotBlockPublicAccessState(str, Enum):
    """
    The state of EBS Snapshot Block Public Access.
    """
    BLOCK_ALL_SHARING = "block-all-sharing"
    BLOCK_NEW_SHARING = "block-new-sharing"


class SpotFleetEbsBlockDeviceVolumeType(str, Enum):
    """
    The volume type. For more information, see [Amazon EBS volume types](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html) in the *Amazon EBS User Guide* .
    """
    GP2 = "gp2"
    GP3 = "gp3"
    IO1 = "io1"
    IO2 = "io2"
    SC1 = "sc1"
    ST1 = "st1"
    STANDARD = "standard"


class SpotFleetInstanceRequirementsRequestAcceleratorManufacturersItem(str, Enum):
    AMAZON_WEB_SERVICES = "amazon-web-services"
    AMD = "amd"
    HABANA = "habana"
    NVIDIA = "nvidia"
    XILINX = "xilinx"


class SpotFleetInstanceRequirementsRequestAcceleratorNamesItem(str, Enum):
    A10G = "a10g"
    A100 = "a100"
    H100 = "h100"
    INFERENTIA = "inferentia"
    K520 = "k520"
    K80 = "k80"
    M60 = "m60"
    RADEON_PRO_V520 = "radeon-pro-v520"
    T4 = "t4"
    T4G = "t4g"
    VU9P = "vu9p"
    V100 = "v100"


class SpotFleetInstanceRequirementsRequestAcceleratorTypesItem(str, Enum):
    GPU = "gpu"
    FPGA = "fpga"
    INFERENCE = "inference"


class SpotFleetInstanceRequirementsRequestBareMetal(str, Enum):
    """
    Indicates whether bare metal instance types must be included, excluded, or required.

    - To include bare metal instance types, specify `included` .
    - To require only bare metal instance types, specify `required` .
    - To exclude bare metal instance types, specify `excluded` .

    Default: `excluded`
    """
    INCLUDED = "included"
    REQUIRED = "required"
    EXCLUDED = "excluded"


class SpotFleetInstanceRequirementsRequestBurstablePerformance(str, Enum):
    """
    Indicates whether burstable performance T instance types are included, excluded, or required. For more information, see [Burstable performance instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html) .

    - To include burstable performance instance types, specify `included` .
    - To require only burstable performance instance types, specify `required` .
    - To exclude burstable performance instance types, specify `excluded` .

    Default: `excluded`
    """
    INCLUDED = "included"
    REQUIRED = "required"
    EXCLUDED = "excluded"


class SpotFleetInstanceRequirementsRequestCpuManufacturersItem(str, Enum):
    INTEL = "intel"
    AMD = "amd"
    AMAZON_WEB_SERVICES = "amazon-web-services"


class SpotFleetInstanceRequirementsRequestInstanceGenerationsItem(str, Enum):
    CURRENT = "current"
    PREVIOUS = "previous"


class SpotFleetInstanceRequirementsRequestLocalStorage(str, Enum):
    """
    Indicates whether instance types with instance store volumes are included, excluded, or required. For more information, [Amazon EC2 instance store](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html) in the *Amazon EC2 User Guide* .

    - To include instance types with instance store volumes, specify `included` .
    - To require only instance types with instance store volumes, specify `required` .
    - To exclude instance types with instance store volumes, specify `excluded` .

    Default: `included`
    """
    INCLUDED = "included"
    REQUIRED = "required"
    EXCLUDED = "excluded"


class SpotFleetInstanceRequirementsRequestLocalStorageTypesItem(str, Enum):
    HDD = "hdd"
    SSD = "ssd"


class SpotFleetRequestConfigDataAllocationStrategy(str, Enum):
    """
    The strategy that determines how to allocate the target Spot Instance capacity across the Spot Instance pools specified by the Spot Fleet launch configuration. For more information, see [Allocation strategies for Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet-allocation-strategy.html) in the *Amazon EC2 User Guide* .

    - **priceCapacityOptimized (recommended)** - Spot Fleet identifies the pools with the highest capacity availability for the number of instances that are launching. This means that we will request Spot Instances from the pools that we believe have the lowest chance of interruption in the near term. Spot Fleet then requests Spot Instances from the lowest priced of these pools.
    - **capacityOptimized** - Spot Fleet identifies the pools with the highest capacity availability for the number of instances that are launching. This means that we will request Spot Instances from the pools that we believe have the lowest chance of interruption in the near term. To give certain instance types a higher chance of launching first, use `capacityOptimizedPrioritized` . Set a priority for each instance type by using the `Priority` parameter for `LaunchTemplateOverrides` . You can assign the same priority to different `LaunchTemplateOverrides` . EC2 implements the priorities on a best-effort basis, but optimizes for capacity first. `capacityOptimizedPrioritized` is supported only if your Spot Fleet uses a launch template. Note that if the `OnDemandAllocationStrategy` is set to `prioritized` , the same priority is applied when fulfilling On-Demand capacity.
    - **diversified** - Spot Fleet requests instances from all of the Spot Instance pools that you specify.
    - **lowestPrice (not recommended)** - > We don't recommend the `lowestPrice` allocation strategy because it has the highest risk of interruption for your Spot Instances. 

    Spot Fleet requests instances from the lowest priced Spot Instance pool that has available capacity. If the lowest priced pool doesn't have available capacity, the Spot Instances come from the next lowest priced pool that has available capacity. If a pool runs out of capacity before fulfilling your desired capacity, Spot Fleet will continue to fulfill your request by drawing from the next lowest priced pool. To ensure that your desired capacity is met, you might receive Spot Instances from several pools. Because this strategy only considers instance price and not capacity availability, it might lead to high interruption rates.

    Default: `lowestPrice`
    """
    CAPACITY_OPTIMIZED = "capacityOptimized"
    CAPACITY_OPTIMIZED_PRIORITIZED = "capacityOptimizedPrioritized"
    DIVERSIFIED = "diversified"
    LOWEST_PRICE = "lowestPrice"
    PRICE_CAPACITY_OPTIMIZED = "priceCapacityOptimized"


class SpotFleetRequestConfigDataExcessCapacityTerminationPolicy(str, Enum):
    """
    Indicates whether running Spot Instances should be terminated if you decrease the target capacity of the Spot Fleet request below the current size of the Spot Fleet.

    Supported only for fleets of type `maintain` .
    """
    DEFAULT = "Default"
    NO_TERMINATION = "NoTermination"


class SpotFleetRequestConfigDataInstanceInterruptionBehavior(str, Enum):
    """
    The behavior when a Spot Instance is interrupted. The default is `terminate` .
    """
    HIBERNATE = "hibernate"
    STOP = "stop"
    TERMINATE = "terminate"


class SpotFleetRequestConfigDataTargetCapacityUnitType(str, Enum):
    """
    The unit for the target capacity. You can specify this parameter only when using attribute-based instance type selection.

    Default: `units` (the number of instances)
    """
    VCPU = "vcpu"
    MEMORY_MIB = "memory-mib"
    UNITS = "units"


class SpotFleetRequestConfigDataType(str, Enum):
    """
    The type of request. Indicates whether the Spot Fleet only requests the target capacity or also attempts to maintain it. When this value is `request` , the Spot Fleet only places the required requests. It does not attempt to replenish Spot Instances if capacity is diminished, nor does it submit requests in alternative Spot pools if capacity is not available. When this value is `maintain` , the Spot Fleet maintains the target capacity. The Spot Fleet places the required requests to meet capacity and automatically replenishes any interrupted instances. Default: `maintain` . `instant` is listed but is not used by Spot Fleet.
    """
    MAINTAIN = "maintain"
    REQUEST = "request"


class SpotFleetSpotCapacityRebalanceReplacementStrategy(str, Enum):
    """
    The replacement strategy to use. Only available for fleets of type `maintain` .

    `launch` - Spot Fleet launches a new replacement Spot Instance when a rebalance notification is emitted for an existing Spot Instance in the fleet. Spot Fleet does not terminate the instances that receive a rebalance notification. You can terminate the old instances, or you can leave them running. You are charged for all instances while they are running.

    `launch-before-terminate` - Spot Fleet launches a new replacement Spot Instance when a rebalance notification is emitted for an existing Spot Instance in the fleet, and then, after a delay that you specify (in `TerminationDelay` ), terminates the instances that received a rebalance notification.
    """
    LAUNCH = "launch"
    LAUNCH_BEFORE_TERMINATE = "launch-before-terminate"


class SpotFleetSpotPlacementTenancy(str, Enum):
    """
    The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of `dedicated` runs on single-tenant hardware. The `host` tenancy is not supported for Spot Instances.
    """
    DEDICATED = "dedicated"
    DEFAULT = "default"
    HOST = "host"


class SpotFleetTagSpecificationResourceType(str, Enum):
    """
    The type of resource. Currently, the only resource type that is supported is `instance` . To tag the Spot Fleet request on creation, use the `TagSpecifications` parameter in `[SpotFleetRequestConfigData](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_SpotFleetRequestConfigData.html)` .
    """
    CLIENT_VPN_ENDPOINT = "client-vpn-endpoint"
    CUSTOMER_GATEWAY = "customer-gateway"
    DEDICATED_HOST = "dedicated-host"
    DHCP_OPTIONS = "dhcp-options"
    EGRESS_ONLY_INTERNET_GATEWAY = "egress-only-internet-gateway"
    ELASTIC_GPU = "elastic-gpu"
    ELASTIC_IP = "elastic-ip"
    EXPORT_IMAGE_TASK = "export-image-task"
    EXPORT_INSTANCE_TASK = "export-instance-task"
    FLEET = "fleet"
    FPGA_IMAGE = "fpga-image"
    HOST_RESERVATION = "host-reservation"
    IMAGE = "image"
    IMPORT_IMAGE_TASK = "import-image-task"
    IMPORT_SNAPSHOT_TASK = "import-snapshot-task"
    INSTANCE = "instance"
    INTERNET_GATEWAY = "internet-gateway"
    KEY_PAIR = "key-pair"
    LAUNCH_TEMPLATE = "launch-template"
    LOCAL_GATEWAY_ROUTE_TABLE_VPC_ASSOCIATION = "local-gateway-route-table-vpc-association"
    NATGATEWAY = "natgateway"
    NETWORK_ACL = "network-acl"
    NETWORK_INSIGHTS_ANALYSIS = "network-insights-analysis"
    NETWORK_INSIGHTS_PATH = "network-insights-path"
    NETWORK_INTERFACE = "network-interface"
    PLACEMENT_GROUP = "placement-group"
    RESERVED_INSTANCES = "reserved-instances"
    ROUTE_TABLE = "route-table"
    SECURITY_GROUP = "security-group"
    SNAPSHOT = "snapshot"
    SPOT_FLEET_REQUEST = "spot-fleet-request"
    SPOT_INSTANCES_REQUEST = "spot-instances-request"
    SUBNET = "subnet"
    TRAFFIC_MIRROR_FILTER = "traffic-mirror-filter"
    TRAFFIC_MIRROR_SESSION = "traffic-mirror-session"
    TRAFFIC_MIRROR_TARGET = "traffic-mirror-target"
    TRANSIT_GATEWAY = "transit-gateway"
    TRANSIT_GATEWAY_ATTACHMENT = "transit-gateway-attachment"
    TRANSIT_GATEWAY_CONNECT_PEER = "transit-gateway-connect-peer"
    TRANSIT_GATEWAY_MULTICAST_DOMAIN = "transit-gateway-multicast-domain"
    TRANSIT_GATEWAY_ROUTE_TABLE = "transit-gateway-route-table"
    VOLUME = "volume"
    VPC = "vpc"
    VPC_FLOW_LOG = "vpc-flow-log"
    VPC_PEERING_CONNECTION = "vpc-peering-connection"
    VPN_CONNECTION = "vpn-connection"
    VPN_GATEWAY = "vpn-gateway"


class VpcEndpointType(str, Enum):
    """
    The type of endpoint.
     Default: Gateway
    """
    INTERFACE = "Interface"
    GATEWAY = "Gateway"
    GATEWAY_LOAD_BALANCER = "GatewayLoadBalancer"


class VpnConnectionCloudwatchLogOptionsSpecificationLogOutputFormat(str, Enum):
    """
    Set log format. Default format is ``json``.
     Valid values: ``json`` | ``text``
    """
    JSON = "json"
    TEXT = "text"


class VpnConnectionIkeVersionsRequestListValueValue(str, Enum):
    """
    The IKE version.
    """
    IKEV1 = "ikev1"
    IKEV2 = "ikev2"


class VpnConnectionPhase1EncryptionAlgorithmsRequestListValueValue(str, Enum):
    """
    The value for the encryption algorithm.
    """
    AES128 = "AES128"
    AES256 = "AES256"
    AES128_GCM16 = "AES128-GCM-16"
    AES256_GCM16 = "AES256-GCM-16"


class VpnConnectionPhase1IntegrityAlgorithmsRequestListValueValue(str, Enum):
    """
    The value for the integrity algorithm.
    """
    SHA1 = "SHA1"
    SHA2256 = "SHA2-256"
    SHA2384 = "SHA2-384"
    SHA2512 = "SHA2-512"


class VpnConnectionPhase2EncryptionAlgorithmsRequestListValueValue(str, Enum):
    """
    The encryption algorithm.
    """
    AES128 = "AES128"
    AES256 = "AES256"
    AES128_GCM16 = "AES128-GCM-16"
    AES256_GCM16 = "AES256-GCM-16"


class VpnConnectionPhase2IntegrityAlgorithmsRequestListValueValue(str, Enum):
    """
    The integrity algorithm.
    """
    SHA1 = "SHA1"
    SHA2256 = "SHA2-256"
    SHA2384 = "SHA2-384"
    SHA2512 = "SHA2-512"


class VpnConnectionVpnTunnelOptionsSpecificationDpdTimeoutAction(str, Enum):
    """
    The action to take after DPD timeout occurs. Specify ``restart`` to restart the IKE initiation. Specify ``clear`` to end the IKE session.
     Valid Values: ``clear`` | ``none`` | ``restart`` 
     Default: ``clear``
    """
    CLEAR = "clear"
    NONE = "none"
    RESTART = "restart"


class VpnConnectionVpnTunnelOptionsSpecificationStartupAction(str, Enum):
    """
    The action to take when the establishing the tunnel for the VPN connection. By default, your customer gateway device must initiate the IKE negotiation and bring up the tunnel. Specify ``start`` for AWS to initiate the IKE negotiation.
     Valid Values: ``add`` | ``start`` 
     Default: ``add``
    """
    ADD = "add"
    START = "start"
