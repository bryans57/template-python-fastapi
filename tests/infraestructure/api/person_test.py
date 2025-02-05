from fastapi.testclient import TestClient

from src.conf import injector
from src.infrastructure.api.main import app
from src.infrastructure.database.postgresql import Postgresql
from src.util import Enviroments
from tests.config.database.dao import GenericDAOTest
from tests.config.mocks.informacion_db import insert_user_person


def test_get_person_data(setup_db):  # pylint: disable=unused-argument, too-many-locals
    # Arrange
    application = TestClient(app)
    input_data = {"identifications": ["123456789", "987654321"], "fieldsInfo": ["city", "first_name", "age"]}

    generic_dao = GenericDAOTest(injector.get(Postgresql))
    generic_dao.execute_query(insert_user_person())

    resulta_data = [
        {"identification": "123456789", "city": "New York", "first_name": "John", "age": 30},
        {"identification": "987654321", "city": "Los Angeles", "first_name": "Jane", "age": 25},
    ]

    # Act
    result = application.post(f"{Enviroments.PREFIX}/example-people/info", json={**input_data})

    # Assert
    data = result.json()
    assert result.status_code == 200
    assert data["data"] == resulta_data
