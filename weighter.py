import torch
from transformers import BertTokenizer, BertModel
import matplotlib.pyplot as plt

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

# Two lists of sentences
sentences1 = ['The cat sits outside',
             'A man is playing guitar',
             'The new movie is awesome']

sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']



# Load pre-trained model tokenizer (vocabulary)
#tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def weighter_k(first_keywords, second_keywords):
    # keywords_1 = df.loc[ df['pubmed_id'] == first_id, 'keywords' ].iloc[0]
    # keywords_2 = df.loc[ df['pubmed_id'] == second_id, 'keywords' ].iloc[0]

    #Compute embedding for both lists
    embeddings1 = model.encode(first_keywords, convert_to_tensor=True)
    embeddings2 = model.encode(second_keywords, convert_to_tensor=True)

    #Compute cosine-similarits
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    return cosine_scores

    #Output the pairs with their score
    # for i in range(len(sentences1)):
    #     print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
    #     print(keywords_1)