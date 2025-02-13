import json
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv('REGION_NAME')
table_name = os.getenv('TABLE_NAME')

dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://sentiment-atlas.vercel.app",
    "Access-Control-Allow-Methods": "OPTIONS, GET",
    "Access-Control-Allow-Headers": "Content-Type"
}


def handler(event, context):
    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    # Обробка preflight-запиту (CORS OPTIONS)
    if method == "OPTIONS":
        return {
            "statusCode": 204,  # No Content
            "headers": CORS_HEADERS,
            "body": ""
        }

    if path == "/" and method == "GET":
        try:
            response = table.scan()
            data = response.get('Items', [])
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": json.dumps(data, default=str)
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": str(e)})
            }

    else:
        return {
            "statusCode": 404,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Not Found"})
        }
