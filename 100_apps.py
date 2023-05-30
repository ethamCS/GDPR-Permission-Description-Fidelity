from google_play_scraper import search

#assembling the qualified names of the top 100 health
#and lifestyle apps on the google play app store

i = "Health"
j = "Lifestyle"
k = "Fitness"

def get_app_ids(key_search):
    keyword = str(key_search) #improve input
    
    results = search(keyword, n_hits=30)
    for result in results:
        app_id = result['appId']
        app_ids.append(app_id)
    return app_ids

# Getting qualified names
app_ids = []
app_ids = get_app_ids(i)
app_ids.append(get_app_ids(j))
app_ids.append(get_app_ids(k))


app_ids= sorted(set(app_ids))

print(app_ids)


'''
app_ids = set(app_ids)
# Write app IDs to a text file
file_path = 'app_ids2.txt'
with open(file_path, 'w') as file:
    for app_id in app_ids:
        #find proper syntax for task
        if app_id in file: 
            continue
        else:
            file.write(f"{app_id}\n")
    

print(f"App IDs written to {file_path}")
'''