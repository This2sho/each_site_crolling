import time
import re
from typing import Type
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 키보드 입력할 때 사용
# pip install webdriver-manager, 크롬드라이버 업데이트 필요x
from webdriver_manager.chrome import ChromeDriverManager 


# 무한 스크롤
# def scrollMax(browser): 
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # interval = 1 # 1초에 한번씩 스크롤 내림
    # prev_height = browser.execute_script("return document.body.scrollHeight")
    # curr_height = 0
    # print(f"이전 높이: {prev_height}")
    # # 반복 수행
    # while (curr_height != prev_height):
    #     # 스크롤 가장 아래로 내림
    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2 )")
    #     # 페이지 로딩 대기
    #     time.sleep(interval)
    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2 + 100 )")
    #     # 현재 문서 높이를 가져와서 저장
    #     curr_height = browser.execute_script("return document.body.scrollHeight")
    #     print(f"현재 높이: {curr_height}")
    #     prev_height = curr_height

    # print("스크롤 완료")
    
def doScrollDown(browser, whileSeconds):
    start = browser.datetime.now()
    end = start + browser.timedelta(seconds=whileSeconds)
    while True:
        time.sleep(1)
        if browser.datetime.now() > end:
            break


# def get_bundle_list(link):
#     options = webdriver.ChromeOptions()
#     options.headless = True
#     options.add_argument("window-size=1920x1080")  # 해상도에 맞게 브라우져를 내부적으로 띄워서 실행
#     browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     browser.get(link)
#     soup = BeautifulSoup(browser.page_source, "lxml")
#     market_list = []
#     try: 
#         table = soup.find('table', {'class': 'productByMall_list_seller__2-bzE'})
#         trs = table.find_all('tr')
#         for tr in trs[1:]: # header row는 제외
#             if tr.find('a', {'class': 'productByMall_mall__1ITj0'}).get_text() != "":
#                 name = tr.find('a', {'class': 'productByMall_mall__1ITj0'}).get_text()
#             else:
#                 name = tr.find('img')['alt']
#             title = tr.find('td', {'class': 'productByMall_price__3F_YF'}).find('em').get_text()
#             market_list.append({'name': name, 'title': title})
#     except AttributeError as e:
#         print(f"get_bundle_list {e}")
#     finally:
#         browser.quit()
#     return market_list

# # 이미지 못들고 오는 경우가 존재해서 직접 들어가서 큰 이미지를 불러온다.
# def get_img_src(link): 
#     options = webdriver.ChromeOptions()
#     options.headless = True
#     options.add_argument("window-size=1920x1080")  # 해상도에 맞게 브라우져를 내부적으로 띄워서 실행
#     browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     browser.get(link)
#     soup = BeautifulSoup(browser.page_source, "lxml")
#     try: 
#         img_src = soup.find('div', {'class': 'image_thumb__20xyr'}).find('img').get('src')
#     except:
#         img_src = soup.find('div', {'class': '_23RpOU6xpc'}).find('img').get('src')
#     finally:
#         browser.quit()
#     return img_src


# def get_datas(soup, page):
#     img_error_count = 0
#     rank = 0
#     datas = []
#     for block in soup:
#         rank += 1
#         index = ""
#         ad = ""
#         review = ""
#         buy = ""
#         choice = ""
#         page_rank = {}
#         market_type = ""
#         market = []
#         img_src = ""
    

#         try: # get index
#             index = block.find('a', {'class': 'basicList_link__1MaTN'}).get_text()
#         except AttributeError as e:
#             print("index error")
        

#         try: # get ad
#             isAd = block.find('div', {'class': 'basicList_price_area__1UXXR'}).get_text()
#             if '광고' in isAd:
#                 ad = "광고"
#         except AttributeError as e:
#             print("ad error")


