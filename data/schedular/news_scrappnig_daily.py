
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import os
from konlpy.tag import Okt
import pickle
from datetime import datetime



# 몽고 디비 연결
def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://trainings.iptime.org:45003/")
    database = mongoClient["teamkim"]
    collection = database[collection]
    return collection

# 날짜 바꾸기
def convert_to_datetime(orgin_str):
    current_datetime = datetime.now()
    news_datetime = datetime.strptime(orgin_str, "%m.%d %H:%M")
    current_year = current_datetime.year
    news_datetime = news_datetime.replace(year=current_year)
    return news_datetime

# 뉴스 스크래핑

def bosascrapping(browser_name, keyword) :

    bosa_news_coll = dbconnect('news_weekly')
    # bosa_news_coll.delete_many({})

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 현재 날짜 설정
    from datetime import datetime, timedelta
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    one_week_date = current_date - timedelta(days=10)
    current_date = current_date.strftime('%Y-%m-%d')
    one_week_date = one_week_date.strftime('%Y-%m-%d')

    ## 상세검색
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(browser_name)
    browser.find_element(By.CSS_SELECTOR, "div.user-etc > div.search-list > span > a").click() # 상세 검색
    time.sleep(1)
    new_tab = browser.window_handles[-1]
    browser.switch_to.window(new_tab)

    browser.find_element(By.CSS_SELECTOR, "#sc_sdate").clear()
    browser.find_element(By.CSS_SELECTOR, "#sc_sdate").send_keys(one_week_date)
    browser.find_element(By.CSS_SELECTOR, "#sc_edate").clear()
    browser.find_element(By.CSS_SELECTOR, "#sc_edate").send_keys(current_date)
    browser.find_element(By.CSS_SELECTOR, "#sc_word").send_keys(keyword)
    browser.find_element(By.CSS_SELECTOR, "#search-tabs1 > form > footer > div > button").click()
    browser.find_element(By.CSS_SELECTOR, "header > div > div > a:nth-child(2)").click() # 요약형
    time.sleep(2)
    ## 스크래핑
    contents = browser.find_elements(By.CSS_SELECTOR, "#section-list > ul > li")
    for index in range(len(contents)) :
        contents = browser.find_elements(By.CSS_SELECTOR, "#section-list > ul > li")
        try : 
            try :
                news_title = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > h4 > a").text
                news_url = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li> h4 > a").get_attribute("href")
                news_when_orgin = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > span > em:nth-child(3)").text
            except :
                news_title = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > div > h4 > a").text
                news_url = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > div > h4 > a").get_attribute("href")
                news_when_orgin = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > div > span > em:nth-child(3)").text
            try : 
                news_image = contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > a > img").get_attribute('src')
            except NoSuchElementException :
                news_image = ' '
                pass
            try : 
                contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li> h4 > a").click() # 안으로 들어가기
            except :
                contents[index].find_element(By.CSS_SELECTOR, "#section-list > ul > li > div > h4 > a").click() # 안으로 들어가기

            news_contents = ''
            news_contents_p = browser.find_elements(By.CSS_SELECTOR, "#article-view-content-div > p")
            for news_p in news_contents_p :
                news_contents += f'<p>{news_p.text}</p>'
            
            # 날짜 형식 맞춰주기
            news_datetime = datetime.strptime(news_when_orgin, '%Y.%m.%d %H:%M')
            
            bosa_news_coll.insert_one({"news_title" : news_title
                                    , "news_datetime" : news_datetime
                                    ,"news_contents":news_contents
                                    ,"news_url":news_url
                                    , "news_image" : news_image
                                     ,'news_paper' : "의학신문" })
            browser.back()
            time.sleep(1)
        except StaleElementReferenceException :
            print("StaleElementReferenceException 발생. 다음 요소로 넘어갑니다")
            continue
    
def thevoicescrapping(browser_name, keyword) :
    thevoice_news_all = dbconnect('news_weekly_thevoice')
    
    # 실제 사용할 때 꼭 지울 것
    thevoice_news_all.delete_many({})

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 현재 날짜 설정
    from datetime import datetime, timedelta
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    one_week_date = current_date - timedelta(days=10)
    current_date = current_date.strftime('%Y-%m-%d')
    one_week_date = one_week_date.strftime('%Y-%m-%d')

    # 상세검색
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(browser_name)
    browser.find_element(By.CSS_SELECTOR, "#search").send_keys(keyword)
    browser.find_element(By.CSS_SELECTOR, "fieldset > form > button").click()
    time.sleep(2)
    
    # 스크래핑
    contents = browser.find_elements(By.CSS_SELECTOR,"div.article-list > section > div")
    for index in range(len(contents)):
        try :
            news_title = browser.find_element(By.CSS_SELECTOR, "div.article-list > section > div > div.list-titles > a").text
            news_url = contents[index].find_element(By.CSS_SELECTOR, "div > div.list-titles > a").get_attribute("href")
        except NoSuchElementException :
            pass
        try : 
            # contents[index].find_element(By.CSS_SELECTOR, "div > div.list-titles > a > strong").click()
            link_element = contents[index].find_element(By.CSS_SELECTOR, "div > div.list-titles > a")
            link_url = link_element.get_attribute("href")
            browser.execute_script(f"window.open('{link_url}', '_blank');")
            new_tab = browser.window_handles[-1]
            browser.switch_to.window(new_tab)
            # 페이지 안에서 구하기
            news_datetime_first = browser.find_element(By.CSS_SELECTOR, "section > div > ul > li:nth-child(2)")[0].text
            date_str = news_datetime_first.split()[1]
            news_datetime = datetime.strptime(date_str, '%Y.%m.%d')
            try : 
                news_image = browser.find_element(By.CSS_SELECTOR, "#article-view-content-div > div > figure > img").get_attribute('src')
            except NoSuchElementException :
                news_image = ''
            news_contents =''
            news_contents_p = browser.find_elements(By.CSS_SELECTOR, "#article-view-content-div > p")
            for news_p in news_contents_p:
                news_contents += f'<p>{news_p.text}</p>'
        except NoSuchElementException:
            news_title = 'none'
            news_datetime = 'none'
            news_contents = 'none'
        thevoice_news_all.insert_one({"news_title" : news_title
                                    , "news_datetime" : news_datetime
                                    ,"news_contents":news_contents
                                    ,"news_url":news_url
                                    , "news_image" : news_image
                                     ,'news_paper' : "뉴스더보이스" })
        browser.close()
        time.sleep(1)
    return

# bosascrapping("http://www.bosa.co.kr/", "희귀질환")
thevoicescrapping("http://www.newsthevoice.com/", "희귀질환")
pass
