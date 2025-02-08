import json


def lambda_handler(event):
    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    if path == "/" and method == "GET":
        return {
            "statusCode":
            200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body":
            json.dumps({"message": "Hello from AWS Lambda with pure Python!"})
        }
    else:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Not Found"})
        }
