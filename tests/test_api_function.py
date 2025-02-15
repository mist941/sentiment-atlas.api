import json
from api_function.main import create_response
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
