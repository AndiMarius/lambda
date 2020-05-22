'''
    Create IAM Role within Lambda Function

  
'''

import json
import boto3
import os

ROLE = json.loads(os.environ['ROLE'])
NAME = os.environ['NAME']

iam = boto3.client('iam')
assume_role_policy_document = json.dumps(ROLE)


def create_iam_role(event, context):
    
    role = iam.create_role(
        RoleName= NAME,
        AssumeRolePolicyDocument=assume_role_policy_document
    )

    return {
        'statusCode': 200,
        'body': json.dumps('IAM Role Created!')
    }
