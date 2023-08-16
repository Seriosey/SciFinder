from pymed import PubMed
import pickle
from pathlib import Path

# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email="givan32@yandex.ru")

# Create a GraphQL query in plain text
query = "Hippocampus"

# Execute the query against the API
results = pubmed.query(query, max_results=5)

# Loop over the retrieved articles
import pathlib

for article in results:

    id = article.pubmed_id
    path = rf"C:\Users\Ivan\PycharmProjects\SciFinder\venv\Data_scipath\{id}.bin"

    file = open(path, 'wb')
    pickle.dump(article, file)
    file.close()
