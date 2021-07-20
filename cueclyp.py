from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

url = "https://cueclyp.com/"
name = "cueclyp"

res = requests.get(url+"aboutcueclyp", headers=headers)
res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 브랜드 설명
# 상품 사진, 이름, 가격, 링크
logo = soup.find("a", attrs={"href":"/"}).img["src"]
description = soup.find("div", attrs={"class":"item-element"}).get_text()
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

res = requests.get(url+"new", headers=headers)
res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

sells = soup.find_all("div", attrs={"class":"shopProductWrapper"})
img_url = "https://contents.sixshop.com"
item_url = "https://cueclyp.com"
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = img_url + sell.find("div", attrs={"class":"img"})["imgsrc"]
    item["link"] = item_url + sell.a["href"]
    item["name"] = sell.a["alt"]
    item["price"] = sell.find("div", attrs={"class":"shopProduct price"}).get_text()
    temp_list.append(item)

# 잘 써졌는지 확인용
data[name] = temp_list
with open("test.json", "w", encoding="utf-8") as make_file:
    json.dump(data, make_file, indent="\t", ensure_ascii=False)

# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# 저장된 파일에 추가하기
# with open(file_name, 'r', encoding="utf-8") as f:
#     read_data = json.load(f)
# read_data[name] = temp_list
# with open(file_name, "w", encoding="utf-8") as make_file:
#     json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

print("완료")