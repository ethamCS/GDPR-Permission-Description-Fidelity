from google_play_scraper import app
import pandas as pd
import sys

app_list = []

def main():
    apps = read_file()
    build_dataset(apps)

def read_file():
    if len(sys.argv) < 2:
        print("Usage: python3 datatset_builder.py filename")
        sys.exit("Error: no file provided")

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            app_list = file.read().split("\n")
        return app_list
    except FileNotFoundError:
        msg = f'Error: "{filename}" could not be found'
        sys.exit(msg)

def build_dataset(apps):
    
    df = pd.DataFrame(columns=['App_Name', 'App_ID', 'Sentence','STORAGE','CONTACT','LOCATION','CAMERA','MICROPHONE','SMS','CALL_LOG','PHONE','CALENDAR','SETTINGS','TASKS'])

    app_id_count = 1
    apps_not_found = 0

    for app_name in apps:
        ### FIXME 
        # Only temporary for dev stuff
        if app_id_count > 10:
            break

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
            apps_not_found += 1
            print("error: app not found")
            continue

        description = result_app_details['description']
        # tokenizing by new lines
        tokens = description.split('\n')

        for sentence in tokens:
            if sentence.strip():  # Check if the sentence is not an empty string after stripping whitespace
                df.loc[len(df.index)] = [app_name, app_id_count, sentence.strip()]
            print(df)
        app_id_count += 1

    # Remove empty rows from the DataFrame
    df = df[df['Sentence'].str.len() > 0]

    # Save the DataFrame to a CSV file
    df.to_csv('./datatset.csv', index=False)


if __name__ == '__main__':
    main()
