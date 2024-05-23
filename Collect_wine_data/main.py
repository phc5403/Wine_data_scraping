import re
import MySQLdb
import requests
import json
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# wine_id = 9478666
# vintage = 2021
flavour_type = {
    1: "black fruit",
    2: "green note",
    3: "other",
    4: "flower",
    5: "green fruit",
    6: "dried fruit",
    7: "red fruit",
    8: "citrus",
    9: "tropical fruits",
    10: "oak",
    11: "green fruit",
    12: "stone fruits",
    13: "spice"
}
flavour_taste = {
    1: "black cherry",
    2: "mulberry",
    3: "olive",
    4: "plum",
    5: "gooseberry",
    6: "mint",
    7: "basil",
    8: "sage",
    9: "almonds",
    10: "oregano",
    11: "eucalyptus",
    12: "chervil",
    13: "green pepper",
    14: "jalapeño",
    15: "herb",
    16: "black tea",
    17: "baked bread",
    18: "honey",
    19: "stone",
    20: "dry fallen leaves",
    21: "beer",
    22: "beeswax",
    23: "band-aid",
    24: "mushroom",
    25: "butter",
    26: "chalk",
    27: "ginger",
    28: "stone slate",
    29: "forest floor",
    30: "wild meat",
    31: "pencil lead",
    32: "saline",
    33: "cured meat",
    34: "clay",
    35: "wet box",
    36: "wet gravel",
    37: "wet soil",
    38: "cheese",
    39: "cream",
    40: "tar",
    41: "potting soil",
    42: "smoked meat",
    43: "lavender",
    44: "lily",
    45: "acacia",
    46: "orange blossom",
    47: "honeysuckle",
    48: "jasmine",
    49: "peony",
    50: "rose",
    51: "geranium",
    52: "violet",
    53: "potpourri",
    54: "hibiscus",
    55: "lime",
    56: "plum",
    57: "blue pear",
    58: "raisins",
    59: "fig",
    60: "dragon fruit",
    61: "strawberry",
    62: "raspberry",
    63: "red plum",
    64: "pomegranate",
    65: "cherry",
    66: "cranberry",
    67: "tomato",
    68: "tangerine",
    69: "lemon",
    70: "marmalade",
    71: "orange",
    72: "grapefruit",
    73: "guava",
    74: "rich",
    75: "mango",
    76: "banana",
    77: "kiwi",
    78: "pineapple",
    79: "bubble gum",
    80: "leather",
    81: "nuts",
    82: "tobacco",
    83: "vanilla",
    84: "sandalwood",
    85: "brioche",
    86: "cedar",
    87: "cigar box",
    88: "espresso",
    89: "chocolate",
    90: "caramel",
    91: "coffee",
    92: "coconut",
    93: "cocoa",
    94: "coke",
    95: "pipe smoking",
    96: "hazelnut",
    97: "brown sugar",
    98: "blueberry",
    99: "quince",
    100: "peach",
    101: "apple",
    102: "apricot",
    103: "licorice",
    104: "cinnamon",
    105: "red pepper",
    106: "nutmeg",
    107: "clove",
    108: "octagon",
    109: "pepper"
}

# RED WHITE SPARKLING ROSE DESSERT FORTIFIED
wineTypeName = {
    1: "RED",
    2: "WHITE",
    3: "SPARKLING",
    4: "ROSE",
    7: "DESSERT",
    24: "FORTIFIED",
}


def fetch_wine_tastes(wine_id):
    url = f"https://www.vivino.com/api/wines/{wine_id}/tastes?language=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 시간 지연
    time.sleep(1)
    # GET 요청을 보냅니다
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # primary_keywords 추출
        primary_keywords = extract_primary_keywords(data)
        # print(primary_keywords)
        return primary_keywords
    else:
        print(f"@@@ Error fetching data: Status code {response.status_code}")
        return False  # Taste 정보 없으면 데이터로 사용할 수 없음.


def extract_primary_keywords(data):
    global flavour_type, flavour_taste

    primary_keywords_list = []
    if "tastes" in data and "flavor" in data["tastes"]:
        if data["tastes"]["flavor"] is None:
            print(f'No flavor : PASS')
            return False
        for flavour in data["tastes"]["flavor"]:
            if "primary_keywords" in flavour:
                for keyword in flavour["primary_keywords"]:
                    primary_keywords_list.append(keyword["name"])
    return primary_keywords_list


