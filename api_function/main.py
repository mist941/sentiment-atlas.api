import json
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv('REGION_NAME')
table_name = os.getenv('TABLE_NAME')

dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)


def handler(event, context):
    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    if path == "/" and method == "GET":
        try:
            response = table.scan()
            data = response.get('Items', [])
            print(data)
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"data": data})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": str(e)})
            }

    else:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Not Found"})
        }
