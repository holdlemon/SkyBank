import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd


def get_transactions(file: str) -> pd.DataFrame:
    transaction = pd.read_excel(file)
    return transaction


def log(filename: Optional[str] = "../data/spending_by_category.xlsx") -> Callable:
    """ Деккоратор для записи отчета в файл xlsx """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            output_data = func(*args, **kwargs)
            df = pd.DataFrame(output_data)
            df.to_excel(filename, index=False)
            return output_data

        return wrapper

    return decorator


@log()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Возвращает траты по заданной категории и заданной дате """
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)

    start_date = current_date - timedelta(days=90)
    filtered_transactions = transactions[(transactions["Категория"] == category) &
                                         (transactions["Дата операции"] >= start_date) &
                                         (transactions["Дата операции"] <= current_date)]
    return filtered_transactions


if __name__ == "__main__":
    path = "../data/operations.xls"
    result = get_transactions(path)
    print(spending_by_category(result, "Супермаркеты", "2021-12-31"))
