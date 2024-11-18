import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('personal-inventory')

def lambda_handler(event, context):
    try:
        # Log the received event for debugging
        print(f"Received event: {json.dumps(event)}")

        # Extract details from the event
        event_source = event.get('source')
        event_detail_type = event.get('detail-type')
        event_name = event.get('detail', {}).get('eventName')
        
        # Log the extracted details
        print(f"Event Source: {event_source}, Event Name: {event_name}, Detail Type: {event_detail_type}")

        # Store the event in DynamoDB
        response = table.put_item(
            Item={
                'ResourceID': event_name,
                'EventSource': event_source,
                'EventDetailType': event_detail_type,
                'EventDetails': json.dumps(event.get('detail')),
            }
        )

        # Log DynamoDB response
        print(f"DynamoDB Response: {response}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event processed successfully"}),
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
