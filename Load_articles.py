from pymed import PubMed
import pandas as pd
pubmed = PubMed(tool="PubMedSearcher", email="givan32@yandex.ru")

## PUT YOUR SEARCH TERM HERE ##
search_term = "Hippocampus"
results = pubmed.query(search_term, max_results=1000)
articleList = []
articleInfo = []

for article in results:
# Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
# We need to convert it to dictionary with available function
    articleDict = article.toDict()
    articleList.append(articleDict)

# Generate list of dict records which will hold all article details that could be fetch from PUBMED API
for article in articleList:
#Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
    pubmedId = article['pubmed_id'].partition('\n')[0]
    # Append article info to dictionary
    articleInfo.append({u'pubmed_id':pubmedId,
                       u'title':article['title'],
                       u'keywords':article['keywords'],
                       u'journal':article['journal'],
                       u'abstract':article['abstract'],
                       u'conclusions':article['conclusions'],
                       u'methods':article['methods'],
                       u'results': article['results'],
                       u'doi':article['doi'],
                       u'publication_date':article['publication_date'],
                       u'authors':article['authors']})

# Generate Pandas DataFrame from list of dictionaries
articlesPD = pd.DataFrame.from_dict(articleInfo)
articlesPD[['keywords', 'authors']] = articlesPD[['keywords', 'authors']].astype(str)
pd.set_option('display.max_columns', None)

# convert to csv-file
export_csv = articlesPD.to_csv(r'C:\Users\Ivan\PycharmProjects\SciFinder\venv\Data_scipath\SciFinder_data.csv', index = None, header=True)

# convert to SQL-db
import sqlite3 as sl
con = sl.connect('SciFinder_data.db')
articlesPD.to_sql('SciFinder_data', con)

con.close()

#Print first 10 rows of dataframe
print('\n', articlesPD.head(10))