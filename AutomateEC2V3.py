import boto3
import configparser

# Read the config and credentials files
config = configparser.ConfigParser()
config.read(['config.ini', 'credentials.ini'])

# Set up the session using the config and credentials
session = boto3.Session(
    aws_access_key_id=config['default']['aws_access_key_id'],
    aws_secret_access_key=config['default']['aws_secret_access_key'],
    region_name=config['default']['region']
)

# Connect to EC2
ec2 = session.client('ec2')

# Security group and key pair
security_group_id = config['default']['security_group_id']
key_pair_name = config['default']['key_pair_name']

# Counter variable to keep track of the number of instances
counter = 1

# Create an EC2 instance
response = ec2.run_instances(
    ImageId='ami-0ff8a91507f77f867', # Amazon Linux 2 LTS
    InstanceType='t2.micro',
    KeyName=key_pair_name,
    SecurityGroupIds=[security_group_id],
    SubnetId=config['default']['subnet_id'],
    MinCount=1,
    MaxCount=1,
    InstanceInitiatedShutdownBehavior='terminate',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Auto_Instance_' + str(counter)
                },
            ]
        },
    ]
)

# Print the instance ID
print(response)

# Increment the counter variable
counter += 1
