import json
import os
from datetime import datetime

import pandas as pd
import yfinance as yf

import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")


def filtered_data_by_date(path: str, target_date: str) -> pd.DataFrame:
    """ Фильтрует данные по дате платежа """
    df = pd.read_excel(path)
    # df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")
    date = datetime.strptime(target_date, "%d.%m.%Y")
    start_of_month = date.replace(day=1)
    filtered_df = df[(df["Дата платежа"] >= start_of_month) & (df["Дата платежа"] <= date)]

    return filtered_df


def get_currency_stocks(path: str, target_currency:str = "RUB") -> str:
    """ Получает данные о валютах """
    stock_prices = []
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
                raise Exception(f"Ошибка запроса {response.status_code}")
    stock_prices_json = json.dumps({"currency_rates": stock_prices}, indent=2)
    return stock_prices_json


def get_exchange_rate(path:str) -> str:
    """ Получает данные об акциях """
    stock_prices = []
    with open(path, "r") as f:
        result = json.load(f)
        for ticker in result["user_stocks"]:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                price = data['Close'].iloc[0]
                stock_prices.append({"stock": ticker, "price": round(price, 2)})

    stock_prices_json = json.dumps({"stock_prices": stock_prices}, indent=2)
    return stock_prices_json


if __name__ == "__main__":
    file_path = "../data/operations.xls"
    print(filtered_data_by_date(file_path, "31.12.2021"))
    # print(get_currency_stocks("../user_settings.json"))
    # print(get_exchange_rate("../user_settings.json"))
