import os
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv("REGION_NAME")
table_name = os.getenv("TABLE_NAME")

config = {
    "aws": {
        "region_name": region_name,
        "table_name": table_name
    },
    "cors": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "https://sentiment-atlas.vercel.app",
        "Access-Control-Allow-Methods": "OPTIONS, GET",
        "Access-Control-Allow-Headers": "Content-Type"
    }
}
