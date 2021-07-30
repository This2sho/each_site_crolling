from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

page_no = 1
url = f"http://www.119reo.com/25/?&page={page_no}&sort=recent"
name = "119reo"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

# res = requests.get(url, headers=headers)
# res.raise_for_status()
# res.encoding = 'euc-kr'
# soup = BeautifulSoup(res.text, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://reblank.cafe24.com"
logo = "data:image/jpeg;base64,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"
description = "리블랭크는 버려진 가죽, 타폴린, 원단 등을 활용하여 다시 사용할 수 있도록\n쓰임새와 디자인을 연구 합니다.\n자연에서 나와 자연으로 돌아감으로써 환경에 해를 끼치지 않는\n선순환이 가능한 [       ]를 만드는 것을 목표로 합니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

while (dsa <= 26) :
    url = f"https://reblank.cafe24.com/product/list.html?cate_no={category_no}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    sells = soup.select('ul.grid4 > li.xans-record-')

    for idx, sell in enumerate(sells):
        if(idx >= 30):
            break
        item = dict()
        item["img"] = sell.select_one('img.thumb')['src']
        item["link"] = item_url+sell.select_one('div.box > a')['href']
        item["name"] = sell.select_one('p.name').get_text()
        if(category_no == 25):
            item["price"] = sell.select_one('li.first').get_text()
        else:
            item["price"] = sell.select_one('#span_product_tax_type_text').parent.get_text()
        temp_list.append(item)
    category_no += 1

# 잘 써졌는지 확인용
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