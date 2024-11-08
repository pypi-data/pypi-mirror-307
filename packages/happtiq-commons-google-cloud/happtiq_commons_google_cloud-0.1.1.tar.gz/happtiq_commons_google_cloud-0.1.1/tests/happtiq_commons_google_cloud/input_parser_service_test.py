import pytest
from happtiq_commons_google_cloud.input_parser_service import InputParserService

@pytest.fixture
def input_parser_service():
    return InputParserService()

def test_parse_input_with_json(input_parser_service):
    data = {
        "message": {
            "data": "eyJ0ZXN0IjogeyJrZXkiOiAidmFsdWUiLCAiYW5vdGhlciI6ICJpbnB1dCJ9LCAidGVzdDIiOiAic29tZXRoaW5nIn0="
        }
    }
    
    message_data = input_parser_service.parse_input(data)
    assert message_data == {"test": {"key": "value", "another": "input"}, "test2": "something"}

def test_parse_input_error(input_parser_service):
    data = {
        "message": {
            "data": "invalid-base64"
        }
    }
    with pytest.raises(Exception):
        input_parser_service.parse_input(data)
