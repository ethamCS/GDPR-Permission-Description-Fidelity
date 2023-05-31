from google_play_scraper import app
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
    # tokenizing by new lines
    tokens = description.split('\n')

    for sentence in tokens:
        if sentence.strip():  # Check if the sentence is not an empty string after stripping whitespace
            df.loc[len(df.index)] = [app_name, app_id_count, sentence.strip()]

    app_id_count += 1

# Remove empty rows from the DataFrame
df = df[df['Sentence'].str.len() > 0]

# Save the DataFrame to a CSV file
df.to_csv('./test2.csv', index=False)
