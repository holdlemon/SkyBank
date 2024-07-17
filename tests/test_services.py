import pytest
import pandas as pd
import json
from src.services import find_transactions_with_phone_numbers


# Фикстура для подготовки тестовых данных
@pytest.fixture
def sample_data(tmp_path):
    data = {
        "Описание": [
            "Покупка +7 123 456-78-90",
            "Оплата +7 987 654-32-10",
            "Перевод без номера",
            "Телефон +7 111 222-33-44"
        ]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_data.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    return file_path


# Тест для функции find_transactions_with_phone_numbers
def test_find_transactions_with_phone_numbers(sample_data):
    result = find_transactions_with_phone_numbers(sample_data)
    expected = json.dumps([
        "Покупка +7 123 456-78-90",
        "Оплата +7 987 654-32-10",
        "Телефон +7 111 222-33-44"
    ], ensure_ascii=False, indent=4)
    assert json.loads(result) == json.loads(expected)


# Тест для случая, когда в данных нет номеров телефонов
def test_find_transactions_with_phone_numbers_no_phones(tmp_path):
    data = {
        "Описание": [
            "Перевод без номера",
            "Оплата без контакта"
        ]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_data_no_phones.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    result = find_transactions_with_phone_numbers(file_path)
    expected = json.dumps([], ensure_ascii=False, indent=4)
    assert json.loads(result) == json.loads(expected)


# Тест для случая, когда данные пусты
def test_find_transactions_with_phone_numbers_empty_data(tmp_path):
    data = {
        "Описание": []
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_data_empty.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    result = find_transactions_with_phone_numbers(file_path)
    expected = json.dumps([], ensure_ascii=False, indent=4)
    assert json.loads(result) == json.loads(expected)
