import json
import pandas as pd
import matplotlib.pyplot
import seaborn
from typing import Optional
from tqdm import tqdm

def parse_dict(dict_ex: dict, columns: list) -> dict:
    results = {}

    for col in columns:
        attachments = col.split('.')
        attachments_size = len(attachments)
        if attachments_size <=1:
            results[col] = dict_ex[col]
            continue

        curr_dict = {}
        for i, attach in enumerate(attachments):
            if i == attachments_size-1:
                results[col] = curr_dict[attach]
                continue
            if i ==0:
                curr_dict = dict_ex[attach] 
                continue
            curr_dict = curr_dict[attach]
    
    return results
            

def load_data(file_path: str)-> Optional[pd.DataFrame]:
    if not file_path:
        return ValueError('filepath не может быть пустым!')
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

    except Exception as e:
        print("Ошибка при чтении файла:", e)

    columns_to_table = ['id', 'name', 'area.name', 
                        'salary.from', 'salary.to', 'salary.gross', 'salary.currency', 
                        'snippet.requirement', 'experience.name']
    table_dict = []

    for i in tqdm(range(len(data)), desc='Обработка объектов'):
        table_dict.append(parse_dict(data[i], columns_to_table))
    
    table_to_df = {key: [dict_i[key] for dict_i in table_dict] for key in columns_to_table}
    
    df = pd.DataFrame(table_to_df, columns=columns_to_table)


    return df


def main():
    
    data_path = 'data/'
    json_path = 'data/Programmer_vacancies.json'
    data = load_data(json_path)
    data.to_excel(data_path + 'table_prepared.xlsx', index=False)

if __name__ == '__main__':
    main()