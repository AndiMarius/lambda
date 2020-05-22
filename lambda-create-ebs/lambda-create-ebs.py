'''
    Create EBS Volume within Lambda Function

  
'''


import os
import boto3
import json

ec2 = boto3.client('ec2')

SIZE = os.environ['SIZE']
AVAILBILITY_ZONE = os.environ['AVAILBILITY_ZONE']
KEY_TAG = os.environ['KEY_TAG']
VALUE_TAG = os.environ['VALUE_TAG']


def create_ebs(event,context):
    ebs = ec2.create_volume(
        Size=int(SIZE),
        AvailabilityZone=AVAILBILITY_ZONE
    )

    ebs_id = ebs['VolumeId']

    ec2.create_tags(
        Resources=[ebs_id],
        Tags=[{"Key": KEY_TAG, "Value": VALUE_TAG}]
    )
    print('This is the volume id: ', ebs_id)

    return {
        'statusCode': 200,
        'body': json.dumps('EBS Volume Created!')
    }