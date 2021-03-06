from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


url = "https://ulkin.co.kr/product-category/unisex?orderby=popularity"
name = "ulkin"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
logo_d = dict()

res = requests.get(url, headers=headers)
res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "http://heureux.kr"
logo = soup.find("a", attrs={"href":"https://ulkin.co.kr/"}).img["src"]
logo_d["logo"] = logo
temp_list.append(logo_d)

sells = soup.find_all("div", attrs={"class":"col-inner"})

for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = sell.find("div", attrs={"class":"image-fade_in_back"}).a.img["src"]
    item["link"] = sell.find("div", attrs={"class":"image-fade_in_back"}).a["href"]
    item["name"] = sell.find("div", attrs={"class":"title-wrapper"}).get_text()
    item["price"] = sell.find("div", attrs={"class":"price-wrapper"}).get_text().split("\n")[1]
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