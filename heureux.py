from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


url = "http://heureux.kr/shop/shopbrand.html?type=N&xcode=005&mcode=003"
name = "heureux"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

res = requests.get(url, headers=headers)
res.raise_for_status()
res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

with open("test.html", "w", encoding='utf-8') as f:
    f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "http://heureux.kr"
logo = item_url+ soup.find("a", attrs={"href":"/index.html"}).img["src"]
description = "HEUREUX ‘오르바이스텔라’는 동물 친화적 가치소비 중심적인 브랜드로서, 이익의 20%를 동물 보호 단체에 기부 합니다. 'HEUREUX'[oe · roe]는 프랑스어로 '행복'을 의미하며 인류 뿐 아니라 동물과 모든 생명에게 행복을 가져다 주겠다는 리의 신념과 진심 어린 소망을 담고 있습니다.우리의 사명은 아름답고 지속 가능한 핸드백 및 제품을 만들며 책임 있는 생산과 소비를 장려하는 것입니다. 우리는 가죽 및 모피를 대신할 최고의 방법을 제시하고 높은 품질의 윤리적 공장과 협력하여 의식 있는 소비를 권장하는 잔인하지 않은 제품을 제공하고자 합니다. 여러분의 지원과 노력을 통해 '모두를 위한 행복'이라는 우리의 철학이 사회와 지구를 더 좋게 만들 수 있다고 믿습니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)


sells = soup.find_all("dl", attrs={"class":"item-list plan-list"})

for idx, sell in enumerate(sells):
    if(idx >= 29):
        break
    item = dict()
    item["img"] = item_url + sell.dt.a.img["src"]
    item["name"] = sell.find("li", attrs={"prd-name"}).get_text()
    item["price"] = sell.find("p").get_text()
    item["link"] = item_url+ sell.dt.a["href"]
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