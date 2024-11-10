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
    try:
        # Use the body directly if it's already a dictionary
        body = event.get('body', {})
        item_id = body.get('ID')
        quantity = body.get('Quantity')

        # Log input to confirm data is being passed correctly
        print(f"Received item ID: {item_id}, Quantity: {quantity}")

        if not item_id or quantity is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "ID and Quantity are required"}),
                "headers": {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
                }
            }

        # Log before DynamoDB update
        print("Attempting to update DynamoDB item...")

        # Update the Quantity using update_item
        response = table.update_item(
            Key={'ID': item_id},
            UpdateExpression="SET Quantity = :q",
            ExpressionAttributeValues={':q': decimal.Decimal(quantity)},
            ReturnValues="UPDATED_NEW"
        )

        # Log response from DynamoDB
        print(f"DynamoDB Response: {response}")

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
