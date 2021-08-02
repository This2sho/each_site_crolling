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


def Scroll_max(browser):
    time.sleep(2)
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    interval = 0.01 # 1초에 한번씩 스크롤 내림
    # prev_height = browser.execute_script("return document.body.scrollHeight")
    # 반복 수행
    # while True:
    #     # 스크롤 가장 아래로 내림
    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
    #     # 페이지 로딩 대기
    #     time.sleep(interval)

    #     # 현재 문서 높이를 가져와서 저장
    #     curr_height = browser.execute_script("return document.body.scrollHeight")
    #     if curr_height == prev_height:
    #         break

    #     prev_height = curr_height
    for i in range(1, 50):
        browser.execute_script(f"window.scrollTo(0, {i*500}) ")
        time.sleep(interval)
    print("스크롤 완료")

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.maximize_window()

page_no = 1
url = f"https://www.commanine.co.kr/shop/shopbrand.html?type=X&xcode=005&sort=&page={page_no}"
name = "commanine"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()


browser.get(url)
Scroll_max(browser)
# time.sleep(1)
soup = BeautifulSoup(browser.page_source, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://www.commanine.co.kr"
logo = item_url + soup.select_one("div.logo_area > h1 > a> img")['src']
description = "당신의 지친 피부에 ‘콤마(쉼)＇을 전달하다. 콤마나인은 바쁜 일상 속 잠깐의 쉼표, 쉼이 필요한 당신의 피부에게 안부를 묻습니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

item_cnt = 0
sells = soup.select('div.item')
for sell in sells:
    if(item_cnt >= 30):
        break
    item = dict()
    item["img"] = item_url + sell.select_one('img.MS_prod_img_s')['src']
    item["link"] = item_url+sell.select_one('a')['href']
    item["name"] = sell.select_one('div.txt > div.b1').get_text()
    item["price"] = sell.select_one('div.b3 > price').get_text()
    if(item["price"] == "0"):
        continue
    temp_list.append(item)
    item_cnt += 1

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