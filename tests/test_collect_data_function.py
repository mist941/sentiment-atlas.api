import os
import pytest
import json
import boto3
from unittest.mock import patch, MagicMock
from moto import mock_aws
from collect_data_function.main import load_countries, collect_analyze_and_save_sentiment, handler


@pytest.fixture
def mock_reddit():
    with patch("collect_data_function.main.praw.Reddit") as mock_reddit:
        mock_instance = mock_reddit.return_value
        mock_instance.subreddit.return_value.search.return_value = [
            MagicMock(title="Test Post", selftext="Test Content")
        ]
        yield mock_instance


@pytest.fixture
def mock_countries():
    return [{"country_id": "UA", "country_name": "Ukraine"}]


@pytest.fixture
def mock_countries_file(tmp_path):
    file_path = tmp_path / "countries.json"
    data = [{
        "country_id": "UA",
        "country_name": "Ukraine"
    }, {
        "country_id": "US",
        "country_name": "United States"
    }]
    file_path.write_text(json.dumps(data))

    return file_path


def test_load_countries(mock_countries_file):
    with patch("collect_data_function.main.open",
               lambda f, _: open(mock_countries_file, "r")):
        countries = load_countries()
        assert len(countries) == 2
        assert countries[0]["country_name"] == "Ukraine"


@mock_aws
def test_collect_analyze_and_save_sentiment():
    boto3.setup_default_session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"))

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

    country = {"country_id": "UA", "country_name": "Ukraine"}

    table.put_item(Item={"country": "UA", "country_name": "Ukraine"})

    with patch("collect_data_function.main.get_dynamodb_table",
               return_value=table):
        collect_analyze_and_save_sentiment(country)

    response = table.get_item(Key={"country": "UA"})
    assert "Item" in response
    assert response["Item"]["country_name"] == "Ukraine"


@patch("collect_data_function.main.collect_analyze_and_save_sentiment")
def test_handler(mock_collect):
    event = {}
    handler(event, None)

    mock_collect.assert_called()
