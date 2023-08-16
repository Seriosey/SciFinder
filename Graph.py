# выделить подтаблицу из pubmed_id и keywords в pandas
# перебрать все id и для каждых двух найти число пересекающихся keywords, записать эти числа в таблицу графа с помощью networkx
# построить граф
# визуализировать граф

# добавить направления рёбер в зависимости от даты публикации

import sqlite3 as sl
import pandas as pd
import io
import csv

db = sl.connect('SciFinder_data.db')
df = pd.read_sql_query("SELECT rowid, pubmed_id, keywords FROM SciFinder_data WHERE rowid < 50 AND keywords <> '[]'", db)

db.close()

df['keywords'] = df['keywords'].str.replace(', ', ',')
df['keywords'] = df['keywords'].str.replace('"', '')
df['keywords'] = df['keywords'].str.replace("'", "")
df['keywords'] = df['keywords'].str.replace("[", "")
df['keywords'] = df['keywords'].str.replace("]", "")
df['keywords'] = df['keywords'].str.replace("’", "")

# перевод получившихся строк в списки
def str_to_list(str_tensor):
    # str_tensor - coloumn of strings to be converted to lists
    pd.options.mode.chained_assignment = None
    for idx, row in enumerate(str_tensor):
        new_row = []
        if "," in row:
            sp = row.split(",")
            for s in sp:
                new_row.append(s)
                str_tensor[idx] = new_row
    return str_tensor

pd_with_lists = str_to_list(df['keywords'])


id_list = df['pubmed_id'].to_list()

# id_id_weight_dict = dict.fromkeys(id_list)

id_id_weight_list = []

for first_id, first_keywords in zip(df['pubmed_id'], df['keywords']):
    weight_counter = 0
    for second_id, second_keywords in zip(df['pubmed_id'], df['keywords']):
        for word in first_keywords:
            if word in second_keywords:
                weight_counter += 1
                new_row = [first_id, second_id, weight_counter]
                id_id_weight_list.append(new_row)
print(id_id_weight_list)

