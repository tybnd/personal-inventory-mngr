import boto3
import json

def lambda_handler(event, context):
    resources = []

    # Fetch EC2 instances
    ec2_client = boto3.client('ec2')
    ec2_response = ec2_client.describe_instances()
    for reservation in ec2_response['Reservations']:
        for instance in reservation['Instances']:
            resources.append({
                "Type": "EC2 Instance",
                "State": instance['State']['Name']
            })
    vpc_response = ec2_client.describe_vpcs()
    for vpc in vpc_response['Vpcs']:
        resources.append({
            "Type": "VPC",
            "State": vpc.get('State', 'Unknown'),

        })
    # Fetch S3 buckets
    s3_client = boto3.client('s3')
    s3_response = s3_client.list_buckets()
    for bucket in s3_response['Buckets']:
        resources.append({
            "Type": "S3 Bucket",
            "State": "Available"
        })

    # Fetch DynamoDB tables
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_response = dynamodb_client.list_tables()
    for table in dynamodb_response['TableNames']:
        resources.append({
            "Type": "DynamoDB Table",
            "State": "Active"
        })

    # Fetch RDS instances
    rds_client = boto3.client('rds')
    rds_response = rds_client.describe_db_instances()
    for db_instance in rds_response['DBInstances']:
        resources.append({

            "Type": "RDS Instance",
            "State": db_instance['DBInstanceStatus']
        })

    # Fetch CloudFront distributions
    cloudfront_client = boto3.client('cloudfront')
    cloudfront_response = cloudfront_client.list_distributions()
    for distribution in cloudfront_response.get('DistributionList', {}).get('Items', []):
        resources.append({
            "Type": "CloudFront Distribution",
            "State": distribution['Status']
        })

    # Fetch Lambda functions
    lambda_client = boto3.client('lambda')
    lambda_response = lambda_client.list_functions()
    for function in lambda_response['Functions']:
        resources.append({
            "Type": "Lambda Function",
            "State": "Available"
        })
    
    # Fetch Load Balancers
    elb_client = boto3.client('elbv2')
    elb_response = elb_client.describe_load_balancers()
    for lb in elb_response['LoadBalancers']:
        resources.append({
            "Type": "Load Balancer",
            "State": lb['State']['Code']
        })

    return {
        'statusCode': 200,
        'body': json.dumps(resources)
    }
