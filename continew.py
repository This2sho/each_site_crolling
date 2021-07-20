from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

url = "http://www.wecontinew.co.kr/product/list.html?cate_no=24"
name = "continew"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

res = requests.get(url, headers=headers)
res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

with open("test.html", "w", encoding='utf-8') as f:
    f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "http://www.wecontinew.co.kr"
logo = item_url + soup.find("div", attrs={"class":"Logo"}).a.img["src"]
description = "주식회사 모어댄의 업사이클링 브랜드 컨티뉴는 자동차 생산과정과 폐자동차에서 수거한 천연가죽, 안전벨트 및 에어백을 업사이클링하여 가방 및 악세사리로 제작하여 새로운 가치를 만들고 있습니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

sells = soup.find_all("li", attrs={"class":"item"})
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = "http:" + sell.find("div", attrs={"class":"description"}).a.img["data-original"]
    item["link"] = item_url+sell.div.a["href"]
    item["name"] = sell.find("p", attrs={"class":"name"}).get_text().replace("\n","")
    item["price"] = sell.find("li", attrs={"class":"xans-record-"}).get_text().replace("\n","")
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