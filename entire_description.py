from google_play_scraper import app
import pandas as pd

# retrieving app descriptions

app_List = ["com.winwalk.android","com.mapmyride.android2","com.achievemint.android"]

df = pd.DataFrame(columns=['App_Name', 'App_ID', 'Sentence'])

app_id_count = 0


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