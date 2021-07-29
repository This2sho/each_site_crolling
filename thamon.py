from os import write
import requests
from bs4 import BeautifulSoup
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

url = "https://thamon.kr/all"
name = "thamon"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정

browser = webdriver.Chrome(options=options)
browser.maximize_window()

browser.get(url)
time.sleep(1)
# res = requests.get(url, headers=headers)
# res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(browser.page_source, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://contents.sixshop.com"
link_url = "https://thamon.kr/"
logo = soup.find("a", attrs={"href":"/"}).img["src"]
description = "타몬은 나뭇잎 특유의 질감, 가벼움, 물이 잘 스며들지 않는 성질을 살린 친환경 잎섬유 제품입니다. 저마다 다른 잎 고유의 무늬와 색상은 타몬의 제품 하나하나를 더욱 특별하게 만들어 줍니다. 타몬은 착한 소비를 추구하고 염색 및 제작 과정에서 자연에서 추출한 염료만을 사용하며 가죽과 같은 동물성 소재는 사용하지 않습니다. 수입의 일부는 숲을 보존하고 주변 지역사회의 지속 가능한 발전을 돕는 데 쓰이고 있습니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

sells = soup.find_all("div", attrs={"class":"shopProductWrapper"})

for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = item_url+sell.select_one('div.thumb')['imgsrc']
    item["link"] = link_url+sell.select_one('a')['href']
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

print("완료")