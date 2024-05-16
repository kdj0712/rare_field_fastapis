from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
webbrowser_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webbrowser_manager_directory))
# Chromebrowser 실행
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException    # Element : 웹요소 찾지 못할 때 / Window : 창이 없거나 찾을 수 없을 때
# Chrome Webbrowser의 capabilities 속성 사용
capabilities = browser.capabilities
from selenium.webdriver.common.by import By
from selenium import webdriver
# - 정보 획득
# from selenium.webbrowser.support.ui import Select      # Select : dropdown 메뉴 다루는 클래스
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003/")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona1_navercafe_rheumatism']

# 로그인 창
browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
time.sleep(2)

from dotenv import load_dotenv
import os
# 환경변수 불러오기
load_dotenv()
# 로그인 계정 불러오기
id = os.getenv('id')
pw = os.getenv('pw')


#자바스크립트로 우회하여 아이디와 비밀번호 값 넘겨줌
browser.execute_script("document.getElementsByName('id')[0].value = \'" + id + "\'") 
browser.execute_script("document.getElementsByName('pw')[0].value = \'" + pw + "\'")

browser.find_element(by=By.CSS_SELECTOR, value='.btn_login').click() #로그인 버튼 클릭
time.sleep(1)

browser.get('https://cafe.naver.com/friendshift/') # 네이버 카페 접속(강직성척추염연합회)
time.sleep(1)

browser.find_element(by=By.CSS_SELECTOR, value='#menuLink87').click() # 류마티스, 자가면역질환 게시판 클릭
time.sleep(1)


browser.switch_to.frame('cafe_main') #프레임 전환
time.sleep(1)

browser.find_element(by=By.CSS_SELECTOR, value='#main-area > div:nth-child(5) > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a.article').click() # 게시글 클릭
time.sleep(1)


while True:
    try :
        time.sleep(2)
        title=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').text # 글 제목 추출
        name=browser.find_element(by=By.CSS_SELECTOR, value='.nickname').text #작성자 추출
        date=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_header > div.WriterInfo > div.profile_area > div.article_info > span.date').text #작성일 추출
        contents=browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer > div > div.content.CafeViewer > div > div').text #글내용 추출
        num = browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > a > strong').text # 댓글 개수
        num = int(num)
        if num != 0:
            reply_list = []
            for j in range(num): 
                reply = browser.find_element(by=By.XPATH, value=f'/html/body/div/div/div/div[2]/div[2]/div[5]/ul/li[{j+1}]/div/div/div[2]/p/span').text
                reply_list.append(reply)
        else : 
            reply_list = ""

        print(reply_list)
                
    except :
        pass

    data={
    'cafe' : '강직성척추염연합회',  # 카페 이름
    'title' : title,
    'name' : name,
    'date' : date,
    'contents' : contents,
    'review' : reply_list
    }

    print(data)
    try :
        browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div.ArticleTopBtns > div.right_area > a.BaseButton.btn_next.BaseButton--skinGray.size_default').click() #다음글 버튼 클릭
    except :
        browser.find_element(by=By.CSS_SELECTOR, value='#app > div > div > div > div.guide_btns > a:nth-child(2) > span').click() # 회원 등급 제한 걸릴 시 '다음글 보기'버튼 클릭
    time.sleep(2)    
    

    collection.insert_one(data)



browser.close()