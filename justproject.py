from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

page_no = 1
url = f"http://just-project.com/shop/?&page={page_no}&sort=recent"
name = "justproject"

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
item_url = "http://just-project.com"
logo = soup.select_one("img.scroll_logo")['src']
description = "쓰레기를 편애하고 수집하며, 쓰레기로 일상의 물건을 만듭니다. 요즘은 쓰레기를 소재로서 진지하게 연구하고 있습니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
while(item_cnt<30):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    sells = soup.select('div.shop-item')
    for idx, sell in enumerate(sells):
        if(item_cnt >= 30):
            break
        item = dict()
        item["img"] = sell.select_one('img.org_img')['src']
        item["link"] = item_url+sell.select_one('a._fade_link')['href']
        item["name"] = sell.select('a._fade_link')[1].get_text()
        item["price"] = sell.select_one('p.pay').get_text()
        temp_list.append(item)
        item_cnt += 1
    page_no += 1

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