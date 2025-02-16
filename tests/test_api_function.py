import json
from unittest.mock import patch
from api_function.main import create_response, handler, config


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


@patch("api_function.main.table.scan")
def test_handler_get_failure(mock_scan):
    mock_scan.side_effect = Exception("DB error")
    event = {"rawPath": "/", "requestContext": {"http": {"method": "GET"}}}
    response = handler(event, None)

    assert response["statusCode"] == 500
    assert "error" in json.loads(response["body"])


def test_handler_options():
    event = {"requestContext": {"http": {"method": "OPTIONS"}}}
    response = handler(event, None)
    assert response["statusCode"] == 204


def test_handler_not_found():
    event = {
        "rawPath": "/unknown",
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }
    response = handler(event, None)
    assert response["statusCode"] == 404
