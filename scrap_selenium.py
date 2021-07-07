from bs4 import BeautifulSoup
from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

url = "https://codegreen.io/shop"
name = "codegreen"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
logo_d = dict()

browser.get(url)
soup = BeautifulSoup(browser.page_source, "lxml")

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://codegreen.io"
logo = item_url+ soup.find("div", attrs={"class":"logo_mobile"}).img["src"]
logo_d["logo"] = logo
temp_list.append(logo_d)

sells = soup.find_all("a", attrs={"class":"card_badge_best--wrapper"})

for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = sell.img["src"]
    item["name"] = sell.next_sibling.h4.get_text()
    item["price"] = sell.next_sibling.div.span.get_text()
    item["link"] = item_url+ sell["href"]
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