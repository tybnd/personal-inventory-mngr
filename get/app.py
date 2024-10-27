import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('personal-inventory')

def lambda_handler(event, context):
    try:
        # Safely access query string parameter 'ID'
        item_id = event.get('queryStringParameters', {}).get('ID')
        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "ID parameter is required"})
            }
        
        # Further processing here (e.g., DynamoDB queries)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully retrieved item",
                "ID": item_id,
                # Add more response data as needed
            })
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }
