from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

page_no = 1
url = f"https://harliek.com/product/list.html?cate_no=47&page={page_no}"
name = "harliek"

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
item_url = "https://harliek.com"
logo = item_url + soup.select_one("div.logo > a > img.logo_b")['src']
description = "할리케이(Harlie K)는 지속 가능한 라이프 스타일을 디자인합니다.\n버려지는 제품들에 예술과 공예적 가치를 불어넣어 시간이 흐를수록\n멋스러워지는 디자인으로 새롭게 재탄생시키는 업사이클 비건 패션 브랜드입니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
while (page_no <= 3) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    sells = soup.select('ul.prdList > li.xans-record-')

    for sell in sells:
        if(item_cnt >= 30):
            break
        item = dict()
        item["img"] = "https:"+ sell.select_one('div.thumbnail > a >img')['src']
        item["link"] = item_url+sell.select_one('div.thumbnail > a')['href']
        item["name"] = sell.select('strong.name>a > span')[1].get_text()
        item["price"] = sell.select('li.xans-record- > span')[1].get_text()
        temp_list.append(item)
        item_cnt += 1
    page_no += 1

# # 잘 써졌는지 확인용
# data[name] = temp_list
# with open("test.json", "w", encoding="utf-8") as make_file:
#     json.dump(data, make_file, indent="\t", ensure_ascii=False)


# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# # 저장된 파일에 추가하기
with open(file_name, 'r', encoding="utf-8") as f:
    read_data = json.load(f)
read_data[name] = temp_list
with open(file_name, "w", encoding="utf-8") as make_file:
    json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

print("완료")