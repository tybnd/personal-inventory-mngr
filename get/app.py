import json
import requests


def lambda_handler(event, context):

    try:
        url = requests.get("api_url_here")
    except requests.RequestException as e:
            #Send some context about this error to Lambda Logs
        print(e)

        raise e
    nameid = ''
    numid= ' '  
    return {
            "statusCode": 200,
            "body": json.dumps({
                "message": nameid, "Count": numid
                # "location": ip.text.replace("\n", "")
            }),
        }