#         try: # get review, # get buy # 두개는 a tag로 이루어짐
#             underline = block.find('div', {'class': 'basicList_etc_box__1Jzg6'})
#             reviewAndBuy = underline.find_all('a', {'class': 'basicList_etc__2uAYO'})
#             for rb in reviewAndBuy:
#                 if '리뷰' in rb.get_text(): # 리뷰가 있으면 
#                     review = rb.find('em', {'class': 'basicList_num__1yXM9'}).get_text()
#                 elif '구매' in rb.get_text(): # 구매건수가 있으면
#                     buy = rb.find('em', {'class': 'basicList_num__1yXM9'}).get_text()
#         except AttributeError as e:
#             print("review & buy error")
        

#         try: # get choice # span 안에 button으로 되어있음
#             choice = underline.find('button', {'class': 'basicList_btn_zzim__2MGkM'}).find('em', {'class': 'basicList_num__1yXM9'}).get_text()
#         except AttributeError as e:
#             print("choice error")
        

#         try: # get page_rank [] 
#             page_rank = {'page': page, 'rank': rank}
#         except AttributeError as e:
#             print("page_rank error")


        # try: # get market []
        #     bundle = block.find_all('a', {'class': 'basicList_mall_item__tHbWj'})
        #     basic_list = block.find('div', {'class': 'basicList_mall_area__lIA7R'})
        #     if bundle: # bundle
        #         market_type = 'bundle'
        #         link = basic_list.find('a')['href']
        #         market = get_bundle_list(link) # 여기서 오래걸림
        #     else: # single
        #         market_type = 'single'
        #         name = block.find('a', {'class': 'basicList_mall__sbVax'}).get_text()
        #         title = block.find('span', {'class': 'price_num__2WUXn'}).get_text()
        #         market.append({'name': name, 'title': title})
        # except AttributeError as e:
        #     print("market error")


        # try: # get img_src
        #     a_tag = block.find('a', {'class': 'thumbnail_thumb__3Agq6'})
        #     img_src = a_tag.find('img').get('src')
        # except AttributeError as e:
        #     print(f"img_src attribute error {e}")
        #     img_error_count += 1
        #     img_src = get_img_src(a_tag.get('href'))

        # print(page_rank)
        # print(img_src)

    #     print(page_rank)
    #     try: 
    #         a_tag = block.find('a', {'class': 'thumbnail_thumb__3Agq6'})
    #         img_src = a_tag.find('img').get('src')
    #     except AttributeError as e:
    #         print(f"img_src attribute error {e}")



    #     dic = {"index": index, "ad": ad, "review": review, "buy":buy, "choice": choice, "page_rank": page_rank, "market_type": market_type, "market": market, "img_src": img_src}  
    #     datas.append(dic)
    # print(f"img_error_count: {img_error_count}")
    # return datas


# main
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("window-size=1920x1080")  # 해상도에 맞게 브라우져를 내부적으로 띄워서 실행
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.maximize_window()

datas = []
search_name = "디퓨저"  # 검색어
page_size = 20
for page in range(1,2): # 1~10 page
    url = f"https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery={search_name}&pagingIndex={page}&pagingSize={page_size}&productSet=total&query={search_name}&sort=rel&timestamp=&viewType=list"
    # url = f"https://search.shopping.naver.com/search/all?query={search_name}&pagingIndex={page}"
    try: 
        browser.get(url)
        cur_url = browser.current_url
        if(re.search('nidlogin',cur_url) == None): # 19금 검색어 입력했을 때 제외 시킴
            doScrollDown(browser, 10)
            soup = BeautifulSoup(browser.page_source, "lxml")
            items = soup.find_all('div', {'class': 'basicList_inner__eY_mq'}) # 아이템 블록 전부
            for idx, item in enumerate(items) :
                print(f'{idx+1}번째 아이템 주소 : {item.find("img")["src"]}')
                print("\n")
        print(f"{page}page 정상완료")    
    except:
        browser.quit()
        break
    
browser.quit()