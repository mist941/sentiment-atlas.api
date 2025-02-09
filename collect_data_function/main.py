import time
import praw
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reddit = praw.Reddit(
    client_id='Wi_tu5pcSZysWpFeOHFcHA',
    client_secret='pxNIqYLYzdjNDMa4aOn5Lruhxo-CVg',
    user_agent='Sentiment Atlas',
    username='RipKlutzy2899',
    password='*Rjkq/u$7JdpaLS'
)
analyzer = SentimentIntensityAnalyzer()

with open('countries.json', 'r') as file:
    data = json.load(file)

countries = data

def collect_and_analyze_sentiment(country):
    try:
        query = country
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
        print(f"Average sentiment for {country}: {average_sentiment:.4f}")

    except Exception as e:
        print(f"Error processing {country}: {e}")

for country in countries:
    collect_and_analyze_sentiment(country)
    time.sleep(1)

print("Sentiment analysis completed for all countries.")

# import boto3
# from botocore.exceptions import ClientError

# def get_secret():

#     secret_name = "sentiment_atlas"
#     region_name = "us-east-1"

#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         # For a list of exceptions thrown, see
#         # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#         raise e

#     secret = get_secret_value_response['SecretString']

#     # Your code goes here.