# 산도, 바디감, 당도, 탄닌 값이 올바르게 존재하는지 검사
def exist_target(target, json_data):  # (산도 등의 대상, 산도 등의 대상 유형, 탐색할 JSON)
    data_frame = json_data['vintage']['wine']
    if 'style' in data_frame:
        data_frame = data_frame['style']  # style = null 인 경우 존재함.
        if data_frame is not None and 'baseline_structure' in data_frame:
            data_frame = data_frame['baseline_structure'][target]
            return data_frame
        else:
            return False
    else:
        return False


################ START ################
# 이미지 크롤링을 위한 세팅
# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")  # Disable notifications

# Setup service with ChromeDriverManager
service = Service(ChromeDriverManager().install())

# Create a driver instance with the specified options
driver = webdriver.Chrome(service=service, options=chrome_options)

# 와인 Id, Vintage 정보가 있는 JSON 로드
with open('./windId_vintage_list.json', 'r', encoding='utf-8') as file:
    wine_list = json.load(file)  # 2000개

# DB 연결
conn = MySQLdb.connect(
    host='localhost',
    user='ssafy',
    passwd='ssafy',
    db='wine_data_injection'
)

# 쿼리 세팅
wine_query = """INSERT INTO wine (name, seo_name, image_url, grape, winery, country, price, rating, vintage, type, acidity, intensity, sweetness, tannin, abv)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

flavour_taste_query = """INSERT INTO wine_flavour (wine_id, flavour_taste_id) VALUES(%s, %s)"""

cursor = conn.cursor()

search_count, correct = 0, 0
wine_index = 0  # Wine 테이블 컬럼 인덱스 체크
start = time.time()
################################################
try:
    for wlst in wine_list:
        time.sleep(1)  # 각 순회마다 요청 대기
        search_count += 1  # 현재 탐색 중 카운트
        wine_id = wlst['wine_id']
        vintage = wlst['vintage']
        # print(wine_id, vintage)

        # URL of the page to scrape
        url = f"https://www.vivino.com/w/{wine_id}?year={vintage}&currency_code=USD"

        # Headers with a custom User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Send a GET request to the page with custom headers
        response = requests.get(url, headers=headers)

        # JSON 파일 세팅
        file_path = './response_sample.json'  # Modify with your desired file path
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # Check if the request was successful
        if response.status_code == 200:
            # Use regex to find <script> tags containing "window.__PRELOADED_STATE__.winePageInformation ="
            match = re.search(r'window\.__PRELOADED_STATE__\.vintagePageInformation = (\{.*?\});', response.text, re.DOTALL)
            if match:
                # Extract the JSON-like content
                json_content = match.group(1)
                # Parse the JSON string into a Python dictionary
                data = json.loads(json_content)
                # Pretty-print the JSON data
                pretty_json = json.dumps(data, indent=4)

                # Save the pretty JSON to a file
                file_path = './vintage_data.json'  # Modify with your desired file path
                with open(file_path, 'w') as file:
                    file.write(pretty_json)
                # print(f"JSON data has been saved to {file_path}")
            else:
                print("No matching script tags found.")
        else:
            print("Failed to retrieve the webpage.")

        # 파일 경로
        file_path = './vintage_data.json'

        # JSON 파일 로드
        with open(file_path, 'r') as file:
            data = json.load(file)

        # 이미지 요소가 없으면 예외 처리 해야함
        # bottle_medium이 있으면 하고, 이미지 크롤링은 없는 경우에 해보자.
        BASE_URL = url
        driver.get(BASE_URL)
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "body > div.wrap > div.grid.topSection > div > div > div.mobile-column-3.tablet-column-3.desktop-column-2 > picture > img")))
        image_url = image_element.get_attribute('src')

        if image_url.startswith('//'):
            image_url = 'https:' + image_url

        # 필요한 데이터 추출 시작 #
        wine_name = data['vintage']['name']
        print("Wine Name:", wine_name)
        seo_name = data['vintage']['seo_name'].replace("-", " ")
        print("Wine SeoName:", seo_name)
        # image_url = "https:" + data['vintage']['image']['variations']['bottle_medium']  # 각종 null, 데이터 누락 존재
        print("Image URL:", image_url)
        grape = data['vintage']['wine']['region']['country']['most_used_grapes'][0]['name']
        print("Grape Name:", grape)

        if 'winery' not in data['vintage']['wine']:
            print(f'No Winery : PASS..')  # 450
            continue
        else:
            winery = data['vintage']['wine']['winery']['name']

        # print("Winery Name:", winery)
        country = data['vintage']['wine']['winery']['region']['country']['name']
        print("Country Name:", country)

        # price = data['price']['amount']  # 가격도 null 존재

        # 가격 로직 수정 + 소숫점 2자리까지
        price = 44.99
        # if 'price' not in data or 'amount' not in data['price']:
        #     price = 49.99
        # else:
        #     price = data['price']['amount']
        # price_factor = 7.310224431523974e-4
        # price = price * price_factor
        # price = f"{price:.2f}"
        # print("Price: ", price)

        average_rating = data['vintage']['statistics']['ratings_average']
        print("Average Rating:", average_rating)
        year = vintage  # "n.v."값 72개 + ""값 2개 = 74개 제외
        if year == "N.V." or year == "":
            print(f"Year 없음 PASS..")
            continue
        print("Year:", year)

        wine_type = data['vintage']['wine']['type_id']
        if wine_type in wineTypeName:
            wine_type = wineTypeName[wine_type]
        print("Wine Type:", wine_type)

        # tannin = data['vintage']['wine']['style']['baseline_structure']['tannin']
        acidity = exist_target('acidity', data)
        if acidity:
            acidity = f"{acidity:.7f}"
        # else:
        #     print(f'## Acidity 없음 PASS..')
        #     continue
        else:
            acidity = 0.0000000

        intensity = exist_target('intensity', data)
        if intensity:
            intensity = f"{intensity:.7f}"
        # else:
        #     print(f'## Intensity 없음 PASS..')
        #     continue
        else:
            intensity = 0.0000000

        sweetness = exist_target('sweetness', data)
        if sweetness:
            sweetness = f"{sweetness:.7f}"
        # else:
        #     print(f'## Sweetness 없음 PASS..')
        #     continue
        else:
            sweetness = 0.0000000

        tannin = exist_target('tannin', data)
        if tannin:
            tannin = f"{tannin:.7f}"
        # else:
        #     print(f'## Tannin 없음 PASS..')
        #     continue
        else:
            tannin = 0.0000000

        print(f'Acidity: {acidity}')
        print(f'Intensity: {intensity}')
        print(f'Sweetness: {sweetness}')
        print(f'Tannin: {tannin}')

        abv = data['vintage']['wine']['alcohol']
        if abv:
            abv = f"{abv:.1f}"
            print(f'Alcohol: {abv}')
        else:
            print(f'## Alcohol 없음 PASS..')
            continue


        # print("Taste:")
        f_taste = fetch_wine_tastes(wine_id)  # Flavour Taste 정보를 담는 LIST
        taste_lst = set()  # DB wine_flavour 테이블에 삽입 할 flavour_taste_id 값들을 저장.
        if not f_taste or f_taste is None:
            print(f'## Taste 정보 없음 PASS..')
            continue
        else:
            for taste in f_taste:
                for key, value in flavour_taste.items():
                    if value == taste:  # 해당 taste값이 DB 목록에 존재 할 경우
                        taste_lst.add(key)
        # 필요한 데이터 추출  종료 #


        # DB에 데이터 삽입 #
        # 1. Wine 테이블 컬럼 추가 sql 세팅
        cursor.execute(wine_query, (wine_name, seo_name, image_url, grape, winery, country, price, average_rating, year, wine_type, acidity, intensity, sweetness, tannin, abv))
        conn.commit()
        wine_idx = cursor.lastrowid

        # 2. Wine_Flavour 테이블 컬럼 추가 sql 세팅
        taste_lst = list(taste_lst)
        for taste in taste_lst:
            cursor.execute(flavour_taste_query, (wine_idx, taste))
            conn.commit()

        correct += 1  # 실제 유효한 데이터 개수
        wine_index += 1  # 데이터가 유효할 때만 테이블의 실제 인덱스값을 증가
        print(f'데이터 삽입 현황: {wine_index}')
        print(f"------------------ {search_count}개 탐색 중.. -----------------------")

    print("-----------------All PROCESS DONE ------------------------")
    print(f'총 {len(wine_list)}개 중 {correct}개 찾음..')

except MySQLdb.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    conn.rollback()  # 오류 발생 시 롤백

end = time.time()
print(f'소요 시간 : {end - start}')
cursor.close()
conn.close()
