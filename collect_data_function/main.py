from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from .config import config
import concurrent
import praw
import boto3
import json


def get_reddit_client():
    return praw.Reddit(client_id=config["reddit"]["client_id"],
                       client_secret=config["reddit"]["client_secret"],
                       user_agent=config["reddit"]["user_agent"],
                       username=config["reddit"]["username"],
                       password=config["reddit"]["password"])


def get_dynamodb_table():
    dynamodb = boto3.resource("dynamodb",
                              region_name=config["aws"]["region_name"])
    return dynamodb.Table(config["aws"]["table_name"])


def load_countries():
    with open('countries.json', 'r') as file:
        return json.load(file)


reddit = get_reddit_client()
table = get_dynamodb_table()
analyzer = SentimentIntensityAnalyzer()
countries = load_countries()


def collect_analyze_and_save_sentiment(country):
    try:
        query = country['country_name']
        subreddit = reddit.subreddit('news')
        posts = subreddit.search(query, limit=100)

        sentiments = [
            analyzer.polarity_scores(post.title + ' ' +
                                     post.selftext)['compound']
            for post in posts
        ]

        average_sentiment = sum(sentiments) / len(
            sentiments) if sentiments else 0

        average_sentiment_decimal = Decimal(str(average_sentiment)).quantize(
            Decimal('0.0001'), rounding=ROUND_HALF_UP)

        table.update_item(Key={'country': country['country_id']},
                          UpdateExpression="""
                            SET country_name = :name,
                                #dt = :date,
                                average_sentiment = :sentiment
                            """,
                          ExpressionAttributeNames={'#dt': 'date'},
                          ExpressionAttributeValues={
                              ':name': country['country_name'],
                              ':date':
                              datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              ':sentiment': average_sentiment_decimal
                          })
    except Exception as e:
        print(f"Error processing {country}: {e}")


def handler(event, context):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(collect_analyze_and_save_sentiment, countries)
