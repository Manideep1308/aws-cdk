		
import os.path		
from aws_cdk.aws_s3_assets import Asset		
from aws_cdk import (		
    aws_ec2 as ec2,		
    aws_iam as iam,		
    App, Stack		
)		
from constructs import Construct		
dirname = os.path.dirname(__file__)		
class EC2InstanceStack(Stack):		
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:		
        super().__init__(scope, id, **kwargs)		
		
# VPC		
vpc = ec2.Vpc(self, "TheVPC",		
    cidr="10.0.0.0/16",		
    max_azs=1,		
    nat_gateways=1,		
    igw_id = vpc.internet_gateway_id		
		
    subnet_configuration=[ec2.SubnetConfiguration(          		
        cidr_mask=24		
        name="PUB",		
        subnet_type=ec2.SubnetType.PUBLIC,		
        availability_zones=["us-east-1a"]		
    ), ec2.SubnetConfiguration(		
        cidr_mask=23,		
        name="PRIV",		
        subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT		
        availability_zones=["us-east-1a"]		
    )		
    ]		
)		
		
#  Security group rules		
my_security_group_without_inline_rules = ec2.SecurityGroup(self, "SecurityGroup",		
    vpc=vpc,		
    description="Allow ssh access to ec2 instances",		
    allow_all_outbound=True,		
    disable_inline_rules=True		
)		
		
# Instance Role and SSM Managed Policy		
role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))		
role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))		
		
# AMI		
amzn_linux = ec2.MachineImage.latest_amazon_linux(		
generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,		
edition=ec2.AmazonLinuxEdition.STANDARD,		
virtualization=ec2.AmazonLinuxVirt.HVM,		
storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE		
)		
		
# Instance		
instance = ec2.Instance(self, "Instance",		
instance_type=ec2.InstanceType("t3.nano"),		
machine_image=amzn_linux,		
vpc = vpc,		
role = role		
)		
		
app = App()		
EC2InstanceStack(app, "ec2-instance")		
		
app.synth()		
		