


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

      
        vpc = ec2.Vpc(
            self, 'MyVpc', vpc_name="VPC2",
            cidr="10.13.0.0/21",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="bero_public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC),
            
        
                ec2.SubnetConfiguration(name="bero_private", cidr_mask=23, subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
            ]    

        )
    
       
        sec_group1 = ec2.SecurityGroup(self, "iac_sg1", security_group_name="sec1", 
            vpc=vpc,
            allow_all_outbound=True,
            )
        

        sec_group1.add_ingress_rule(
            peer=ec2.Peer.ipv4('0.0.0.0/0'), 
            description="Allow SSH connection", 
            connection=ec2.Port.tcp(22)
            )


     
        sec_group2 = ec2.SecurityGroup(self, "iac_sg2", security_group_name="sec2",
            vpc=vpc,
            allow_all_outbound=True,
            )

        sec_group2.add_ingress_rule(
            peer=ec2.Peer.ipv4('0.0.0.0/0'),
            description="Allow SSH connection", 
            connection=ec2.Port.tcp(22)
            )

       
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")) 


     
        ub_image = ec2.MachineImage.from_ssm_parameter('/aws/service/canonical/ubuntu/server/focal/stable/current/amd64/hvm/ebs-gp2/ami-id')

   
        instance = ec2.Instance(self, "IaCInstance1",
            instance_type=ec2.InstanceType("t2.large"),
            machine_image=ub_image,
            block_devices=[
                ec2.BlockDevice(device_name="/dev/sda1", volume=ec2.BlockDeviceVolume.ebs(50))
            ],
            vpc = vpc,            
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
             ),
            role=role,
            security_group=sec_group1,
            key_name = "iacvpc"
            )
      
        instance = ec2.Instance(self, "IaCInstance2",
            instance_type=ec2.InstanceType("t2.large"),
            machine_image=ub_image,
            block_devices=[
                ec2.BlockDevice(device_name="/dev/sda1", volume=ec2.BlockDeviceVolume.ebs(50))                
            ],
            vpc = vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
             ),
            role=role,
            security_group=sec_group2,
            key_name = "iacvpc"
        )



       
