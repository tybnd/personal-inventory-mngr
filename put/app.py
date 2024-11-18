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
        # Fetch existing resources from DynamoDB
        existing_items = get_existing_resources()

        # Log existing resources
        print(f"Existing Resources in DynamoDB: {existing_items}")

        # Fetch current resources (this could be from an external service or input data)
        new_resources = get_current_resources()

        # Log new resources
        print(f"New Resources Detected: {new_resources}")

        # Compare existing and new resources
        updated_resources = compare_and_update_resources(existing_items, new_resources)

        # Log updated resources
        print(f"Updated Resources: {updated_resources}")

        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Table updated successfully", "updated_resources": updated_resources}),
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

# Helper function to get existing resources from DynamoDB
def get_existing_resources():
    response = table.scan()  # Scan to get all resources
    return response.get('Items', [])

# Helper function to get current resources (e.g., from a list, an external API, etc.)
def get_current_resources():
    # For example, we're using a hardcoded list of new resources.
    # In a real case, you could fetch this from another source (S3, API, etc.)
    return [
        {"ResourceID": "hammer", "Quantity": 10},
        {"ResourceID": "wrench", "Quantity": 20},
        # Add more resources as needed
    ]

# Helper function to compare existing and new resources, and return updated resources
def compare_and_update_resources(existing_items, new_resources):
    updated_resources = []

    # Convert existing items into a dictionary for easy lookups
    existing_dict = {item['ResourceID']: item for item in existing_items}

    # Check for new or updated resources
    for resource in new_resources:
        item_id = resource['ResourceID']
        if item_id not in existing_dict:
            # Add new resource to the table
            table.put_item(Item=resource)
            updated_resources.append({"ResourceID": item_id, "Status": "Added"})
        elif existing_dict[item_id]['Quantity'] != resource['Quantity']:
            # Update existing resource in the table
            table.update_item(
                Key={'ResourceID': item_id},
                UpdateExpression="SET Quantity = :q",
                ExpressionAttributeValues={':q': decimal.Decimal(resource['Quantity'])},
                ReturnValues="UPDATED_NEW"
            )
            updated_resources.append({"ResourceID": item_id, "Status": "Updated"})

    # Check for removed resources
    for item in existing_items:
        item_id = item['ResourceID']
        if item_id not in [resource['ResourceID'] for resource in new_resources]:
            # Remove resource from the table (if it doesn't exist in new resources)
            table.delete_item(Key={'ResourceID': item_id})
            updated_resources.append({"ResourceID": item_id, "Status": "Removed"})

    return updated_resources
