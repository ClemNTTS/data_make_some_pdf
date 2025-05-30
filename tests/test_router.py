from fastapi.testclient import TestClient
import base64
from app.main import app


client = TestClient(app)


def test_home_api():
    response = client.get("/")
    assert response.status_code == 200


def test_create_template():
    with open("tests/Cave_purple.png", "rb") as image_file:
        image_data = image_file.read()

    json_data = {
        "file_name": "test_template",
        "font": "Helvetica",
        "font_size": 12,
        "content": [
            {
                "element_type": "text",
                "content": "Hello, World!",
                "x": 100,
                "y": 750,
                "width": 0,
                "height": 0,
            },
            {
                "element_type": "image",
                "content": base64.b64encode(image_data).decode("utf-8"),
                "x": 100,
                "y": 700,
                "width": 200,
                "height": 100,
            },
            {
                "element_type": "input",
                "content": "input_field",
                "x": 100,
                "y": 650,
                "width": 200,
                "height": 20,
                "input_type": "text",
            },
            {
                "element_type": "input",
                "content": "checkbox_field",
                "x": 100,
                "y": 620,
                "width": 20,
                "height": 20,
                "input_type": "checkbox",
            },
        ],
    }

    response = client.post("/template", json=json_data)
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == 'attachment; filename="test_template.pdf"'
    )
    assert response.headers["Content-Type"] == "application/pdf"
