import boto3
import sure 
import pytest
from app import EC2InstanceStack
from moto import mock_ec2
from botocore.exceptions import ClientError


@mock_ec2
def test_create_and_delete_vpc():
    ec2 = boto3.resource("ec2", region_name="us-east-1a")
    client = boto3.client("ec2", region_name="us-east-1a")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc.cidr_block.should.equal("10.0.0.0/16")

 

    with pytest.raises(ClientError) as ex:
        client.delete_vpc(VpcId="vpc-1234abcd")
    ex.value.response["ResponseMetadata"]["HTTPStatusCode"].should.equal(400)
    ex.value.response["ResponseMetadata"].should.have.key("RequestId")
    ex.value.response["Error"]["Code"].should.equal("InvalidVpcID.NotFound")



@mock_ec2
def test_boto3_describe_regions():
    ec2 = boto3.client("ec2", "us-east-1a")
    resp = ec2.describe_regions()
    len(resp["Regions"]).should.be.greater_than(1)
    for rec in resp["Regions"]:
        rec["Endpoint"].should.contain(rec["RegionName"])

    test_region = "us-east-1"
    resp = ec2.describe_regions(RegionNames=[test_region])
    resp["Regions"].should.have.length_of(1)
    resp["Regions"][0].should.have.key("RegionName").which.should.equal(test_region)
    resp["Regions"][0].should.have.key("OptInStatus").which.should.equal(
        "opt-in-not-required"
    )   
@mock_ec2   
def test_subnets_boto3():
    ec2 = boto3.resource("ec2", region_name="us-east-1a")
    client = boto3.client("ec2", region_name="us-east-1a")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    subnet = ec2.create_subnet(VpcId=vpc.id, CidrBlock="10.0.0.0/24")

    ours = client.describe_subnets(SubnetIds=[subnet.id])["Subnets"]
    ours.should.have.length_of(1)

    client.delete_subnet(SubnetId=subnet.id)

    with pytest.raises(ClientError) as ex:
        client.describe_subnets(SubnetIds=[subnet.id])
    err = ex.value.response["Error"]
    err["Code"].should.equal("InvalidSubnetID.NotFound")

    with pytest.raises(ClientError) as ex:
        client.delete_subnet(SubnetId=subnet.id)
    ex.value.response["ResponseMetadata"]["HTTPStatusCode"].should.equal(400)
    ex.value.response["ResponseMetadata"].should.have.key("RequestId")
    ex.value.response["Error"]["Code"].should.equal("InvalidSubnetID.NotFound")