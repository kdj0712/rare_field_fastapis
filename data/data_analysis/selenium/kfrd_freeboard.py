## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona1_kfrd_freeboard']
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
for i in range(1, 11):
    url = f"https://www.kfrd.org/board/list.asp?page={i}&boardcd=104"
    html_source = browser.get(url)
    for j in range(1, 11):
        time.sleep(1)
        contents =  browser.find_elements(By.CSS_SELECTOR,value=f"#wrap > div.container > div.contents > div.cont > div.board > table > tbody > tr:nth-child({j}) > td.b_tit > a")
        contents.click()
        
        contents_title = browser.find_element(By.CSS_SELECTOR,value=f"#wrap > div.container > div.contents > div.cont > div > table > thead > tr > th").text
        
        contents_writer = browser.find_element(By.CSS_SELECTOR,value=f"#wrap > div.container > div.contents > div.cont > div > table > tbody > tr:nth-child(1) > td.b_tit3.b_line").text
        contents_writer_list = contents_writer.split(' : ')
        contents_writer = contents_writer_list[1]
        
        contents_date = browser.find_element(By.CSS_SELECTOR,value=f"#wrap > div.container > div.contents > div.cont > div > table > tbody > tr:nth-child(1) > td:nth-child(2)").text
        contents_date_list = contents_date.split(' : ')
        contents_date = contents_date_list[1]
        
        contents_text = browser.find_element(By.CSS_SELECTOR,value=f"#wrap > div.container > div.contents > div.cont > div > table > tbody > tr:nth-child(2) > td").text
        
        print(contents_title)
        print(contents_writer)
        print(contents_date)
        print(contents_text)

        pass    
    
        # collection.insert_one({"num": num, "raredisease_title_KO":raredisease_title_KO, "raredisease_title_ENG":raredisease_title_ENG, "KCD_code": KCD_code, "special_calculation": special_calculation, "support_text": support_text})

pass