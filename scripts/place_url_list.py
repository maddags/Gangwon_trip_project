import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import response
import time
import pandas as pd
import json

with open('./Gangwon_trip_project/config.json', 'r') as f:
    config = json.load(f)

# driver 오류
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# URL 설정
search = "강원도"
url = "https://kr.trip.com/global-search/searchlist/search/?keyword={search}&from=home"
url = url.format(search=search)

# URL 접속
# 왕경훈 : 
# 진수현 : 
# 한호 : C:/Users/madda/.ssh/project_3/chromedriver.exe
driver = webdriver.Chrome(config["Chromedriver"],options=options)
driver.get(url)


# 크롤링할 정보 들어가기
driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[3]/div/ul/li[3]').click()
time.sleep(2)

# 장소 목록
page = driver.find_elements_by_css_selector("ul.gl-cpt-pager > li")
page_cnt = int(page[-1].text)
place_url_list = []
for page in range(page_cnt):
    places_url = driver.find_elements_by_css_selector("div.gl-search-result_list > div.content > div.gl-search-result_list-content > div > a")
    for place in places_url:
        place_url =place.get_attribute("href")
        place_url_list.append(place_url)
    driver.find_element_by_css_selector("div.gl-search-result_page > div > button.btn-next").send_keys(Keys.ENTER)
    time.sleep(2)

place_url_list = pd.DataFrame(place_url_list, columns = ["URL"])
place_url_list.to_csv("../data/tripcom_place_url_list.csv", index = False)

# 데이터 저장
score_list = []                # 리뷰 평점 
score_date_list = []       # 리뷰 작성일
coment_list = []            # 리뷰(원문)
coment_trans_list = []  # 리뷰(번역)
place_list = []                # 장소
place_type_list = []       # 장소 분류
bnt_list = []                   # 운영시간
rcm_time_list = []         # 추천관광시간
address_list = []            # 주소


# 페이지 들어가기
for place in place_url_list:
    driver.get(place)
    time.sleep(2)

    # 장소
    place_css = driver.find_element_by_css_selector("h1.basicName")

    # 장소 분류
    place_type_css = driver.find_elements_by_css_selector("div.gl-poi-detail_tags > span")

    # 운영시간
    bnt_css = driver.find_element_by_xpath('//*[@id="poi.detail.overview"]/div/div[2]/div/div[3]/div[1]/div[1]/div/span[2]')

    # 관광 추천시간
    rcm_time_css = driver.find_element_by_xpath('//*[@id="poi.detail.overview"]/div/div[2]/div/div[3]/div[1]/div[2]/div/span[2]')

    # 주소
    address_css = driver.find_element_by_xpath('//*[@id="poi.detail.overview"]/div/div[2]/div/div[3]/div[1]/div[3]/div[1]/div/div/div/div/span[1]')
    # 평점,평점 작성일
    # score_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > span')
    
    # 리뷰
    # coment_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a')

    # 리뷰 번역
    # coment_trans_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a > p')
    
    # 데이터 수집
    ## 장소
    place_list.append(place_css.text)

    ## 장소 분류
    place_types = []
    for type in place_type_css:
        place_types.append(type.text)
    place_type_list.append(place_types)

    ## 운영시간
    bnt_list.append(bnt_css.text)
    
    ## 관광 추천시간
    rcm_time_list.append(rcm_time_css.text)
    
    ## 주소 
    address_list.append(address_css.text)


    # 리뷰 page만큼 for문 돌리기
    review_page_filter = driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/div/div/div/ul/li[5]').text
    if review_page_filter == "...":
        review_page = driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/div/div/div/ul/li[6]').text
        review_page = int(review_page)-1
        print(review_page)
    elif review_page_filter == "5":
        review_page = driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/div/div/div/ul/li[5`]').text
        
        # review_page = driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/div/div/div/ul/li[6]').text
        # review_page = int(review_page)-1
        # print(review_page)

            

    for page in range(review_page):
        score_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > span.review_score')
        date_css = driver.find_elements_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/ul/div[1]/li/div[2]/div[3]/span/span')
        coment_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a')
        coment_trans_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a > p')


        ## 리뷰 평점,작성일
        for point in score_css:
            score = point.text
            score_list.append(score)
        
        for point in date_css:
            date = point.text
            date = date.split(" ")
            print(date)
            date = date[1] + date[2] + date[3]
            score_date_list.append(date)


        ## 리뷰(원문)
        for place in coment_css :
            coment = place.get_attribute("alt")
            coment_list.append(coment)


        ## 리뷰(번역)
        for place in coment_trans_css:
            coment_trans = place.text
            coment_trans_list.append(coment_trans)
        
        print(coment_trans_list)
        if page < (review_page-1):
            driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/div/div/div/button[2]').send_keys(Keys.ENTER)
            time.sleep(1)




    info_table = [place_list,place_type_list,bnt_list,rcm_time_list,address_list]
    info_table = pd.DataFrame(info_table).T
    info_table.columns = ["장소","분류","운영시간","관광추천시간","주소"]
    print(info_table)

    review_table = [score_list,score_date_list,coment_list,coment_trans_list]
    review_table = pd.DataFrame(review_table).T
    review_table.columns = ["평점","작성일","리뷰(원문)","리뷰(번역)"]

    print(review_table)

