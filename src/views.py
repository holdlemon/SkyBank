import json
import logging
import os
from datetime import datetime
from typing import Dict, List

import pandas as pd

from src.utils import filtered_data_by_date, get_currency_stocks, get_exchange_rate


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_dir, 'logs')

# Создаем каталог logs, если он не существует
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logger = logging.getLogger("views.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(log_dir, 'views.log'), mode="w")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_greeting(date_time: str) -> str:
    """ Приветствие в зависимости от времени суток """
    logger.info("Получаем дату и конвертируем в формат datetime")
    formatted_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = formatted_date.hour
    if 4 <= hour < 12:
        greeting_message = "Доброе утро"
    elif 12 <= hour < 17:
        greeting_message = "Добрый день"
    elif 17 <= hour < 23:
        greeting_message = "Добрый вечер"
    else:
        greeting_message = "Доброй ночи"
    logger.info("Приветствие в зависимости от времени суток")
    return greeting_message


def card_information(transactions: pd.DataFrame) -> list[dict]:
    """ Возвращает сумму операций и кэшбека по картам """
    result = []
    transaction = (transactions.loc[transactions["Сумма платежа"] < 0]
                   .groupby(by="Номер карты").agg("Сумма платежа").sum().to_dict())
    for card_number, total_spent in transaction.items():
        result.append({
            "last_digits": card_number,
            "total_spent": abs(round(total_spent, 2)),
            "cashback": abs(round(total_spent / 100, 2))
        }
        )
    logger.info("Выводим сумму операций и кэшбека по картам")
    return result


def get_top_five_transactions(transactions: pd.DataFrame) -> List[Dict]:
    """ Возвращает ТОП-5 транзакций по сумме платежа """
    result = []
    transaction = transactions.sort_values(by="Сумма платежа", ascending=False).iloc[:5].to_dict(orient="records")
    for transact in transaction:
        result.append({
            "date": transact["Дата операции"].strftime("%d.%m.%Y"),
            "amount": transact["Сумма платежа"],
            "category": transact["Категория"],
            "description": transact["Описание"]
        }
        )
    logger.info("Выводим ТОП-5 транзакций по сумме платежа")
    return result


def get_main_page_data(date_time: str, user_settings: str = "../user_settings.json",
                       path: str = "../data/operations.xls") -> str:
    greeting = get_greeting(date_time)
    transactions = filtered_data_by_date(path, date_time)
    card_data = card_information(transactions)
    top_transactions = get_top_five_transactions(transactions)
    currencies = get_currency_stocks(user_settings)
    stocks = get_exchange_rate(user_settings)

    output_json = json.dumps({
        "greeting": greeting,
        "cards": card_data,
        "top_transactions": top_transactions,
        "currency_rates": currencies,
        "stock_prices": stocks
    },
        indent=4,
        ensure_ascii=False
    )
    return output_json


if __name__ == "__main__":

    print(get_main_page_data("2021-12-21 12:00:00"))
