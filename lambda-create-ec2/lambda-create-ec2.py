'''
    Create EC2 instance within Lambda Function

    Be carefull of the INSTANCE_TYPE and the SUBNET_ID , not all of them are supported
'''


import os
import boto3
import json

AMI = os.environ['AMI']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
KEY_NAME = os.environ['KEY_NAME']
SUBNET_ID = os.environ['SUBNET_ID']

ec2 = boto3.resource('ec2')


def lambda_handler(event, context):
    instance = ec2.create_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SubnetId=SUBNET_ID,
        MaxCount=1,
        MinCount=1
    )

    return {
        'statusCode': 200,
        'body': json.dumps('EC2 Instance Created!')
    }