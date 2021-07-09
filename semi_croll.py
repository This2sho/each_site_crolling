from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 키보드 입력할 때 사용
import json
import time
import re

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

def getRelateTerms(browser):
    relate_terms = []
    soup = BeautifulSoup(browser.page_source, "lxml")
    try:
        elems = soup.find("div", attrs={"class":"relatedTags_relation_srh__1CleC"}).find_all("li")
    except AttributeError as e:
        print("관련 검색어가 없습니다.")
        return []
    for elem in elems:
        relate_terms.append(elem.get_text())
    return relate_terms

def getSuggestTerms(browser):
    suggest_terms = []
    elem = browser.find_element_by_class_name("searchInput_search_input__1Eclz")
    elem.click()
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "lxml")
    try:
        elems = soup.find("div", attrs={"class":"autoComplete_basis_result__39ATc autoComplete_active__3HkBd"}).find_all("li")
    except AttributeError as e:
        print("추천 검색어가 없습니다.")
        return []

    for elem in elems:
        suggest_terms.append(elem.get_text())
    return suggest_terms

def getUrlList(browser):
    url_list = []
    soup = BeautifulSoup(browser.page_source, "lxml")
    elems = soup.find_all("a", attrs={"class":"thumbnail_thumb__3Agq6"})
    for elem in elems:
        url_list.append(elem["href"])
    return url_list

def getTags(browser):
    tag_list = []
    for elem in url_list:
        browser.get(elem)
        Scroll_max(browser)
        soup = BeautifulSoup(browser.page_source, "lxml")
        try:
            tags = soup.find_all("li", attrs={"class":"_2RkVi-H2ze N=a:itm.tag"})
        except AttributeError as e:
            print("tag가 없습니다.")
            return []
        for tag in tags:
            tag_list.append(tag.get_text())
    return tag_list   




# def Test_json(name, list):
#     data = dict()
#     data[name] = list
#     with open("test_fun.json", "w", encoding="utf-8") as make_file:
#         json.dump(data, make_file, indent="\t", ensure_ascii=False)


# def Save_json(file_name, name, list):
#     with open(file_name, 'r', encoding="utf-8") as f:
#         read_data = json.load(f)
#     read_data[name] = list
#     with open(file_name, "w", encoding="utf-8") as make_file:
#         json.dump(read_data, make_file, indent="\t",ensure_ascii=False)

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("windw-size=1902x1080") # pc해상도 설정
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

search_name = "아이폰"  # 검색어
url = f'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={search_name}&pagingIndex=1&pagingSize=40&productSet=checkout&query={search_name}&sort=rel&timestamp=&viewType=list'
browser.get(url)
cur_url = browser.current_url
print(re.search('nidlogin',cur_url))
if(re.search('nidlogin',cur_url) == None): # 19금 검색어 입력했을 때 제외 시킴
    Scroll_max(browser)
    url_list = getUrlList(browser)
    # 가져와야 할 것 
    # 연관 검색어
    # 추천 검색어
    # 테그 
    relate_terms = getRelateTerms(browser)
    suggest_terms = getSuggestTerms(browser)
    tag_list = getTags(browser)

    print(len(url_list))
    print(relate_terms)
    print(suggest_terms)
    print(tag_list)
browser.quit()
    


# # 잘 써졌는지 확인용
# Test_json(name, temp_list)

# 파일 쓰기 test보고 잘 됐으면 ㄱㄱ
# 저장된 파일에 추가하기
# 저장할 파일 설정
# file_name = "data.json"
# Save_json(file_name, name, temp_list)
# browser.quit()

print("완료")