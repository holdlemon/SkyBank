import json
import logging
import os
from datetime import datetime, time

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_dir, 'logs')

# Создаем каталог logs, если он не существует
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logger = logging.getLogger("utils.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(log_dir, 'utils.log'), mode="w")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)

load_dotenv()
API_KEY = os.getenv("API_KEY")


def filtered_data_by_date(path: str, target_date: str) -> pd.DataFrame:
    """ Фильтрует данные по дате платежа """
    logger.info("Открываем файл с данными в формате XLS")
    df = pd.read_excel(path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    # df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")
    date = datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")
    start_of_month = date.replace(day=1)
    end_of_month = datetime.combine(date, time.max)
    filtered_df = df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= end_of_month)]
    logger.info("Возвращаем данные, отсортированные с начала месяца по заданную дату")
    return filtered_df


def get_currency_stocks(path: str, target_currency: str = "RUB") -> list[dict]:
    """ Получает данные о валютах """
    stock_prices = []
    logger.info("Открываем файл с пользовательскими настройками и выбираем валюту для конвертации")
    with open(path, "r") as f:
        result = json.load(f)
        for currency in result["user_currencies"]:
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                price = data["conversion_rates"][target_currency]
                stock_prices.append({"currency": currency, "rate": round(price, 2)})
            else:
                logger.error("Ошибка запроса на конвертацию валюты")
                raise Exception(f"Ошибка запроса {response.status_code}")
    logger.info("Данные по валютам успешно получены")
    return stock_prices


def get_exchange_rate(path: str) -> list[dict]:
    """ Получает данные об акциях """
    stock_prices = []
    logger.info("Открываем файл с пользовательскими настройками и выбираем акции для отображения курса")
    with open(path, "r") as f:
        result = json.load(f)
        for ticker in result["user_stocks"]:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                price = data['Close'].iloc[0]
                stock_prices.append({"stock": ticker, "price": round(price, 2)})
    logger.info("Данные по акциям успешно получены")
    return stock_prices


if __name__ == "__main__":
    file_path = "../data/operations.xls"
    print(filtered_data_by_date(file_path, "2021-12-31 23:59:59"))
    # print(get_currency_stocks("../user_settings.json"))
    # print(get_exchange_rate("../user_settings.json"))
