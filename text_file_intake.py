from google_play_scraper import app
from google_play_scraper import permissions
import pandas as pd

file_path = './app_List.txt'

def read_qualified_names(file_path):
    with open(file_path, 'r') as file:
        app_List = file.read().split(",")
    return app_List

app_List = read_qualified_names(file_path)

df = pd.DataFrame(columns=['App_Name', 'App_ID', 'Sentence'])

app_id_count = 1


for app_name in app_List:
    result_app_details = app(
        app_name,
        lang='en',  # defaults to 'en'
        country='eu'  # defaults to 'us'
    )

    description = result_app_details['description']
    # tokenizeing by new lines
    tokens = description.split('\n')
    

    for sentence in tokens:
         if len(sentence) > 1:
             df.loc[len(df.index)] = [app_name, app_id_count, sentence]

    app_id_count += 1
    print(df)

df.to_csv('./test.csv')
