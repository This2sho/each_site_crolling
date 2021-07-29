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

url = "https://thepangaia.com/collections/all?sorting=best-sellers"
name = "pangaia"

browser.get(url)
Scroll_max(browser)
soup = BeautifulSoup(browser.page_source, "lxml")
# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())


# 필요한 데이터
# 로고 
# 브랜드 설명
# 상품 사진, 이름, 가격, 링크
logo = "data:image/png;base64,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"
description = "While 2020 has been an unpredictable year, we’ve achieved more this year than we could ever have imagined. We’re still committed to constantly evolving and finding new ways to protect our planet. We want to thank you for choosing PANGAIA and joining us in this mission. Without you, none of this would be possible."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

# try:
#     WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productPriceSpan")))
#     # 성공했을 때 동작
# except:
#     # 어떻게든 실행되는 구문 (자바의 try-catch-finally랑 비슷 하지만 파이썬에서는 catch대신 except 로 오류 처리)
#     print("에러다 임마.")
#     browser.quit()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(browser.page_source, "lxml")

sells = soup.find_all("div", attrs={"class":"product-card"})
# img_url = "https://contents.sixshop.com"
# item_url = "https://cueclyp.com"
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] =  sell.select_one('div>div>a>div>div>div>img')['src'] #find("div", attrs={"class":"product-card-images"}).select('div > div > img')["src"]
    item["link"] = sell.find("a", attrs={"class":"product-card__image-container"})["href"]
    item["name"] = sell.find("a", attrs={"class":"product-card__title"}).get_text()
    item["price"] = sell.select_one('div.product-card__price').get_text()
    temp_list.append(item)

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

browser.quit()
print("완료")