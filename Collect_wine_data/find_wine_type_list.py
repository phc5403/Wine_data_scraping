# import json
# import pandas as pd
# import requests
# import time
# wine_df = []
# #Create Empty DataFrame To Append To
# wine_cols = ['wineId', 'vintage', 'type']
# wine_df = pd.DataFrame(columns=wine_cols)
#
# for x in range(1,100):
#     r = requests.get(
#     "https://www.vivino.com/api/explore/explore",
#     params = {
#         "country_codes[]":"us",
#         "page": x,
#         "wine_type_ids": 3
#     },
#         headers= {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
#     }
#
#     )
#
#     if r.status_code == 200:
#         results = [
#             (
#                 # t["vintage"]["wine"]["winery"]["name"],
#                 t["vintage"]["wine"]["id"],
#                 f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
#                 # t["vintage"]["statistics"]["ratings_average"],
#                 # t["vintage"]["statistics"]["ratings_count"],
#                 # t["vintage"]["wine"]["region"]["country"]["name"],
#                 # t["vintage"]["wine"]["region"]["name"],
#                 # t["price"]["amount"],
#                 t["vintage"]["wine"]["type_id"]
#             )
#             for t in r.json()["explore_vintage"]["matches"]
#         ]
#
#         # Create temporary DataFrame from the results
#         temp_df = pd.DataFrame(results, columns=wine_cols)
#
#         # Append temporary DataFrame to the main DataFrame using concat
#         wine_df = pd.concat([wine_df, temp_df], ignore_index=True)
#
#     else:
#         print(f"Failed to fetch data for page {x}. Status code: {r.status_code}")
#         time.sleep(1)  # To handle rate limiting or network issues gracefully
#
#     # Assuming you might want to save the DataFrame to a CSV file after the loop
#     wine_df.to_json("wine_data.json", orient='records', lines=True)
#     print("Data has been saved to wine_data.json.")

import requests
import json

# Setup the API endpoint
url = "https://www.vivino.com/api/explore/explore"

# Base parameters for the API call
params = {
    "country_code": "US",  # Filter by country, e.g., USA
    # "country_codes[]": ["us", "fr", "it", "br", "ca", "de"],
    "page": 1,                # Start from the first page
    "per_page": 25,           # Maximum number of results per page as allowed by the API
    # "wine_type_ids[]": 1,  # 레드
    # "wine_type_ids[]": 2,  # 화이트
    # "wine_type_ids[]": 3,  # 스파
    # "wine_type_ids[]": 4,  # 로즈
    # "wine_type_ids[]": 7,  # 디저트
    "wine_type_ids[]": 24,  # 포티파이드
}

# Headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
}

# List to collect all relevant wine data
fortified_wine_list = []

cnt = 0
# Continue fetching until no more data is returned
while True:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        matches = data['explore_vintage']['matches']
        if not matches:  # Break the loop if no matches are found
            break
        for match in matches:
            wine_id = match['vintage']['wine']['id']
            year = match['vintage']['year']

            if year == "N.V." or year == "":
                print(f'Year 없음.. PASS')
                continue
            # Append the data to the list
            fortified_wine_list.append({
                "wine_id": wine_id,
                "year": year
            })
        params['page'] += 1  # Increment the page number for the next request
        cnt += 1

        if cnt == 500:
            print(f'500개 완료')
            break
        print(f'{cnt}개 탐색 중...')
    else:
        print(f"Failed to fetch data on page {params['page']}: {response.status_code}")
        break

# Save the collected wine data to a JSON file
with open('fortified_wine_list.json', 'w') as file:
    json.dump(fortified_wine_list, file, indent=4)

print("Wine data saved to fortified_wine_list.json.")

# 1168