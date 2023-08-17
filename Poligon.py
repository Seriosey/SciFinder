from Graph import create_dataframe
from Graph import build_graph
from Graph import get_shortest_way

data_base_file = 'SciFinder_data.db'
df = create_dataframe(data_base_file, kwords_to_list=True)

id_list = df['pubmed_id']
keywords_list = df['keywords']
Graph = build_graph(id_list, keywords_list, drow=False)

print(id_list)
A = '37579923'
B = '37565054'
short_way = get_shortest_way(Graph, df, A, B)
