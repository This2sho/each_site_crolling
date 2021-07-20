from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

url = "https://cueclyp.com/new"
name = "cueclyp"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
logo_d = dict()

browser.get(url)
soup = BeautifulSoup(browser.page_source, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://contents.sixshop.com"
logo = soup.find("a", attrs={"href":"/"}).img["src"]
logo_d["logo"] = logo
temp_list.append(logo_d)

sells = soup.find_all("div", attrs={"class":"shopProductWrapper"})

for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = item_url+sell.find("div", attrs={"class":"thumb img"})["imgsrc"]
    item["link"] = item_url+sell.a["href"]
    item["name"] = sell.find("div", attrs={"class":"shopProduct productName"}).get_text()
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