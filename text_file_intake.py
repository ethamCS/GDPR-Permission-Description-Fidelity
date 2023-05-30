from google_play_scraper import app
from google_play_scraper import permissions
import pandas as pd

file_path = './app_ids2.txt'

def read_qualified_names(file_path):
    with open(file_path, 'r') as file:
        app_List = file.read().split("\n")
    return app_List

app_List = read_qualified_names(file_path)

df = pd.DataFrame(columns=['App_Name', 'App_ID', 'Sentence'])

app_id_count = 1


for app_name in app_List:
    if app_name == None: 
        continue
    try:
        result_app_details = app(
        app_name,
        lang='en',  # defaults to 'en'
        country='eu'  # defaults to 'us'
        )
    except: 
        print(app_name)
        print("error: app not found")
        continue


    description = result_app_details['description']
    # tokenizeing by new lines
    tokens = description.split('\n')
 

    for sentence in tokens:
         #see what is causing empty lines, then make a conditional for it
        if sentence.strip():  # Check if the sentence is not an empty string after stripping whitespace
            df.loc[len(df.index)] = [app_name, app_id_count, sentence.strip()]

    app_id_count += 1
    print(df)

# or parse the csv and remove empty rows 
df.to_csv('./test2.csv')
