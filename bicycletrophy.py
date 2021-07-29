from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import time

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정

browser = webdriver.Chrome(options=options)
browser.maximize_window()

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
    for i in range(1, 16):
        browser.execute_script(f"window.scrollTo(0, {i*500}) ")
        time.sleep(interval)
    print("스크롤 완료")


# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

url = "http://bicycletrophy.cafe24.com/product/list.html?cate_no=45"
name = "bicycletrophy"

browser.get(url)
# Scroll_max(browser)
time.sleep(1)
soup = BeautifulSoup(browser.page_source, "lxml")
# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())


# try:
#     WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productPriceSpan")))
#     # 성공했을 때 동작
# except:
#     # 어떻게든 실행되는 구문 (자바의 try-catch-finally랑 비슷 하지만 파이썬에서는 catch대신 except 로 오류 처리)
#     print("에러다 임마.")
#     browser.quit()
# res.encoding = 'euc-kr'
# soup = BeautifulSoup(browser.page_source, "lxml")

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "http://bicycletrophy.cafe24.com"
logo = item_url + soup.select_one('div.logo_img > a > img')['src']
description = "설명없음"
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

sells = soup.select('ul.prdList > li')
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = sell.select_one('img')['src']
    item["link"] = sell.select_one('a.avurl')['href']
    item["name"] = sell.select('p.name > strong > span')[1].get_text()
    item["price"] = sell.select('li.xans-record- > span')[0].get_text()
    temp_list.append(item)

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

browser.quit()
print("완료")