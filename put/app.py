import json
import boto3
from botocore.exceptions import ClientError
import decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('personal-inventory')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)  # Convert DynamoDB Decimal to float for JSON
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    # Parse input JSON
    try:
        body = json.loads(event['body'])
        item_id = body['ID']
        quantity = body['Quantity']
    except (KeyError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "ID and Quantity are required"}),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
            }
        }
    
    try:
        # Add or update item in DynamoDB
        table.put_item(
            Item={
                'ID': item_id,
                'Quantity': decimal.Decimal(quantity)  # Store as Decimal
            }
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item updated successfully"}),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
            }
        }

    except ClientError as e:
        print(f"ClientError: {e.response['Error']['Message']}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
            }
        }
