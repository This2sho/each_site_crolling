from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("windw-size=1902x1080") # pc해상도 설정

browser = webdriver.Chrome(options=options)
browser.maximize_window()


# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

url = "http://www.patagonia.co.kr/shop/inside/article.php?sno=27"
name = "patagonia"

browser.get(url)
soup = BeautifulSoup(browser.page_source, "lxml")
# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())


# 필요한 데이터
# 로고 
# 브랜드 설명
# 상품 사진, 이름, 가격, 링크
img_url = "http://www.patagonia.co.kr"
item_url = "http://www.patagonia.co.kr/shop"

logo = item_url + soup.find("a", attrs={"href":"/"}).img["src"]
description = soup.find("div", attrs={"class":"inside-article-content"}).get_text()
brand["logo"] = logo
brand["description"] = description.replace("\n",'')
temp_list.append(brand)

browser.find_element_by_xpath("//*[@id='gnb']/div[3]/strong").click()
browser.find_element_by_xpath("//*[@id='menuCategory']/ul[2]/li/strong/a").click()

# try:
#     WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productPriceSpan")))
#     # 성공했을 때 동작
# except:
#     # 어떻게든 실행되는 구문 (자바의 try-catch-finally랑 비슷 하지만 파이썬에서는 catch대신 except 로 오류 처리)
#     print("에러다 임마.")
#     browser.quit()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(browser.page_source, "lxml")

sells = soup.find("ul", attrs={"class":"after"}).find_all("li")

for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = img_url + sell.find("img")["src"]
    item["link"] = item_url + sell.find("a", attrs={"class":"goodsimg"})["href"].replace("..", '')
    try:
        item["name"] = sell.select_one("a.pname").get_text()
        item["price"] = sell.select_one("span.fontArial").get_text()
    except:
        continue
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