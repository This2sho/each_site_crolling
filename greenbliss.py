from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

url = "http://www.greenbliss.co.kr/product/list.html?cate_no=37"
name = "greenbliss"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

res = requests.get(url, headers=headers)
res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "http://www.greenbliss.co.kr"
logo = item_url + soup.select_one("div#logo>a>img")['src']
description = "그린블리스는 예쁘고 편안한 양말, 마스크, 티셔츠 등 라이프스타일 제품을\n식물성 오가닉 소재로 환경에 해를 최소화하면서 만들고,\n자연과 동물의 소중함을 이야기하고 행동하려 노력하는 브랜드입니다.\n그린블리스는 자연에 나은 것이 우리에게 나은 것이라고 믿습니다.\n예쁘고 편안하게, 오래 쓰세요."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
sells = soup.select("ul.prdList>li.item")
for sell in sells:
    if(item_cnt >= 30):
        break
    item = dict()
    item["img"] = "https:" + sell.select_one('div.box> a > img.thumb')['src']
    item["link"] = item_url+sell.select_one('div.box> a')['href']
    item["name"] = sell.select_one('p.name > a > span').get_text()
    item["price"] = sell.select_one('li.xans-record->span').get_text()
    temp_list.append(item)
    item_cnt += 1
# 잘 써졌는지 확인용
# data[name] = temp_list
# with open("test.json", "w", encoding="utf-8") as make_file:
    # json.dump(data, make_file, indent="\t", ensure_ascii=False)


# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# 저장된 파일에 추가하기
with open(file_name, 'r', encoding="utf-8") as f:
    read_data = json.load(f)
read_data[name] = temp_list
with open(file_name, "w", encoding="utf-8") as make_file:
    json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

print("완료")