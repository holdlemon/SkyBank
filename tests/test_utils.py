import pytest
import pandas as pd
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.utils import filtered_data_by_date, get_currency_stocks, get_exchange_rate


# Фикстура для подготовки тестовых данных
@pytest.fixture
def sample_data():
    data = {
        "Дата операции": ["01.12.2021 12:00:00", "15.12.2021 12:00:00", "01.01.2022 12:00:00"],
        "Сумма платежа": [100, 200, 300]
    }
    return pd.DataFrame(data)


# Тест для функции filtered_data_by_date
def test_filtered_data_by_date(tmp_path, sample_data):
    # Сохраняем тестовые данные во временный файл
    file_path = tmp_path / "test_data.xlsx"
    sample_data.to_excel(file_path, index=False)

    # Вызываем функцию с тестовыми данными
    result = filtered_data_by_date(file_path, "2021-12-31 23:59:59")

    # Проверяем, что результат содержит только данные за декабрь 2021 года
    assert result["Дата операции"].apply(lambda x: x.month).unique() == [12]
    assert result["Дата операции"].apply(lambda x: x.year).unique() == [2021]


# Тест для функции get_currency_stocks
@patch('requests.get')
def test_get_currency_stocks(mock_get, tmp_path):
    # Подготавливаем mock для requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "conversion_rates": {
            "RUB": 75.0
        }
    }
    mock_get.return_value = mock_response

    # Подготавливаем тестовые данные
    test_data = {
        "user_currencies": ["USD"]
    }
    file_path = tmp_path / "test_settings.json"
    with open(file_path, "w") as f:
        json.dump(test_data, f)

    # Вызываем функцию с тестовыми данными
    result = get_currency_stocks(file_path)

    # Проверяем результат
    assert result == [{"currency": "USD", "rate": 75.0}]


# Тест для функции get_exchange_rate
@patch('yfinance.Ticker')
def test_get_exchange_rate(mock_ticker, tmp_path):
    # Подготавливаем mock для yfinance.Ticker
    mock_history = MagicMock()
    mock_history.history.return_value = pd.DataFrame({
        "Close": [100.0]
    })
    mock_ticker.return_value = mock_history

    # Подготавливаем тестовые данные
    test_data = {
        "user_stocks": ["AAPL"]
    }
    file_path = tmp_path / "test_settings.json"
    with open(file_path, "w") as f:
        json.dump(test_data, f)

    # Вызываем функцию с тестовыми данными
    result = get_exchange_rate(file_path)

    # Проверяем результат
    assert result == [{"stock": "AAPL", "price": 100.0}]