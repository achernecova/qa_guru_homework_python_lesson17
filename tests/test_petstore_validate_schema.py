import jsonschema
import requests

from tests.schemas import response_user, user_data

BASE_URL = "https://petstore.swagger.io/v2/user/"

new_user = {
    "id": 5,
    "username": "Olga",
    "firstName": "Third",
    "lastName": "User",
    "email": "third_user@test.com",
}


def test_put_valid_schema_with_correct_user():
    requests.post(url=BASE_URL, json=new_user)
    response = requests.put(url=BASE_URL + "Man", json={"username": "Woman"})
    assert response.status_code == 200
    jsonschema.validate(instance=response.json(), schema=response_user)


def test_post_valid_schema_with_correct_user():
    response = requests.post(url=BASE_URL, json=new_user)
    response_user_data = requests.get(BASE_URL + "Olga")

    assert response.status_code == 200
    jsonschema.validate(instance=response_user_data.json(), schema=user_data)
