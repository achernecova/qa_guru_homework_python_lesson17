import allure
import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2/user/"

list_new_users = [
    {
        "id": 1,
        "username": "Sasha",
        "firstName": "New First",
        "lastName": "User",
        "email": "first_user@test.com",
        "password": "passwordUser1",
        "phone": "+76662223355",
        "userStatus": 0,
    },
    {
        "id": 2,
        "username": "Anna",
        "firstName": "New Second",
        "lastName": "User",
        "email": "second_user@test.com",
        "password": "passwordSecond2",
        "phone": "+76665559977",
        "userStatus": 0,
    },
]
new_user = {
    "id": 4,
    "username": "Anna",
    "firstName": "Third",
    "lastName": "User",
    "email": "third_user@test.com",
    "password": "passwordUser3",
    "phone": "+75556663322",
    "userStatus": 0,
}


@allure.tag("GET-request")
@allure.description("Получение юзера по имени. Без post запроса предварительного - получаем 404 ошибку.")
def test_get_new_user_and_assert_username():
    requests.post(url=BASE_URL, json=new_user)
    response = requests.get(BASE_URL + "Anna")
    body = response.json()
    assert body["username"] == "Anna"
    assert response.status_code == 200


@allure.tag("GET-request")
@allure.description("Get user by a non-existent name")
def test_get_new_user_and_assert_status_code_404():
    response = requests.get(BASE_URL + "Оля")
    assert response.status_code == 404


@allure.tag("GET-request")
@allure.description("Get user by incorrect name")
def test_get_new_user_and_assert_status_code_405():
    response = requests.get(BASE_URL + "#sdrtgh")
    assert response.status_code == 405


@allure.tag("POST-request")
@allure.description("Add correct list new users")
def test_post_add_list_users_and_assert_status_code_200():
    response = requests.post(url=BASE_URL + "createWithList", json=list_new_users)
    body = response.json()
    assert body["message"] == "ok"
    assert body["code"] == 200


@allure.tag("POST-request")
@allure.description("Add correct user")
def test_post_add_correct_user_assert_status_code_200():
    response = requests.post(url=BASE_URL, json=new_user)
    assert response.status_code == 200


@allure.tag("POST-request")
@allure.description("Add user with incorrect name")
def test_post_add_incorrect_user_assert_status_code_500():
    response = requests.post(url=BASE_URL, json={"id": "#", "username": ""})
    assert response.status_code == 500


@allure.tag("PUT-request")
@allure.description("Меняем пользователя с некорректным именем.")
@pytest.mark.xfail(reason="Ошибка - ответ возвращается 200, хотя должен 404 т.к. пользователя с таким именем нет.")
def test_put_correct_user():
    requests.post(url=BASE_URL, json=new_user)
    response = requests.put(url=BASE_URL + "Man", json={"username": "Woman"})
    assert response.status_code == 404


@allure.tag("DELETE-request")
@allure.description("Удаляем существующего пользователя по имени")
def test_delete_user_with_correct_name():
    requests.post(url=BASE_URL, json={"id": 4, "username": "Woman"})
    response_delete_user = requests.delete(url=BASE_URL + "Woman")
    assert response_delete_user.status_code == 200


@allure.tag("DELETE-request")
@allure.description("Удаляем пользователя несуществующего")
def test_delete_user_with_incorrect_name():
    response_add_user = requests.delete(url=BASE_URL + "Oleg")
    assert response_add_user.status_code == 404
