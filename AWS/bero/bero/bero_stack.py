

from aws_cdk import (
    # Duration,
    Size,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class BeroStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "BeroQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        vpc = ec2.Vpc(
            self, 'MyVpc',
            cidr="10.13.0.0/21",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="bero_public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC),
            
        
                ec2.SubnetConfiguration(name="bero_private", cidr_mask=23, subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
            ]    

        )
    
        #  Security group rules
        # my_security_group_without_inline_rules = ec2.SecurityGroup(self, "SecurityGroup",
        #     vpc=vpc,
        #     description="Allow ssh access to ec2 instances",
        #     allow_all_outbound=True,
        #     disable_inline_rules=True
        #     )
        

        # # Security group rules 2

        # #create a new security group
        # sec_group = ec2.SecurityGroup(
        #     self,
        #     "sec-group-allow-ssh",
        #     vpc=vpc,
        #     allow_all_outbound=True,
        #     )

        # # add a new ingress rule to allow port 22 to internal hosts
        # sec_group.add_ingress_rule(
        #     peer=ec2.Peer.ipv4('10.0.0.0/16'),
        #     description="Allow SSH connection", 
        #     connection=ec2.Port.tcp(22)
        #     )

        # # Instance Role and SSM Managed Policy
        # role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        # role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")) 


        # AMI
        # amzn_linux = ec2.MachineImage.latest_amazon_linux(
        #     generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
        #     edition=ec2.AmazonLinuxEdition.STANDARD,
        #     virtualization=ec2.AmazonLinuxVirt.HVM,
        #     storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        #     )
   

        # ubuntu = ec2.MachineImage.from_ssm_parameter('/aws/service/canonical/ubuntu/server/focal/stable/current/amd64/hvm/ebs-gp2/ami-id')
           
        # ubuntu= ec2.MachineImage.generic_linux({
        #     'us-east-1' : "ami-0059b7cd9f67d8050"
        # })
       
      
       
        # Instance1
        # instance = ec2.Instance(self, "Instance",
        #     instance_type=ec2.InstanceType("t3.nano"),
        #     machine_image=ubuntu,
        #     block_devices=[
        #         ec2.BlockDevice(device_name="/dev/sda1", volume=ec2.BlockDeviceVolume.ebs(50)), 
        #         ec2.BlockDevice(device_name="/dev/sdm", volume=ec2.BlockDeviceVolume.ebs(100))
        #     ],
        #     vpc = vpc,
        #     role = role,
        #     security_group=my_security_group_without_inline_rules
        #     )

         # Instance 2
        # instance = ec2.Instance(self, "Instance2",
        #      instance_type=ec2.InstanceType("t3.nano"),
        #      machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
        #      block_devices=[ec2.BlockDevice(device_name="/dev/sdm", volume=ec2.BlockDeviceVolume.ebs(500))],
             
        #      vpc=vpc,
        #      role=role,
        #      key_name=
        # )

       
