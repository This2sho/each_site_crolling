from os import write
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

url = "https://bbybstore.com/goods/goods_list.php?cateCd=004"
name = "bbyb"

# 저장할 파일 설정
file_name = "data.json"

data = dict() # 맨 처음 파일 쓸 때 씀. + test 용
temp_list = []
brand = dict()

res = requests.get(url, headers=headers)
res.raise_for_status()
# res.encoding = 'euc-kr'
soup = BeautifulSoup(res.text, "lxml")

# with open("test.html", "w", encoding='utf-8') as f:
#     f.write(soup.prettify())

# 필요한 데이터
# 로고 
# 상품 사진, 이름, 가격, 링크
item_url = "https://bbybstore.com"
logo = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAeFBMVEX///8AAADt7e1SUlKoqKiNjY0HBweZmZnx8fH19fVCQkInJyctLS2JiYnr6+v09PTT09PZ2dnf39+CgoJJSUl2dna0tLTGxsZiYmI6OjofHx8vLy9nZ2e9vb1YWFhubm6enp4YGBiVlZU2NjbDw8O5ubkTExM/Pz+sfe3nAAAEeUlEQVR4nO2a6VYiMRBGG9ltBUVRNhEQ9f3fcFyo6izVGaQjc86ce395qoukvyxVlbRFAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8twwuLselrug6GUZMjeWb/fFT94ie9n0qnZTLfXUSuF7br9vnG9xvpo0fX/KDmSuG13eRlf/DrCsPXSyj84M53nIp95lrvxdqtbN26Fstg1H5FYSTxolfrOvUcJ2ofVcZbNTrzU6uw1ZqcQeFVsMMSCoPRmIl5V9nuxOZOeELhyxkUtjrHK5x7njpfCzUNFmJzJyehsPV0BoX3xyts3Xqul2Lei0XjzLPrl1K4PoPCnr8Xkgr9+X6MXrMtFi+EpBT2ojTUTGF5KcyrTvyAJgp77+qrS8+fmqJ4F/thkHTd+jMjCq+s3v1l0VihE8In+nr+VhCFTgQa78Q1WNGvLb9djTN7z00UbpzeS3GN0tVpiMJrx6YD7i89UVi66VhGww81RbE82JdfwzGUFi99L1HYd2y6wjOFGkvh8Op4hTKJYXDveO+pcebB97IUFmdQqGHBfx9Tofz+PWhXs8NXXSMzXQZepkL55b7IgqlQCiw70pgKvQLtE92hH7HmRv4OMqytcGv2fjLmKi2rl3NIrtJN2PCoV7UshWqUAFKrtJfpiJGKNDUZ31P4UjvgEj63Q40z3dDHiKXF/mDLnfHvxno8u5U4WFO1lZPqcCgylnHLWn/vNepEZyJRuNPeB7eySF8zKzQof1B5W3FvdXg2kyw+jVwSNY0xZtkVhgsvofDOavom9BpFLvUK385weroOXesVzuMLgU/avtcq9qhX2I+dsyuMEkBqlZo15ONffRKr9Dn2zq4wXHvJs4UZ2peuR9twSJ0tdoZ/boXBqCcVmjvxyfWwCumUwlz3GEmFfvBLKuyZW3FbOdxbz5MKo+zZTGF70xemen5ZeAlMFG536tqtgslDqvW656Jw5vSuo5IpXxjnw2KgF39ewjDOh0XRF1czMgzf5PGLeWK3apqR7t48R2Cz8tZM5vZsV216JRMeLr7RAQhr7m/MujTzAdFUOJYDohc/bIXykqV5TS3334s427s/9hRqGZsnmpoKNVd7ocZWKA30TA2Dw9Olfa1kKtQkY8bnH5NW6G2uJgrD2+UDaYVxHXsKpsLhi9WHrVAOiG/ZFOoq/cU5nJh92ArXLcsqnKJQL8Ly7kMvverHo41rNbOFBj47lh6p0OtHv3rkjaXrToV2YefD7aZyrT4ARhc1P1G4cnpf2703Vmjj7a1k1VaT8I5UaLLI85k0qdC/KkkrtOvkJgqN82R2hfat/hGDkUVh5ttEi9O/ruVQeI6va8HCSymsC+wNFNp1Xk6Fb01vohop3P7+TdQqGsPa/8WY1ycuUVjaF9g1/23yUUzZd1un8HrfjllPN8YQDgzPdnvVfUx8rB0fmp/ZPh27906uFQoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwz/gDKxoxvnHk0lQAAAAASUVORK5CYII="
description = "BBYB는 BLANK BY BELLA의 약자로 다채로운 컬러와 다양한 소재로\n매 시즌 새롭고 유니크한 컨셉의 디자인을 선보입니다.\n이탈리아어로 '아름다운 여성'을 의미하는 벨라는\n'BBYB'가 추구하는 여성을 표현합니다.\n많은 여성들은 때로는 사랑스럽게, 때로는 아름답게, 때로는 시크하게\n자신의 개성을 드러내고 싶어합니다.\n적극적이면서 넓은 시야를 갖고 낡은 가치관에 구애 받지 않는\n새로운 라이프 스타일을 지향하는 여성들을 위해\n매 시즌 다양하고 독특한 BBYB만의 감성을 담은 벨라를 채워나갑니다."
brand["logo"] = logo
brand["description"] = description
temp_list.append(brand)

sells = soup.select('div.item-display > ul > li')
for idx, sell in enumerate(sells):
    if(idx >= 30):
        break
    item = dict()
    item["img"] = item_url + sell.select_one('img')['src']
    item["link"] = item_url + sell.select_one('a')['href'].replace('..','')
    item["name"] = sell.select_one('span.txt > strong').get_text().replace('\n','')
    item["price"] = sell.select_one('span.price').get_text().replace('\n','')
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