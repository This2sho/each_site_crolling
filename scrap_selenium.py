from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import time

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("windw-size=1902x1080") # pc해상도 설정

browser = webdriver.Chrome(options=options)
browser.maximize_window()

def Scroll_max(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    interval = 1 # 1초에 한번씩 스크롤 내림
    prev_height = browser.execute_script("return document.body.scrollHeight")
    # 반복 수행
    while True:
        # 스크롤 가장 아래로 내림
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
        # 페이지 로딩 대기
        time.sleep(interval)

        # 현재 문서 높이를 가져와서 저장
        curr_height = browser.execute_script("return document.body.scrollHeight")
        if curr_height == prev_height:
            break

        prev_height = curr_height

    print("스크롤 완료")

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

url = "https://cueclyp.com/aboutcueclyp"
name = "cueclyp"

browser.get(url)
soup = BeautifulSoup(browser.page_source, "lxml")
# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())


# 필요한 데이터
# 로고 
# 브랜드 설명
# 상품 사진, 이름, 가격, 링크
logo = "http" + soup.find("a", attrs={"href":"/"}).img["src"]
description = soup.find("div", attrs={"id":"itemElement15435168"}).get_text()
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

browser.find_element_by_xpath("//*[@id='siteHeader']/div[3]/div[2]/div/ul/li[2]/a").click()
try:
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productPriceSpan")))
    # 성공했을 때 동작
except:
    # 어떻게든 실행되는 구문 (자바의 try-catch-finally랑 비슷 하지만 파이썬에서는 catch대신 except 로 오류 처리)
    print("에러다 임마.")
    browser.quit()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(browser.page_source, "lxml")

sells = soup.find_all("div", attrs={"class":"shopProductWrapper"})
img_url = "https://contents.sixshop.com"
item_url = "https://cueclyp.com"
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = img_url + sell.find("div", attrs={"class":"img"})["imgsrc"]
    item["link"] = item_url + sell.a["href"]
    item["name"] = sell.a["alt"]
    item["price"] = sell.find("span", attrs={"class":"productPriceSpan"}).get_text()
    temp_list.append(item)

# 잘 써졌는지 확인용
data[name] = temp_list
with open("test.json", "w", encoding="utf-8") as make_file:
    json.dump(data, make_file, indent="\t", ensure_ascii=False)

# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# 저장된 파일에 추가하기
# with open(file_name, 'r', encoding="utf-8") as f:
#     read_data = json.load(f)
# read_data[name] = temp_list
# with open(file_name, "w", encoding="utf-8") as make_file:
#     json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

browser.quit()
print("완료")