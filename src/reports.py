import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_dir, 'logs')

# Создаем каталог logs, если он не существует
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logger = logging.getLogger("reports.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(log_dir, 'reports.log'), mode="w")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def get_transactions(file: str) -> pd.DataFrame:
    """ Получаем DataFrame для дальнейшего использование """
    logger.info("Подготоваливаем DataFrame для дальнейших действий")
    transaction = pd.read_excel(file)
    return transaction


def log(filename: Optional[str] = "../data/spending_by_category.xlsx") -> Callable:
    """ Деккоратор для записи отчета в файл xlsx """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            output_data = func(*args, **kwargs)
            df = pd.DataFrame(output_data)
            logger.info("Записываем данные в файл XLSX")
            df.to_excel(filename, index=False)
            return output_data

        return wrapper

    return decorator


@log()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Возвращает траты по заданной категории и заданной дате """
    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        if date is None:
            logger.info("Получаем текущую дату")
            current_date = datetime.now()
        else:
            logger.info("Получаем заданную дату")
            current_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)

        start_date = current_date - timedelta(days=90)
        filtered_transactions = transactions[(transactions["Категория"] == category) &
                                             (transactions["Дата операции"] >= start_date) &
                                             (transactions["Дата операции"] <= current_date)]
        logger.info("Возвращаем траты по заданной категории и заданной дате")
        return filtered_transactions
    except Exception as ex:
        logger.error(f"Ошибка: {ex}")


if __name__ == "__main__":
    path = "../data/operations.xls"
    result = get_transactions(path)
    print(spending_by_category(result, "Супермаркеты", "2021-12-31"))
