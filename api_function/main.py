import json
import boto3
from .config import config

dynamodb = boto3.resource("dynamodb", region_name=config["aws"]["region_name"])
table = dynamodb.Table(config["aws"]["table_name"])


def create_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": config["cors"],
        "body": json.dumps(body, default=str)
    }


def handler(event, context):
    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    if method == "OPTIONS":
        return create_response(204, "")

    if path == "/" and method == "GET":
        try:
            response = table.scan()
            data = response.get('Items', [])
            return create_response(200, data)
        except Exception as e:
            return create_response(500, {"error": str(e)})

    else:
        create_response(404, {"error": "Not Found"})
