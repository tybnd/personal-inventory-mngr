import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('personal-inventory')

def lambda_handler(event, context):
    # Parse input JSON
    try:
        body = json.loads(event['body'])
        item_id = body['ID']
        quantity = body['Quantity']
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "ID and Quantity are required"})
        }
    
    try:
        # Add or update item in DynamoDB
        table.put_item(
            Item={
                'ID': item_id,
                'Quantity': quantity
            }
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item updated successfully"})
        }

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
