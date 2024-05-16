## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona1_kord_freeboard']
# insert 작업 진행
# 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time


# Chrome 드라이버 설치 디렉터리 설정
# webdriver_manager_directory = ChromeDriverManager().install()

# Chrome 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# WebDriver 생성
browser = webdriver.Chrome()

# DB초기화
# collection.delete_many({})

# 웹 페이지 열기  
# 크롤링할 웹 페이지 URL
for i in range(1, 184):
    url = f"https://www.kord.or.kr/bbs/board.php?bo_table=0605&page={i}"
    html_source = browser.get(url)
    for j in range(1, 16):
        try : 
            contents =  browser.find_element(By.CSS_SELECTOR,value=f"#fboardlist > div > table > tbody > tr:nth-child({j}) > td.td_subject > div.subj-content > a")
            contents.click()
            time.sleep(1)
            
            contents_title = browser.find_element(By.CSS_SELECTOR,value=f"#bo_v_title").text
            
            contents_writer = browser.find_element(By.CSS_SELECTOR,value=f"#bo_v_info > div.hidden-xs > strong:nth-child(1) > span").text
            
            contents_date = browser.find_element(By.CSS_SELECTOR,value=f"#bo_v_info > div.hidden-xs > strong:nth-child(3)").text
            
            click_count = browser.find_element(By.CSS_SELECTOR,value=f"#bo_v_info > div.hidden-xs > strong:nth-child(4)").text
            
            contents_text = browser.find_element(By.CSS_SELECTOR,value=f"#bo_v_con").text
            
            print(contents_title)
            print(contents_writer)
            print(contents_date)
            print(click_count)
            print(contents_text)

            browser.back()
        except : 
            pass    
        
        collection.insert_one({
            "contents_title": contents_title
            , "contents_writer":contents_writer
            , "contents_date":contents_date
            , "click_count": click_count
            , "contents_text": contents_text
            })

pass