import pytest
import pandas as pd
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.views import get_greeting, card_information, get_top_five_transactions, get_main_page_data


# Фикстура для подготовки тестовых данных
@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [datetime(2021, 12, 1), datetime(2021, 12, 15), datetime(2022, 1, 1)],
        "Сумма платежа": [-100, -200, -300],
        "Номер карты": ["1234", "1234", "5678"],
        "Категория": ["Food", "Food", "Entertainment"],
        "Описание": ["Lunch", "Dinner", "Movie"]
    }
    return pd.DataFrame(data)


# Тест для функции get_greeting
def test_get_greeting():
    assert get_greeting("2021-12-21 12:00:00") == "Добрый день"
    assert get_greeting("2021-12-21 08:00:00") == "Доброе утро"
    assert get_greeting("2021-12-21 20:00:00") == "Добрый вечер"
    assert get_greeting("2021-12-21 02:00:00") == "Доброй ночи"


# Тест для функции card_information
def test_card_information(sample_transactions):
    result = card_information(sample_transactions)
    expected = [
        {"last_digits": "1234", "total_spent": 300.0, "cashback": 3.0},
        {"last_digits": "5678", "total_spent": 300.0, "cashback": 3.0}
    ]
    assert result == expected


# Тест для функции get_top_five_transactions
def test_get_top_five_transactions(sample_transactions):
    result = get_top_five_transactions(sample_transactions)
    expected = [
        {"date": "01.12.2021", "amount": -100, "category": "Food", "description": "Lunch"},
        {"date": "15.12.2021", "amount": -200, "category": "Food", "description": "Dinner"},
        {"date": "01.01.2022", "amount": -300, "category": "Entertainment", "description": "Movie"}
    ]
    assert result == expected


# Тест для функции get_main_page_data
@patch('src.views.filtered_data_by_date')
@patch('src.views.get_currency_stocks')
@patch('src.views.get_exchange_rate')
def test_get_main_page_data(mock_get_exchange_rate, mock_get_currency_stocks, mock_filtered_data_by_date):
    mock_filtered_data_by_date.return_value = pd.DataFrame({
        "Дата операции": [datetime(2021, 12, 1)],
        "Сумма платежа": [-100],
        "Номер карты": ["1234"],
        "Категория": ["Food"],
        "Описание": ["Lunch"]
    })
    mock_get_currency_stocks.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_get_exchange_rate.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = get_main_page_data("2021-12-21 12:00:00")
    expected = {
        "greeting": "Добрый день",
        "cards": [{"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0}],
        "top_transactions": [{"date": "01.12.2021", "amount": -100, "category": "Food", "description": "Lunch"}],
        "currency_rates": [{"currency": "USD", "rate": 75.0}],
        "stock_prices": [{"stock": "AAPL", "price": 150.0}]
    }
    assert json.loads(result) == expected
