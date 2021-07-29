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

url = "https://www.kaneitei.com/shop"
name = "kaneitei"

browser.get(url)
# Scroll_max(browser)
time.sleep(2)
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
item_url = "https://contents.sixshop.com"
link_url = "https://www.kaneitei.com"
logo = soup.select_one('img.site-logo')['src']
description = "카네이테이는 빈티지 군용 텐트를 재활용하여 제품을 만듭니다.\n카네이테이 제품은 시간의 흔적들이 만들어낸 자연스러운 다양성을 그대로 포용합니다. \n꾸며내고 다듬어서가 아닌 상처 나고 녹슨 있는 그대로의 모습에서 완전함을 느낍니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

sells = soup.select('div.shopProductWrapper')
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = item_url + sell.select_one('div.thumb')['imgsrc']
    item["link"] = link_url + sell.select_one('a')['href']
    item["name"] = sell.select_one('div.productName').get_text()
    item["price"] = sell.select_one('div.price').get_text()
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