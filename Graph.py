# добавить направления рёбер в зависимости от даты публикации
# перевести абстракты, результаты и заключения в векторы и кластеризовать их в векторном пространстве

import sqlite3 as sl
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from weighter import *
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

print()

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
            weight = weighter_k(first_keywords, second_keywords)
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
def get_shortest_way(G, A, B, drow:bool):
    # находит кратчайший путь между двумя узлами графа
    # если узлы никак не связаны, возвращает "Статьи не связаны"
    # G : graph
    # A, B : str - article`s pubmed ids
    # if keywords == True возвращает ключевые слова, по которым совпадают данные статьи
    result = nx.shortest_path(G, A, B)
    if result:
        print(f'Кратчайший путь от {A} к {B}: {result}')
    else:
        print( 'Статьи не связаны' )

    if drow == True:
        pos = nx.spring_layout(G, seed=7)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        node_color_list = []
        for node in G:
            if node == A or node == B:
                node_color_list.append('red')
            elif node in result[1:-1]:
                node_color_list.append('orange')
            else:
                node_color_list.append('blue')

        # Set all edge color attribute to black
        for e in G.edges():
            G[e[0]][e[1]]['color'] = 'black'
        # Set color of edges of the shortest path to green
        for i in range(len(result) - 1):
            G[result[i]][result[i + 1]]['color'] = 'red'
        # Store in a list to use for drawing
        edge_color_list = [G[e[0]][e[1]]['color'] for e in G.edges()]
        nx.draw(G, node_color=node_color_list, edge_color=edge_color_list, with_labels=True)
        plt.show()

        print( G.edges[A, B]['weight'] )


def get_keywords(first_id, second_id, df):
    keywords_1 = df.loc[ df['pubmed_id'] == first_id, 'keywords' ].iloc[0]
    keywords_2 = df.loc[ df['pubmed_id'] == second_id, 'keywords' ].iloc[0]
    print(keywords_1)
    matching_words = []
    for word in keywords_1:
        if word in keywords_2:
            matching_words.append(word)
    if matching_words == []:
        print('Совпадений по ключевым словам нет')
    else:
        print (f'Совпадающие ключевые слова: {matching_words}')
    print(keywords_1, '\n', keywords_2)

