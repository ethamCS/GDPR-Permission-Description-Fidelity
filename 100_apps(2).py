from google_play_scraper import search

def get_app_ids(key_search):
    keyword = str(key_search)
    app_ids = []
    results = search(keyword, n_hits=30)
    for result in results:
        app_id = result['appId']
        app_ids.append(app_id)
    return app_ids

# Getting qualified names
app_ids = get_app_ids("Health") + get_app_ids("Lifestyle") + get_app_ids("Fitness") + get_app_ids("Sleep")

# Write app IDs to a text file
file_path = 'app_ids2.txt'
existing_ids = set()

# Read existing IDs from the file (if it exists)
try:
    with open(file_path, 'r') as file:
        existing_ids = set(line.strip() for line in file)
except FileNotFoundError:
    pass

# Filter out duplicate app IDs
app_ids = [app_id for app_id in app_ids if app_id not in existing_ids]

# Write filtered app IDs to the file
with open(file_path, 'a') as file:
    for app_id in app_ids:
        file.write(f"{app_id}\n")

print(f"App IDs written to {file_path}")
