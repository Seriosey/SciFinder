# выделить подтаблицу из pubmed_id и keywords в pandas
# перебрать все id и для каждых двух найти число пересекающихся keywords, записать эти числа в таблицу графа с помощью networkx
# построить граф
# визуализировать граф

# добавить направления рёбер в зависимости от даты публикации

import sqlite3 as sl
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import io
import csv


def create_dataframe(data_base_file, kwords_to_list:bool):
    # if kwords_to_list == True, convert string of keywords to list

    db = sl.connect(data_base_file)
    df = pd.read_sql_query("SELECT rowid, pubmed_id, keywords FROM SciFinder_data WHERE rowid < 50 AND keywords <> '[]'", db)
    db.close()
    df['keywords'] = df['keywords'].str.replace(', ', ',')
    df['keywords'] = df['keywords'].str.replace('"', '')
    df['keywords'] = df['keywords'].str.replace("'", "")
    df['keywords'] = df['keywords'].str.replace("[", "")
    df['keywords'] = df['keywords'].str.replace("]", "")
    df['keywords'] = df['keywords'].str.replace("’", "")

    # перевод получившихся строк в списки
    if kwords_to_list == True:
        pd.options.mode.chained_assignment = None
        for idx, row in enumerate(df['keywords']):
            new_row = []
            if "," in row:
                sp = row.split(",")
                for s in sp:
                    new_row.append(s)
                    df['keywords'][idx] = new_row
    return df

# построение графа
def build_graph(id_list, keywords_list, drow:bool):
    # id_list : list of pubmed_ids
    # keywords_list : list of keywords
    # if drow == True, create matplotlib graph
    G = nx.Graph()
    for first_id, first_keywords in zip(id_list, keywords_list):
        weight = 0
        for second_id, second_keywords in zip(id_list, keywords_list):
            if first_id == second_id:
                break
            for word in first_keywords:
                if word in second_keywords:
                    weight += 1
            weight /= len(second_keywords) + len(first_keywords)
            G.add_edge(first_id, second_id, weight=weight)

    # удаление рёбер с нулевым весом
    remove = []
    for edge in G.edges.data('weight'):
        if edge[2] == 0:
            remove.append(edge)
    G.remove_edges_from(remove)

    # построение графа
    if drow == True:
        pos = nx.spring_layout(G, seed=7)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        nx.draw_spring(G, with_labels=True)
        plt.show()
    return G


# поиск кратчайшего пути между двумя узлами
def get_shortest_way(G, df, A, B):
    # находит кратчайший путь между двумя узлами графа
    # если узлы никак не связаны, возвращает "Статьи не связаны"
    # G : graph
    # df : dataframe with 'pubmed_id' coloumn
    # A, B : str - article`s pubmed ids
    result = nx.shortest_path(G, A, B)
    if result:
        print(f'Кратчайший путь от {A} к {B}: {result}')
    else:
        print( 'Статьи не связаны' )

