import json
from unittest.mock import patch
from api_function.main import create_response, handler
from api_function.config import config


def test_create_response():
    response = create_response(200, {"message": "OK"})
    expected = {
        "statusCode": 200,
        "headers": config["cors"],
        "body": json.dumps({"message": "OK"})
    }
    assert response["statusCode"] == expected["statusCode"]
    assert json.loads(response["body"]) == json.loads(expected["body"])


@patch("api_function.main.table.scan")
def test_handler_get_success(mock_scan):
    mock_scan.return_value = {"Items": [{"id": "1", "name": "Test"}]}
    event = {"rawPath": "/", "requestContext": {"http": {"method": "GET"}}}
    response = handler(event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == [{"id": "1", "name": "Test"}]
