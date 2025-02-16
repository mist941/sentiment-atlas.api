import pytest
from unittest.mock import patch, MagicMock
import boto3
from moto import mock_aws


@pytest.fixture
def mock_reddit():
    with patch("collect_data_function.main.praw.Reddit") as mock_reddit:
        mock_instance = mock_reddit.return_value
        mock_instance.subreddit.return_value.search.return_value = [
            MagicMock(title="Test Post", selftext="Test Content")
        ]
        yield mock_instance


@pytest.fixture
@mock_aws
def mock_dynamodb():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="TestTable",
        KeySchema=[{
            "AttributeName": "country",
            "KeyType": "HASH"
        }],
        AttributeDefinitions=[{
            "AttributeName": "country",
            "AttributeType": "S"
        }],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        },
    )
    yield table


@pytest.fixture
def mock_countries():
    return [{"country_id": "UA", "country_name": "Ukraine"}]
