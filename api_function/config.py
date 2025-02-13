import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv("REGION_NAME", "us-east-1")
table_name = os.getenv("TABLE_NAME", "sentiment_data")

config = {
    "aws": {
        "region_name": region_name,
        "table_name": table_name
    },
    "cors": {
        "allowed_origin": "https://sentiment-atlas.vercel.app",
        "allowed_methods": "OPTIONS, GET",
        "allowed_headers": "Content-Type"
    }
}
