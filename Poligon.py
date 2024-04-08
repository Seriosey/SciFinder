from Graph import create_dataframe
from Graph import build_graph
from Graph import get_shortest_way
from weighter import base_model, dmis_biobert, doc2vec_model, gsarti_biobert, check_embeddings
from sklearn.cluster import kmeans_plusplus
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

data_base_file = 'SciFinder_data.db'
df = create_dataframe(data_base_file, kwords_to_list=True)

id_list = df['pubmed_id'].to_list()
keywords_list = df['keywords'].to_list()

def id_to_embeddings(id):
    keywords = df.loc[df['pubmed_id'] == id, 'keywords'].values[0]
    #print(keywords)
    embedding = base_model.encode(keywords, convert_to_numpy=True, normalize_embeddings = True) 
    return embedding
        
print(id_to_embeddings('37584417'))

embeddings = [id_to_embeddings(id) for id in id_list]


check_embeddings(keywords_list, model = base_model)

# X = np.array(embeddings, dtype=object)
# centers, indices = kmeans_plusplus(X, n_clusters=6, random_state=0)
# print('centers: ', centers)

# print(id_list)
# Graph = build_graph(id_list, keywords_list, drow=False)
# print(Graph)

# #print(id_list)
# A = '37586425'
# B = '37586373'
# short_way = get_shortest_way(Graph, A, B, drow=True) # ,df
# print(short_way)

# print()