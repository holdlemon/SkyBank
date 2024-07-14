import datetime as dt

import pandas as pd

from src.reports import spending_by_category, get_transactions
from src.services import find_transactions_with_phone_numbers
from src.utils import filtered_data_by_date, get_currency_stocks, get_exchange_rate
from src.views import get_main_page_data


def main_page():
    """ Приветствие на главной странице """
    user_currencies = get_currency_stocks("../user_settings.json")
    user_stocks = get_exchange_rate("../user_settings.json")
    print(
        f"""Здравствуйте!
        Ваши настройки:
        Курсы валют: {user_currencies}
        Курсы акций: {user_stocks}
        Путь к файлу с транзакциями по умолчанию: "data/operations.xls"
        Сегодняшняя дата: 31.12.2021
        """
    )

    path_to_file = input("Введите путь к файлу с транзакциями или ничего не вводи, чтобы оставить путь по умолчанию: ")
    user_date = input("Введите дату: ")
    if path_to_file == "" and user_date == "":
        path_to_file = "../data/operations.xls"
        user_date = "2021-12-31 23:59:59"
        transactions = filtered_data_by_date(path_to_file, user_date)

    else:
        transactions = filtered_data_by_date(path_to_file, user_date)

    if not isinstance(transactions, pd.DataFrame):
        return "Список транзакций не был получен"

    print("Главная страница:\n")
    print(get_main_page_data(user_date))

    return transactions


def user_func(transactions: pd.DataFrame) -> None:
    """Доступ к пользовательским возможностям"""

    print(
        """Вам доступны следующие функции:
    1. Поиск номеров телефона
    2. Выгрузка трат по выбранной категории за три месяца
        """
    )
    user_choice = input("Выберите функцию (введите её номер): ")
    match user_choice:
        case "1":
            while True:
                try:
                    path = input("Введите путь к файлу с операциями: ")
                    if path == "":
                        path = "../data/operations.xls"
                        print(find_transactions_with_phone_numbers(path))
                        break
                    else:
                        print(find_transactions_with_phone_numbers(path))
                        break
                except Exception as ex:
                    print(f"Ошибка: {ex}")

        case "2":
            while True:
                try:
                    category = input("Введите категорию: ")
                    date = input("Введите дату в формате ДД.ММ.ГГГГ или пропустите ввод для принятия текущей даты: ")
                    if date == "":
                        date = "2021-12-31"
                        path = "../data/operations.xls"
                        result = get_transactions(path)
                        print(spending_by_category(result, category, date))

                    print("Данные сохранены в файл reports/spending_by_category.xlsx")
                    break
                except Exception as ex:
                    print(f"Ошибка: {ex}")

        case _:
            print("\nОШИБКА ВВОДА! Укажите число 1 или 2")
            user_func(transactions)


if __name__ == "__main__":
    tr = main_page()
    if isinstance(tr, pd.DataFrame):
        user_func(tr)
