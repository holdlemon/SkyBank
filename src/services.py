import json
import logging
import os
import re

import pandas as pd


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(project_dir, 'logs')

# Создаем каталог logs, если он не существует
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logger = logging.getLogger("services.py")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(log_dir, 'services.log'), mode="w")
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def find_transactions_with_phone_numbers(path: str) -> str:
    """ Возвращает JSON-ответ с поиском по номерам телефонов """
    logger.info("Читаем данные из XLS файла")
    df = pd.read_excel(path)
    output_data = []
    phone_regex = re.compile(r'\+7 \d{3} \d{3}-\d{2}-\d{2}')

    for index, row in df.iterrows():
        description = str(row['Описание'])
        logger.info("Ищем данные с номерами телефонов")
        matches = phone_regex.findall(description)
        if matches:
            output_data.append(description)
    logger.info("Возвращаем JSON ответ с данными по номерам телефонов")
    return json.dumps(output_data, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    file = "../data/operations.xls"
    print(find_transactions_with_phone_numbers(file))

