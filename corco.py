from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

page_no = 1
url = f"https://corcoshop.com/product/list.html?cate_no=59&page={page_no}"
name = "corco"

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
item_url = "https://corcoshop.com"
logo = item_url + soup.select_one("div.xans-element- > span.pc_logo > a.navbar-brand > img")['src']
description = "현재 환경상태의 심각성을 바탕으로 나무를 베지 않고도 얻을 수 있는 코르크 나무껍질과 동물을 학대하면서 얻는 가죽이 아닌 친환경 적인 소재로 새로운 가치를 추구하는 착한 기업 코르코 입니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
while(item_cnt<30):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    sells = soup.select('div.row > div.xans-record-')
    for sell in sells:
        if(item_cnt >= 30):
            break
        item = dict()
        item["img"] = "https:" + sell.select_one('div.hb_img_box> a > img.img-fluid')['src']
        item["link"] = item_url+sell.select_one('div.hb_img_box > a')['href']
        item["name"] = sell.select_one('p.hb_prod_name > a > span').get_text()
        item["price"] = sell.select_one('p.hb_prodrecom_price').get_text()
        temp_list.append(item)
        item_cnt += 1
    page_no += 1
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