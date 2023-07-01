import os

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
test_email = os.getenv("TEST_EMAIL")
test_password = os.getenv("TEST_PASSWORD")

@pytest.mark.parametrize("email, password", [(test_email, test_password)])
def test_get_token(email, password):
    response = client.get(f"/v1/getToken?email={email}&password={password}")
    assert response.status_code == 200
    # Aquí puedes realizar más aserciones sobre los datos de respuesta

@pytest.mark.parametrize("email, password", [(test_email, test_password)])
def test_get_schedule(email, password):
    response = client.get(f"/v1/schedule?email={email}&password={password}")
    assert response.status_code == 200
    # Aquí puedes realizar más aserciones sobre los datos de respuesta

@pytest.mark.parametrize("email, password", [(test_email, test_password)])
def test_get_courses(email, password):
    response = client.get(f"/v1/courses?email={email}&password={password}")
    assert response.status_code == 200
    # Aquí puedes realizar más aserciones sobre los datos de respuesta

@pytest.mark.parametrize("email, password", [(test_email, test_password)])
def test_get_grades(email, password):
    course_data = {
        "courseType": "-",
        "campus": "320",
        "tipo_curso": "ACT",
        "empty": "0",
        "courseId": "INE001",
        "professor_code": "17034212",
        "type": "S",
        "section": "9004",
        "school_code": "CEI",
        "courseIdBB": "INE001-9004-2023-1-D"
    }
    response = client.post(f"/v1/grades?email={email}&password={password}", json=course_data)
    assert response.status_code == 200
    # Aquí puedes realizar más aserciones sobre los datos de respuesta
