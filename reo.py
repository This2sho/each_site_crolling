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
item_url = "http://www.119reo.com"
logo = "https://cdn.imweb.me/thumbnail/20210728/f0c69bfbca671.png"
description = "119REO는 제품 판매 수익금의 50%를 소방단체에 기부하고,전시 및 토크쇼를 통해 시민들에게 오늘날 소방 현실을 알립니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
while (page_no <= 3) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    sells = soup.select('div.shop-item')

    for sell in sells:
        if(item_cnt >= 30):
            break
        item = dict()
        item["img"] = sell.select_one('a.shop-item-thumb > img')['src']
        item["link"] = item_url+sell.select_one('a.shop-item-thumb')['href']
        item["name"] = sell.select_one('div.item-pay>div>h2').get_text()
        item["price"] = sell.select_one('p.pay').get_text()
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