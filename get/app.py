import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('personal-inventory')

def lambda_handler(event, context):
    print("Received event: ", json.dumps(event))  # Log the entire event

    # Check if 'queryStringParameters' exists
    query_params = event.get('queryStringParameters', {})
    item_id = query_params.get('ID')  # Get ID from query string

    if item_id is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "ID parameter is required"})
        }

    try:
        response = table.get_item(Key={'ID': item_id})
        item = response.get('Item')

        if item:
            return {
                "statusCode": 200,
                "body": json.dumps(item)
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item not found"})
            }

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }
