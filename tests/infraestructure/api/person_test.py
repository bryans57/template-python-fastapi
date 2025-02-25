from fastapi.testclient import TestClient

from src.infrastructure.api.main import app
from src.util import Enviroments
from tests.config.database.dao import (
    GenericDAOTest,
    PersonDAOTest,
)
from tests.config.mocks.informacion_db import insert_user_person


def test_get_person_data(setup_db):  # pylint: disable=unused-argument
    # Arrange
    application = TestClient(app)
    input_data1 = {"identifications": ["123456789", "987654321"], "fieldsInfo": ["city", "first_name", "age"]}

    generic_dao = GenericDAOTest(setup_db)
    generic_dao.execute_query(insert_user_person())

    resulta_data = [
        {"identification": "123456789", "city": "New York", "first_name": "John", "age": 30},
        {"identification": "987654321", "city": "Los Angeles", "first_name": "Jane", "age": 25},
    ]

    # Act
    result = application.post(f"{Enviroments.PREFIX}/example-people/info", json={**input_data1})

    # Assert
    data = result.json()
    assert result.status_code == 200
    assert data["data"] == resulta_data


basic_user = input_data = {
    "identification": "123456789",
    "first_name": "John",
    "last_name": "Doe",
    "weight": 70.50,
    "height": 1.75,
    "age": 30,
    "city": "New York",
    "country": "USA",
    "email": "john.doe@mail.com",
    "phone": "+123456789",
    "address": "123 Main St",
}


def test_add_person_data(setup_db):  # pylint: disable=unused-argument
    # Arrange
    application = TestClient(app)
    input_data1 = basic_user

    # Act
    result = application.post(f"{Enviroments.PREFIX}/example-people", json={**input_data1})

    # Assert

    assert result.status_code == 200
    response_json = result.json()
    assert response_json["isError"] is False
    assert "timestamp" in response_json
    assert response_json["data"] == input_data1

    person_dao_test = PersonDAOTest(setup_db)
    person_info = person_dao_test.get_person_info(input_data1["identification"])[0]

    person_info_dict = dict(person_info)  # No need to map columns manually
    assert input_data1.items() <= person_info_dict.items(), "Mismatch!"


def test_update_person_data(setup_db):  # pylint: disable=unused-argument
    # Arrange
    application = TestClient(app)
    input_data1 = {
        "identification": "123456789",
        "first_name": "John",
        "last_name": "Doe2",
        "city": "New York 2",
        "email": "john.doe2@mail.com",
    }

    sql_insert = (
        f"INSERT INTO person (identification, first_name, last_name, city, email) "
        f"VALUES ('{input_data1['identification']}', '{basic_user['first_name']}', "
        f"'{basic_user['last_name']}', '{basic_user['city']}', '{basic_user['email']}');"
    )

    generic_dao = GenericDAOTest(setup_db)
    generic_dao.execute_query(sql_insert)

    # Act
    result = application.put(f"{Enviroments.PREFIX}/example-people", json={**input_data1})

    # Assert

    assert result.status_code == 200
    response_json = result.json()
    assert response_json["isError"] is False
    assert "timestamp" in response_json
    assert response_json["data"].items() <= input_data1.items()

    person_dao_test = PersonDAOTest(setup_db)
    person_info = person_dao_test.get_person_info(input_data1["identification"])[0]

    person_info_dict = dict(person_info)  # No need to map columns manually
    assert input_data1.items() <= person_info_dict.items(), "Mismatch!"


def test_delete_person_data(setup_db):  # pylint: disable=unused-argument
    # Arrange
    application = TestClient(app)
    input_data1 = {"identifications": ["1234567891"]}

    sql_insert = (
        f"INSERT INTO person (identification, first_name, last_name, city, email) "
        f"VALUES ('{input_data1['identifications'][0]}', '{basic_user['first_name']}', "
        f"'{basic_user['last_name']}', '{basic_user['city']}', '{basic_user['email']}');"
    )

    generic_dao = GenericDAOTest(setup_db)
    generic_dao.execute_query(sql_insert)

    # Act
    result = application.request(
        "DELETE",
        f"{Enviroments.PREFIX}/example-people",
        json={**input_data1},
        headers={"Content-Type": "application/json"},
    )  # pylint: disable=unexpected-keyword-arg

    # Assert

    assert result.status_code == 200
    response_json = result.json()
    assert response_json["isError"] is False
    assert "timestamp" in response_json
    assert response_json["data"] == [
        {
            "identification": input_data1["identifications"][0],
            "city": basic_user["city"],
            "first_name": basic_user["first_name"],
            "last_name": basic_user["last_name"],
            "email": basic_user["email"],
        }
    ]

    person_dao_test = PersonDAOTest(setup_db)
    person_info = person_dao_test.get_person_info(input_data1["identifications"][0])

    assert person_info == []
