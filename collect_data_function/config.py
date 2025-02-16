import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


def get_secrets():
    if os.getenv("TEST_ENV"):
        return {
            "client_id": "fake_client_id",
            "client_secret": "fake_client_secret",
            "user_agent": "fake_user_agent",
            "username": "fake_username",
            "password": "fake_password"
        }

    try:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager",
                                region_name="us-east-1")
        secret_value = json.loads(
            client.get_secret_value(
                SecretId="sentiment_atlas")["SecretString"])
        return secret_value
    except (NoCredentialsError, ClientError):
        raise Exception("AWS credentials not found or error fetching secrets")


secret_value = get_secrets()

config = {
    "reddit": {
        "client_id": secret_value["client_id"],
        "client_secret": secret_value["client_secret"],
        "user_agent": secret_value["user_agent"],
        "username": secret_value["username"],
        "password": secret_value["password"],
    },
    "aws": {
        "region_name": "us-east-1",
        "table_name": "SentimentData"
    }
}
