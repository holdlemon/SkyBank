import json
import re

import pandas as pd


def find_transactions_with_phone_numbers(path: str) -> str:
    """ Возвращает JSON-ответ с поиском по номерам телефонов """
    df = pd.read_excel(path)
    output_data = []
    phone_regex = re.compile(r'\+7 \d{3} \d{3}-\d{2}-\d{2}')

    for index, row in df.iterrows():
        description = str(row['Описание'])
        matches = phone_regex.findall(description)
        if matches:
            output_data.append(description)

    return json.dumps(output_data, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    result = find_transactions_with_phone_numbers("../data/operations.xls")
    print(result)
