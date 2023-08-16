# import sqlite3 as sl
# db = sl.connect('my-test.db')
#
# c = db.cursor()
#
# # c.execute("""CREATE TABLE articles (
# # title text,
# # full_text text,
# # views integer,
# # author text
# # )""")
#
#
# # c.execute("INSERT INTO articles VALUES ('LabSON is cool', 'LabSON Jobs', 100, 'LabSONLabSON')")
#
# c.execute(
# "SELECT rowid, * FROM articles WHERE --- ORDERED BY --- DESC"
# )
# print(c.fetchmany(2))
#
# c.execute("DELETE FROM articles WHERE ---")
#
# c.execute("UPDATE articles SET author = 'avtor', ---, --- WHERE ---")
#
# db.commit()
#
# db.close()


from Graph import df

ids_list = df['pubmed_id'].to_list()

edge_list = []
for id_1 in ids_list:
    for id_2 in ids_list:
        edge = (id_1, id_2)
        edge_list.append(edge)

import networkx as nx
import matplotlib.pyplot as plt

# G = nx.from_edgelist(edge_list)
#
# print(nx.adjacency_matrix(G))
#
# nx.draw_spring(G, with_labels=True)
# plt.show()
#
# A = ids_list[0]
# B = ids_list[10]
# print(nx.shortest_path(G, A, B))

G = nx.Graph()
G.add_edge(1, 2, weight=0.6)

pos = nx.spring_layout(G, seed=7)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)

nx.draw_spring(G, with_labels=True)

plt.show()