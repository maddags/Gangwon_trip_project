import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import requests
from scraper.models import Location, TouristsReview
#### selenium 3.141.0 version

def run():
    # driver 오류
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    url = "https://www.tripadvisor.co.kr/Attractions-g1072105-Activities-a_allAttractions.true-Gangwon_do.html"
    driver = webdriver.Chrome("C:\gitdoc\Gangwon_trip_project\chromedriver102.exe",options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    # get_urls = driver.find_elements_by_css_selector(".bMktZ div.MGdFu a")
    #url 리스트화
    #첫페이지
    # urls = []
    # for url in get_urls:
    #     urls.append(url.get_attribute("href"))
    #두번째 페이지 이후
    # for num in range(30, 727, 30):
    #     add_url = 'https://www.tripadvisor.co.kr/Attractions-g1072105-Activities-oa{num}-Gangwon_do.html'
    #     add_url = add_url.format(num=num)
    #     driver.get(add_url)
    #     get_urls = driver.find_elements_by_css_selector(".bMktZ div.MGdFu a")
    #     for url in get_urls:
    #         urls.append(url.get_attribute("href"))
    
        #장소 상세 페이지
    with open('./data/tripadvisor_urls.txt', 'r') as f:
        urls = f.read().splitlines()
    for url in urls:
        try: # try4 - 페이지 형식 다를 때 있음
            driver.get(url)
            driver.implicitly_wait(10)
            location = driver.find_element_by_css_selector("h1.WlYyy").text
            if Location.objects.filter(location_name = location).count() == 0:
                Location(location_name = location).save()

            try: #try1
                while True:
                    try: #try2
                        reviews = driver.find_elements_by_css_selector('div.dHjBB ._c')
                        for i in range(len(reviews)):
                            try: #try3 
                                selector = 'div.dHjBB > div:nth-child({i}) > span > div > '.format(i=i+1)
                                rate = driver.find_element_by_css_selector(selector + 'div:nth-child(2) svg').get_attribute('aria-label')
                                rate = rate[8:]
                                date = driver.find_element_by_css_selector(selector + '.fxays div:nth-last-child(2)').text
                                date = date.split(' ')
                                year = date[0].strip('년')
                                month = '0' + date[1].strip('월')
                                month = month[-2:]
                                day = '0' + date[2].strip('일')
                                day = day[-2:]
                                date = year+month+day
                                try:
                                    #이 부분에서 걸리면 너무 버벅거려서 최적화 필요해보임
                                    member = driver.find_element_by_css_selector(selector + '.eRduX').text.split(' • ')
                                    member = member[1]
                                except:
                                    member = ''
                                    pass
                                summury = driver.find_element_by_css_selector(selector + '.WlYyy').text
                                review = driver.find_element_by_css_selector(selector + '._T')
                                review.click()
                                review = review.text.rstrip('덜 보기')
                                review_text = summury + ' ' + review
                                TouristsReview(location_name=location, rate=rate, date=date, member=member, review = review_text).save()
                            except Exception as e:
                                loc = url.split('Reviews')
                                loc = loc[1].replace('.html', '')
                                f = open("./error.txt", 'a')
                                error_type = f'try 3 exception - {loc} : {e}\n'
                                f.write(error_type)
                                f.close()
                                continue
                    except Exception as e:
                        loc = url.split('Reviews')
                        loc = loc[1].replace('.html', '')
                        f = open("./error.txt", 'a')
                        error_type = f'try 2 exception - {loc} : {e}\n'
                        f.write(error_type)
                        f.close()
                        pass
                    toNext = driver.find_elements_by_css_selector('.cCnaz .eRhUG')
                    toNext[0].click()
                    driver.implicitly_wait(10)
                    time.sleep(1)
            except Exception as e:
                loc = url.split('Reviews')
                loc = loc[1].replace('.html', '')
                f = open("./error.txt", 'a')
                error_type = f'try 1 exception - {loc} : {e}\n'
                f.write(error_type)
                f.close()
                continue
        except Exception as e:
            loc = url.split('Reviews')
            loc = loc[1].replace('.html', '')
            f = open("./error.txt", 'a')
            error_type = f'try 4 exception - {loc} : {e}\n'
            f.write(error_type)
            f.close()
            continue
    print('end')
    driver.quit()