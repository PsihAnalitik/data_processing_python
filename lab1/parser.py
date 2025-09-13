'''
Данный скрипт скачивает N заданных вакансий из hh.ru
'''

import requests
from typing import Optional, List
from tqdm import tqdm
import json
import os

def download_data(vacancy_pattern: str, 
              items_size: int=2000,
              only_with_salary: bool=True, 
              per_page: int=100,
              save_path: str=None) -> Optional[List]:

    # Ограничения API
    if items_size > 2000:
        raise ValueError("items_size не может превышать 2000 — это ограничение API hh.ru")
    if per_page > 100:
        raise ValueError("per_page не может быть больше 100 — это ограничение API hh.")

    vacancies_url_get = 'https://api.hh.ru/vacancies'

    params = {
        "text": vacancy_pattern,
        "only_with_salary": only_with_salary,
        "per_page": per_page
    }
    # get запрос выглядит так: per_page - количество страниц и page - номер страницы.
    # API hh позволяет выдавать не более 2000 объектов по запросу.
    # В формате per_page & page. Максимальное количество per_page=100
    per_page = 100
    total_pages = (items_size + per_page -1)// per_page

    collected = []

    for page in tqdm(range(total_pages), desc="Загрузка вакансий"):
        params["page"] = page
        response = requests.get(url=vacancies_url_get, params=params)

        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            break
        items = response.json().get("items", [])
        collected.append(items)

    collected = sum(collected, [])
    if save_path:
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        
        if save_path.endswith('.json'):
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(collected, f, indent=2)
        else:
            raise ValueError("save_path должен оканчиваться на .json")
        print(f"Данные сохранены в {save_path}")
    else:
        return collected


def main():
    save_path = 'data/Programmer_vacancies.json'
    download_data('Разработчик', save_path=save_path)

if __name__ == '__main__':
    main()