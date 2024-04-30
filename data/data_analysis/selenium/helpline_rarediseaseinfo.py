## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['selenium_helpline_rarediseaseinfo']
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
url = f"https://helpline.kdca.go.kr/cdchelp/ph/supbiz/selectMdepSupList.do?menu=B0102&pageIndex={i+1}&schGubun=tit&schSuplDcd=&schText="
html_source = browser.get(url)
first_content = browser.find_element(By.CSS_SELECTOR,value="#search-results > section > div.search-results-chunks > div > article:nth-child(6) > div.docsum-wrap > div.docsum-content > a")
first_content.click()
while True:
    heading_title = browser.find_element(By.CSS_SELECTOR,value='.heading-title')
    title = heading_title.text
    try: 
        browser.find_element(By.CSS_SELECTOR,value='#abstract')
        abstract = browser.find_element(By.CSS_SELECTOR,value='#abstract')
        abstract_text = abstract.text
        abstract_text = ''
    abstract_list = abstract_text.split('\n')
    try:
        artical_date = browser.find_element(By.CSS_SELECTOR,value='.cit').text
        artical_date_list = artical_date.split(';')
        artical_date_list = artical_date_list[0].split(':')
        artical_date = artical_date_list[0]
    except:
        artical_date = ''
    print(title)
    print(artical_date)
    print(abstract_list)
    collection.insert_one({"title": title,"artical_date":artical_date,"abstract_list":abstract_list})
    time.sleep(2)
    next_btn = browser.find_element(By.CSS_SELECTOR,value='div.next.side-link.visible > a')
    next_btn.click()
    time.sleep(2)
pass