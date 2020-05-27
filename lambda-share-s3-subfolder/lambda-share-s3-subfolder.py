import boto3
import json
import os

'''
    Create an S3 Bucket with a subfolder and add the bucket policy (read OR write) to that subfolder
    The bucket has these properties: 
        - Versioning enabled
        - Encryption AES256
        - Block all public access
'''

client_stormdev = boto3.client('s3')
resource_stormdev = boto3.resource('s3')

ACCOUNT_ID = os.environ['ACCOUNT_ID']
# ACCOUNT_ID = "xxxxxxxxxxxx"

ACCOUNT_USERNAME = os.environ['ACCOUNT_USERNAME']
# ACCOUNT_USERNAME = "xxxxxxxxxxx"

BUCKET_NAME = os.environ['BUCKET_NAME']
# BUCKET_NAME = "boto3-xxxxx-xxxxx"

BUCKET_REGION = os.environ['BUCKET_BUCKET_REGION']
# BUCKET_REGION = "eu-west-1"

BUCKET_SUBFOLDER = os.environ['BUCKET_BUCKET_SUBFOLDER']
# BUCKET_SUBFOLDER = "test-BUCKET_SUBFOLDER"

BUCKET_POLICY_TYPE = os.environ['BUCKET_POLICY_TYPE']  # read OR write
# BUCKET_POLICY_TYPE = "read"


def shareS3BUCKET_SUBFOLDER():
    print("Creating S3 Bucket with Subfolder")
    createBucket(BUCKET_NAME, BUCKET_REGION, BUCKET_SUBFOLDER)

    print("Creating S3 Bucket policy")
    createBucketPolicy(BUCKET_POLICY_TYPE, ACCOUNT_ID, ACCOUNT_USERNAME, BUCKET_NAME, BUCKET_SUBFOLDER)


def createBucket(BUCKET_NAME, BUCKET_REGION, BUCKET_SUBFOLDER):
    client_stormdev.create_bucket(
        ACL='private',
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': BUCKET_REGION
        })

    client_stormdev.put_object(
        Bucket=BUCKET_NAME,
        Key=(BUCKET_SUBFOLDER + '/')
    )

    bucket_versioning = resource_stormdev.BucketVersioning(BUCKET_NAME)
    bucket_versioning.enable()

    client_stormdev.put_bucket_encryption(
        Bucket=BUCKET_NAME,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}
                }
            ]
        }
    )

    client_stormdev.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'BlockPublicPolicy': True,
            'IgnorePublicAcls': True,
            'RestrictPublicBuckets': True
        }
    )


def createBucketPolicy(BUCKET_POLICY_TYPE, ACCOUNT_ID, ACCOUNT_USERNAME, BUCKET_NAME, BUCKET_SUBFOLDER):
    if BUCKET_POLICY_TYPE == 'read':
        read = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Principal": {
                        "AWS": "arn:aws:iam::" + ACCOUNT_ID + ":user/" + ACCOUNT_USERNAME
                    },
                    "Resource": "arn:aws:s3:::" + BUCKET_NAME + "/" + BUCKET_SUBFOLDER + "/*"
                }
            ]
        }

        read = json.dumps(read)

        client_stormdev.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=read
        )

        return {
            'statusCode': 200,
            'body': json.dumps('S3 Bucket with shared subfolder created!')
        }

    elif BUCKET_POLICY_TYPE == 'write':
        write = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3.PutObject"
                    ],
                    "Principal": {
                        "AWS": "arn:aws:iam::" + ACCOUNT_ID + ":user/" + ACCOUNT_USERNAME
                    },
                    "Resource": "arn:aws:s3:::" + BUCKET_NAME + "/" + BUCKET_SUBFOLDER + "/*"
                }
            ]
        }

        write = json.dumps(write)

        client_stormdev.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=write
        )

        return {
            'statusCode': 200,
            'body': json.dumps('S3 Bucket with shared subfolder created!')
        }


shareS3BUCKET_SUBFOLDER()
