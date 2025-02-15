import json
import boto3

session = boto3.session.Session()
client = session.client(service_name='secretsmanager', region_name='us-east-1')
secret_value = json.loads(
    client.get_secret_value(SecretId='sentiment_atlas')['SecretString'])

config = {
    "reddit": {
        "client_id": secret_value["client_id"],
        "client_secret": secret_value["client_secret"],
        "user_agent": secret_value["user_agent"],
        "username": secret_value["username"],
        "password": secret_value["password"],
    },
    "aws": {
        "region_name": 'us-east-1',
        "table_name": 'SentimentData'
    }
}
