import praw
import json
import boto3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

secret_name = "sentiment_atlas"
region_name = "us-east-1"
session = boto3.session.Session()
client = session.client(service_name='secretsmanager', region_name=region_name)
secret_value = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])

reddit = praw.Reddit(
    client_id=secret_value['client_id'],
    client_secret=secret_value['client_secret'],
    user_agent=secret_value['user_agent'],
    username=secret_value['username'],
    password=secret_value['password']
)

analyzer = SentimentIntensityAnalyzer()

with open('countries.json', 'r') as file:
    countries = json.load(file)

dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table('SentimentData')

def collect_analyze_and_save_sentiment(country):
    try:
        query = country['country_name']
        subreddit = reddit.subreddit('all')
        posts = subreddit.search(query, limit=100)
        
        sentiments = []
        for post in posts:
            content = post.title + ' ' + post.selftext
            sentimentCompound = analyzer.polarity_scores(content)['compound']
            sentiments.append(sentimentCompound)
            
        if len(sentiments) == 0:
            average_sentiment = 0
        else:   
            average_sentiment = sum(sentiments) / len(sentiments)
        average_sentiment_decimal = Decimal(str(average_sentiment)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        
        table.put_item(
            Item={
                'country': country['country_id'],
                'country_name': country['country_name'],
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'average_sentiment': average_sentiment_decimal
            }
        )

    except Exception as e:
        print(f"Error processing {country}: {e}")

def handler(event, context):
    for country in countries:
        collect_analyze_and_save_sentiment(country)
