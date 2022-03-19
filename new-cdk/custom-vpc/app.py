
from http import client
import boto3
from moto import mock_s3
@mock_s3 
class s3():

 client=boto3.client("s3")
 client.create_bucket(Bucket="db")