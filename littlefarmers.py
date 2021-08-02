from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

url = "https://smartstore.naver.com/littlefarmers/category/3b624ed14740472f877f09e4cadd2495?cp=1"
name = "littlefarmers"

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
item_url = "https://smartstore.naver.com"
logo = soup.select_one("img._1QhZSUVBeK")['src']
description = "리틀파머스는 자연 본연이 가지고 있는 아름다움을 존중하고 그 가치에 중심을 둡니다. 건강한 땅 건강한 스타일, 건강한 삶을 추구하며 자연친화적이고 가치있는 소비를 지향합니다. 친환경적인 소재를 사용하고 불필요한 장식을 배재한 신발과 가방을 디자인하며 장인의 손길이 묻어나는 핸드메이드 작업 방식으로 자연스런 멋을 추구합니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

sells = soup.select('li.-qHwcFXhj0')
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = sell.select_one('img._25CKxIKjAk')['src']
    item["link"] = item_url+sell.select_one('a._3BkKgDHq3l')['href']
    item["name"] = sell.select_one('strong.QNNliuiAk3').get_text()
    item["price"] = sell.select_one('span.nIAdxeTzhx').get_text()
    temp_list.append(item)

# # 잘 써졌는지 확인용
# data[name] = temp_list
# with open("test.json", "w", encoding="utf-8") as make_file:
#     json.dump(data, make_file, indent="\t", ensure_ascii=False)


# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# 저장된 파일에 추가하기
with open(file_name, 'r', encoding="utf-8") as f:
    read_data = json.load(f)
read_data[name] = temp_list
with open(file_name, "w", encoding="utf-8") as make_file:
    json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

print("완료")