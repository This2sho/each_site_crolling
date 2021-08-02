from os import write
import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
import time

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.maximize_window()

page_no = 1
url = f"https://fragiled-earth.com/product-category/women/page/{page_no}/"
name = "fragiled"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

browser.get(url)
# Scroll_max(browser)
time.sleep(1)
soup = BeautifulSoup(browser.page_source, "lxml")
# res = requests.get(url, headers=headers)
# res.raise_for_status()
# # res.encoding = 'euc-kr'
# soup = BeautifulSoup(res.text, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://allbirds.co.kr"
logo = "https://fragiled-earth.com/wp-content/uploads/2020/06/-1-768x131.png"
description = "‘프레자일’은 흔히 배송업체에서 많이 쓰이는 표현입니다. 깨지기 쉬운 물건이 배송과정에서 파손되는 사고를 방지하기 위해 배송업체는 포장 겉면에 ‘프레자일’이라는 스티커를 부착합니다. 이렇게 작은 스티커 하나가 부착되면 배송업체는 배송품을 대하는 자세를 달리합니다. ‘프레자일드’는 우리가 지구를 대하는 자세에 대해 이야기하는 브랜드입니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
sells = soup.select("article.product")
while (item_cnt < 30) :
    for sell in sells:
        if(item_cnt >= 30):
            break
        item = dict()
        item["img"] = sell.select_one('div.elementor-image > a > img')['src']
        item["link"] = sell.select_one('div.elementor-image > a')['href']
        item["name"] = sell.select_one('h1.elementor-heading-title > a').get_text()
        item["price"] = sell.select_one('div.elementor-text-editor').get_text()
        temp_list.append(item)
        item_cnt += 1
    
# 잘 써졌는지 확인용
data[name] = temp_list
with open("test.json", "w", encoding="utf-8") as make_file:
    json.dump(data, make_file, indent="\t", ensure_ascii=False)


# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# # 저장된 파일에 추가하기
# with open(file_name, 'r', encoding="utf-8") as f:
#     read_data = json.load(f)
# read_data[name] = temp_list
# with open(file_name, "w", encoding="utf-8") as make_file:
#     json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

print("완료")