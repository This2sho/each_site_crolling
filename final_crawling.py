import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
# pip install webdriver-manager, 크롬드라이버 업데이트 필요x
from webdriver_manager.chrome import ChromeDriverManager 


# 스크롤
def scrollMax(browser): 
    # 물품을 80개씩 보게되면 17500 높이를 가진다.
    # height = browser.execute_script("return document.body.scrollHeight") # 현재 문서 높이를 가져와서 저장
    for i in range(34):
        time.sleep(0.01) # 0.01초 로딩 대기는 안점함을 확인했다.
        browser.execute_script(f"window.scrollTo(0, {i*5}00)") # 스크롤을 가장 아래로 내림


def get_datas(soup, page):
    rank = 0
    datas = []
    for block in soup:
        rank += 1
        index = ""
        ad = ""
        review = ""
        buy = ""
        choice = ""
        page_rank = {}
        market_type = ""
        market = []
        img_src = ""
    

        try: # get index
            index = block.find('a', {'class': 'basicList_link__1MaTN'}).get_text()
        except AttributeError as e:
            print("index error")
        

        try: # get ad
            isAd = block.find('div', {'class': 'basicList_price_area__1UXXR'}).get_text()
            if '광고' in isAd:
                ad = "광고"
        except AttributeError as e:
            print("ad error")


        try: # get review, # get buy # 두개는 a tag로 이루어짐
            underline = block.find('div', {'class': 'basicList_etc_box__1Jzg6'})
            reviewAndBuy = underline.find_all('a', {'class': 'basicList_etc__2uAYO'})
            for rb in reviewAndBuy:
                if '리뷰' in rb.get_text(): # 리뷰가 있으면 
                    review = rb.find('em', {'class': 'basicList_num__1yXM9'}).get_text()
                elif '구매' in rb.get_text(): # 구매건수가 있으면
                    buy = rb.find('em', {'class': 'basicList_num__1yXM9'}).get_text()
        except AttributeError as e:
            print("review & buy error")
        

        try: # get choice # span 안에 button으로 되어있음
            choice = underline.find('button', {'class': 'basicList_btn_zzim__2MGkM'}).find('em', {'class': 'basicList_num__1yXM9'}).get_text()
        except AttributeError as e:
            print("choice error")
        

        try: # get page_rank [] 
            page_rank = {'page': page, 'rank': rank}
        except AttributeError as e:
            print("page_rank error")


        try: # get market_type, market []
            ul = block.find('ul', {'class': 'basicList_mall_list__vIiQw'})
            if ul: # bundle
                market_type = 'bundle'
                a_tags = ul.find_all('a', {'class': 'basicList_mall_item__tHbWj'})
                for a_tag in a_tags:
                    name = a_tag.find('span', {'class': 'basicList_mall_name__1XaKA'}).get_text()
                    title = a_tag.find('span', {'class': 'basicList_price__2r23_'}).get_text()
                    market.append({'name': name, 'title': title})
            else: # single
                market_type = 'single'
                name = block.find('a', {'class': 'basicList_mall__sbVax'}).get_text()
                title = block.find('span', {'class': 'price_num__2WUXn'}).get_text()
                market.append({'name': name, 'title': title})
        except AttributeError as e:
            print(f"market error {e}")


        try: # get img_src
            a_tag = block.find('a', {'class': 'thumbnail_thumb__3Agq6'})
            img_src = a_tag.find('img').get('src')
        except AttributeError as e:
            print(f"img_src attribute error {e}")


        dic = {"index": index, "ad": ad, "review": review, "buy": buy, "choice": choice, "page_rank": page_rank, "market_type": market_type, "market": market, "img_src": img_src}
        datas.append(dic)
    return datas


def gogo(): # main
    start = time.time()  # 시작 시간 저장
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1000x800")  # 해상도에 맞게 브라우져를 내부적으로 띄워서 실행
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.maximize_window()

    datas = []
    search_name = "디퓨저"  # 검색어
    for page in range(12): # 1~12 page
        page += 1 # index와 실제 페이지 간의 헷갈리지 않게 하는 +1 
        url = f"https://search.shopping.naver.com/search/all?query={search_name}&pagingSize=80&pagingIndex={page}"
        try: 
            browser.get(url)
            cur_url = browser.current_url
            if(re.search('nidlogin',cur_url) == None): # 19금 검색어 입력했을 때 제외 시킴
                scrollMax(browser)
                soup = BeautifulSoup(browser.page_source, "lxml")
                soup = soup.find_all('div', {'class': 'basicList_inner__eY_mq'}) # 아이템 블록 전부
                datas += get_datas(soup, page) # 데이터 가져오기
            print(f"{page}page 정상완료")    
        except:
            browser.quit()
            break
        
    # for data in datas : # 출력
    #     print(data) 
    print(datas)
    browser.quit()
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    return datas


if __name__ == "__main__":
    gogo() # return datas


# [
#     {
#         "index":"양키캔들 라운드 리드디퓨저 외 유명 디퓨저 모음전",
#         "ad":"광고",
#         "review":"34",
#         "buy":"149",
#         "choice":"122",
#         "page_rank":"[{'page':'1','rank':'1'}]",
#         "market_type":"single",
#         "market":"[{'name':'양키캔들 한국공식 쇼핑몰','title':'39,000'}]",
#         "img_src":"https://shopping-phinf.pstatic.net/main_8256978/82569781931.4.jpg?type=f140"
#     }
# ]

# [
#     {
#         "index":"쿤달 퍼퓸 디퓨저 200ml",
#         "ad":"",
#         "review":"1650",
#         "buy":"",
#         "choice":"199",
#         "page_rank":"[{'page':'1','rank':'4'}]",
#         "market_type":"bundle",
#         "market":"[{'name':'도토리 헬스케어','title':'16,500'},{'name':'쿤달 KUNDAL','title':'18,500'}]",
#         "img_src":"https://shopping-phinf.pstatic.net/main_2372660/23726605669.20210526145644.jpg?type=f140"
#     }
# ]
