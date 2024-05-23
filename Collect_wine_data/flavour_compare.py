# 영문 풍미 데이터
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

# 한글 풍미 데이터 (영문 풍미 키와 매핑)
korean_flavour = {
    1: "블랙체리",
    2: "오디",
    3: "올리브",
    4: "자두",
    5: "구스베리",
    6: "민트",
    7: "바질",
    8: "세이지",
    9: "아몬드",
    10: "오레가노",
    11: "유칼립투스",
    12: "처빌",
    13: "피망",
    14: "할라피뇨",
    15: "허브",
    16: "홍차",
    17: "구운빵",
    18: "꿀",
    19: "돌",
    20: "마른낙엽",
    21: "맥주",
    22: "밀랍",
    23: "반창고",
    24: "버섯",
    25: "버터",
    26: "분필",
    27: "생강",
    28: "석연슬레이트",
    29: "숲바닥",
    30: "야생고기",
    31: "연필심",
    32: "염분",
    33: "절인고기",
    34: "점토",
    35: "젖은상자",
    36: "젖은자갈",
    37: "젖은토양",
    38: "치즈",
    39: "크림",
    40: "타르",
    41: "화분흙",
    42: "훈제육",
    43: "라벤더",
    44: "백합",
    45: "아카시아",
    46: "오렌지꽃",
    47: "인동덩굴",
    48: "자스민",
    49: "작약",
    50: "장미",
    51: "제라늄",
    52: "제비꽃",
    53: "포푸리",
    54: "히비스커스",
    55: "라임",
    56: "매실",
    57: "청배",
    58: "건포도",
    59: "무화과",
    60: "용과",
    61: "딸기",
    62: "라즈베리",
    63: "붉은자두",
    64: "석류",
    65: "체리",
    66: "크랜베리",
    67: "토마토",
    68: "귤",
    69: "레몬",
    70: "마멀레이드",
    71: "오렌지",
    72: "자몽",
    73: "구아바",
    74: "리치",
    75: "망고",
    76: "바나나",
    77: "키위",
    78: "파인애플",
    79: "풍선껌",
    80: "가죽",
    81: "견과류",
    82: "담배",
    83: "바닐라",
    84: "백단",
    85: "브리오슈",
    86: "삼나무",
    87: "시가박스",
    88: "에스프레소",
    89: "초콜릿",
    90: "캐러멜",
    91: "커피",
    92: "코코넛",
    93: "코코아",
    94: "콜라",
    95: "파이프담배",
    96: "헤이즐넛",
    97: "흑설탕",
    98: "블루베리",
    99: "모과",
    100: "복숭아",
    101: "사과",
    102: "살구",
    103: "감초",
    104: "계피",
    105: "붉은고추",
    106: "육두구",
    107: "정향",
    108: "팔각",
    109: "후추"
}

# 모든 항목이 일치하는지 검증
mismatch = []
for key in flavour_taste:
    if flavour_taste[key].lower() != korean_flavour[key].lower():
        mismatch.append((key, flavour_taste[key], korean_flavour[key]))

# 불일치 항목 출력
if mismatch:
    print("These items do not match:")
    for mis in mismatch:
        print(f"Key: {mis[0]}, English: {mis[1]}, Korean: {mis[2]}")
else:
    print("All items match correctly.")