from pymed import PubMed
import pandas as pd
pubmed = PubMed(tool="PubMedSearcher", email="seriosey-s@yandex.ru")

## PUT YOUR SEARCH TERM HERE ##
search_term = "Interneurons"
results = pubmed.query(search_term, max_results=1000)
articleList = []
articleInfo = []



for article in results:
    print(article.toJSON)
# Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
# We need to convert it to dictionary with available function
    articleDict = article.toDict()
    articleList.append(articleDict)

print(articleList[0])

# Generate list of dict records which will hold all article details that could be fetch from PUBMED API
for article in articleList:
    
#Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
    pubmedId = article['pubmed_id'].partition('\n')[0]
    # Append article info to dictionary
    #if (article['title'] and article['keywords'] and article['journal'] and article['abstract'] and article['conclusions'] and article['methods'] and article['results'] and article['doi'] and article['publication_date'] and article['authors']):
    try:    
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
        print(article['title'], ' appended')
    


        # Generate Pandas DataFrame from list of dictionaries
        articlesPD = pd.DataFrame.from_dict(articleInfo)
        articlesPD[['keywords', 'authors']] = articlesPD[['keywords', 'authors']].astype(str)

    except KeyError as e:
            print("No such key in the article")

pd.set_option('display.max_columns', None)
articlesPD = articlesPD.applymap(str)

# convert to csv-file
export_csv = articlesPD.to_csv(r'/Users/sergejskorohod/Downloads/aspire/source/SciFinder/Articles/SciFinder_data.csv', index = None, header=True)

# convert to SQL-db
import sqlite3 as sl
con = sl.connect('SciFinder_data.db')
articlesPD.to_sql('SciFinder_data', con)

con.close()

#Print first 10 rows of dataframe
print('\n', articlesPD.head(10))