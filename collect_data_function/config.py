import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

secret_name = os.getenv('SECRET_NAME')
region_name = os.getenv('REGION_NAME')
table_name = os.getenv('TABLE_NAME')

session = boto3.session.Session()
client = session.client(service_name='secretsmanager', region_name=region_name)
secret_value = json.loads(
    client.get_secret_value(SecretId=secret_name)['SecretString'])

config = {
    "reddit": {
        "client_id": secret_value["client_id"],
        "client_secret": secret_value["client_secret"],
        "user_agent": secret_value["user_agent"],
        "username": secret_value["username"],
        "password": secret_value["password"],
    },
    "aws": {
        "region_name": region_name,
        "table_name": table_name
    }
}
