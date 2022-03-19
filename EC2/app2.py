# Infrastructure as code using AWS CDK in Python

import os.path

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack)

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
            igw_id = vpc.internet_gateway_id,
            subnet_configuration=[ec2.SubnetConfiguration(          
                cidr_mask=24,
                name="PUB",
                subnet_type=ec2.SubnetType.PUBLIC,
                availability_zones=["us-east-1a"],
                ), ec2.SubnetConfiguration(
                cidr_mask=23,
                name="PRIV",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
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

        my_security_group_without_inline_rules.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")

    # Security group rules 2

    #create a new security group
        sec_group = ec2.SecurityGroup(
            self,
            "sec-group-allow-ssh",
            vpc=vpc,
            allow_all_outbound=True,
            )

# add a new ingress rule to allow port 22 to internal hosts
        sec_group.add_ingress_rule(
            peer=ec2.Peer.ipv4('10.0.0.0/16'),
            description="Allow SSH connection", 
            connection=ec2.Port.tcp(22)
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

    # Instance1
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=amzn_linux,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(50)
                ), ec2.BlockDevice(
                device_name="/dev/sdm",
                volume=ec2.BlockDeviceVolume.ebs(100)
                )
                ],
            vpc = vpc,
            role = role,
            security_group=my_security_group_without_inline_rules
            )

    # Instance 2
        instance = ec2.Instance(self, "Instance2",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ec2.AmazonLinuxImage(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),

        volume = ec2.Volume(self, "Volume",
        availability_zone="us-west-2a",
        size=Size.gibibytes(500),
        encrypted=True
        )
        volume.grant_attach_volume(role, [instance]),   

    # NAT gateway traffic
        provider = ec2.NatProvider.instance(
            instance_type=instance_type,
            allow_all_traffic=False 
            ),
        ec2.Vpc(self, "TheVPC",
         nat_gateway_provider=provider
            ),
        provider.connections.allow_from(ec2.Peer.ipv4("1.2.3.4/8"), ec2.Port.tcp(80))
        vpc = vpc,
        role = role,
        security_group=sec_group,
        )


app = App()
EC2InstanceStack(app, "ec2-instance")

app.synth()