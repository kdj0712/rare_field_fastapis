## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona1_behcet_freeboard']
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
url = "https://www.behcet.co.kr/login?url=https%3A%2F%2Fwww.behcet.co.kr%2F"
html_source = browser.get(url)

# 로그인 정보
id = "tm2372"
pw = "rladbwls91"

# 자유게시판 들어가기 & 로그인 시도
element_login_field = browser.find_element(by=By.CSS_SELECTOR, value="#flogin > div.login-form > div:nth-child(1) > div > input")
element_login_field.send_keys(id)

element_password_field = browser.find_element(by=By.CSS_SELECTOR, value="#flogin > div.login-form > div:nth-child(2) > div > input")
element_password_field.send_keys(pw)

element_login_button = browser.find_element(by=By.CSS_SELECTOR, value = "#flogin > div.login-form > button")
element_login_button.click()
time.sleep(1)

# 크롤링할 웹 페이지 URL
free_board = browser.find_element(By.CSS_SELECTOR,value="body > div > div.container > section > div.main__side > section.main__side-board.news > ul > li:nth-child(2) > a")
free_board.click()
time.sleep(1)

first_content = browser.find_element(By.CSS_SELECTOR,value="#fboardlist > table > tbody > tr:nth-child(2) > td.list-title.board__title > a")
first_content.click()
time.sleep(1)

while True: 
    try:
        contents_title = browser.find_element(By.CSS_SELECTOR,value="body > div > div.container > section > div > div > div > ul > h3").text
        contents_writer = browser.find_element(By.CSS_SELECTOR,value="body > div > div.container > section > div > div > div > ul > ul > li:nth-child(1) > span").text
        contents_date = browser.find_element(By.CSS_SELECTOR,value="body > div > div.container > section > div > div > div > ul > ul > li:nth-child(4) > span").text
        click_count = int(browser.find_element(By.CSS_SELECTOR,value="body > div > div.container > section > div > div > div > ul > ul > li.post-view > span").text)
        contents_text = browser.find_element(By.CSS_SELECTOR,value="#post-content").text

        reply_num = browser.find_element(By.CSS_SELECTOR,value="body > div > div.container > section > div > div > div > ul > ul > li:nth-child(2) > span").text
        reply_num = int(reply_num)
        reply_list = []
        for i in range(1, reply_num+1):
            try:
                reply = browser.find_element(By.XPATH,value=f"/html/body/div/div[2]/section/div/div/div/div[4]/div[{i+1}]").text
                reply_list.append(reply)
            except:
                pass
            time.sleep(1)   

        # 다음글 버튼 클릭
        next_button = browser.find_element(By.CSS_SELECTOR,value="div > div > a.btn.btn-default.btn-sm.btn-next").click()
                
        collection.insert_one({
            "contents_title": contents_title
            , "contents_writer":contents_writer
            , "contents_date":contents_date
            , "click_count": click_count
            , "contents_text":contents_text
            , "reply_list":reply_list
            })
    except : 
        break