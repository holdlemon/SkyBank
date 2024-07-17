import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
from src.reports import get_transactions, spending_by_category  # Замените 'your_module' на имя вашего модуля


# Тест для функции get_transactions с использованием patch и mock
def test_get_transactions():
    with patch("pandas.read_excel") as mock_read_excel:
        mock_df = pd.DataFrame({
            "Дата операции": ["01.12.2021 12:00:00", "15.12.2021 12:00:00", "01.01.2022 12:00:00"],
            "Категория": ["Супермаркеты", "Супермаркеты", "Развлечения"],
            "Сумма": [100, 200, 300]
        })
        mock_read_excel.return_value = mock_df

        result = get_transactions("fake_file.xlsx")
        pd.testing.assert_frame_equal(result, mock_df)


# Тест для функции spending_by_category с использованием patch и mock
@patch("pandas.DataFrame.to_excel")
@patch("src.reports.datetime")  # Замените 'your_module' на имя вашего модуля
def test_spending_by_category(mock_datetime, mock_to_excel):
    mock_datetime.now.return_value = datetime(2022, 1, 1)
    mock_datetime.strptime.return_value = datetime(2022, 1, 1)

    transactions = pd.DataFrame({
        "Дата операции": ["01.12.2021 12:00:00", "15.12.2021 12:00:00", "01.01.2022 12:00:00"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Развлечения"],
        "Сумма": [100, 200, 300]
    })

    # Исправленный ожидаемый результат с правильным типом данных
    expected_result = pd.DataFrame({
        "Дата операции": [datetime(2021, 12, 1, 12, 0, 0), datetime(2021, 12, 15, 12, 0, 0)],
        "Категория": ["Супермаркеты", "Супермаркеты"],
        "Сумма": [100, 200]
    })

    result = spending_by_category(transactions, "Супермаркеты", "2022-01-01")
    pd.testing.assert_frame_equal(result, expected_result)
    mock_to_excel.assert_called_once()


# Тест для функции spending_by_category без указания даты
@patch("pandas.DataFrame.to_excel")
@patch("src.reports.datetime")  # Замените 'your_module' на имя вашего модуля
def test_spending_by_category_no_date(mock_datetime, mock_to_excel):
    mock_datetime.now.return_value = datetime(2022, 1, 1)

    transactions = pd.DataFrame({
        "Дата операции": ["01.12.2021 12:00:00", "15.12.2021 12:00:00", "01.01.2022 12:00:00"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Развлечения"],
        "Сумма": [100, 200, 300]
    })

    # Исправленный ожидаемый результат с правильным типом данных
    expected_result = pd.DataFrame({
        "Дата операции": [datetime(2021, 12, 1, 12, 0, 0), datetime(2021, 12, 15, 12, 0, 0)],
        "Категория": ["Супермаркеты", "Супермаркеты"],
        "Сумма": [100, 200]
    })

    result = spending_by_category(transactions, "Супермаркеты")
    pd.testing.assert_frame_equal(result, expected_result)
    mock_to_excel.assert_called_once()