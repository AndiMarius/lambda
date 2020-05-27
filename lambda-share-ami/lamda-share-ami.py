import boto3
import os
import json

'''
Share AMI cross account:
 -   If AMI owner wants to share the ami with an user on the same region
    
 -   If AMI owner wants to share the ami with an user on another region
        In this case the owner need to have the AMI on both regions
'''


USER_ID = os.environ['USER_ID']
AMI_ID = os.environ['AMI_ID']

SOURCE_REGION = os.getenv("SOURCE_REGION", '') #AMI'S REGION IF YOU NEED TO SHARE CROSS REGION
TARGET_REGION = os.getenv("TARGET_REGION", '') #NEW AMI'S REGION IF YOU NEED TO SHARE CROSS REGION






def share_ami(event,context):

    if TARGET_REGION == '':
        #RESOURCES
        ec2_client = boto3.client('ec2')
        ec2_resource = boto3.resource('ec2')

        print('No region selected, I will share the AMI on the same region where is located')

        print("Share AMI with the user")
        ec2_client.modify_image_attribute(ImageId=AMI_ID, OperationType='add',
                                        Attribute='launchPermission',
                                        UserIds=[USER_ID])
        return {
            'statusCode': 200,
            'body': json.dumps('AMI Shared')
        }


    else:
        #RESOURCES WITH DESIRED REGION
        ec2_client = boto3.client('ec2', region_name=TARGET_REGION)
        ec2_resource = boto3.resource('ec2', region_name=TARGET_REGION)

        print('A different region is selected. I will copy the AMI on the desired region and then share it with the user')
        tmp_Image_Id = ec2_client.copy_image(Description='',
                                            Name='Copied AMI',
                                            SourceImageId=AMI_ID,
                                            SourceRegion=SOURCE_REGION)

        tmp_Image = ec2_resource.Image(tmp_Image_Id['ImageId'])

        if tmp_Image.state == 'pending':
            print("Waiting for image to be available.")
            while tmp_Image.state != 'available':
                tmp_Image = ec2_resource.Image(tmp_Image_Id['ImageId'])
            print("Image Available to use")
            
            print("Share AMI with the user")
            ec2_client.modify_image_attribute(ImageId=tmp_Image_Id['ImageId'], OperationType='add',
                                            Attribute='launchPermission',
                                            UserIds=[USER_ID])
            return {
                'statusCode': 200,
                'body': json.dumps('AMI Shared')
            }