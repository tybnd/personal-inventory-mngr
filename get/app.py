import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('personal-inventory')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Safely access query string parameter 'ID'
        item_id = event.get('queryStringParameters', {}).get('ID')
        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "ID parameter is required"}),
                "headers": {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
                }
            }
        
        # Example: Retrieve item from DynamoDB (GET functionality)
        response = table.get_item(Key={'ID': item_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item not found"}),
                "headers": {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
                }
            }

        item = response['Item']

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully retrieved item",
                "item": item
            }, cls=DecimalEncoder),
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
            "body": json.dumps({"message": "Internal Server Error"}),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
            }
        }
    except Exception as e:
        print(f"Exception: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"}),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
            }
        }
