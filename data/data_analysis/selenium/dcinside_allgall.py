# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from pymongo import MongoClient

def dbconnect(collection) :
    mongoClient = MongoClient("mongodb://localhost:27017/")
    database = mongoClient["data_analysis"]
    collection = database[collection]
    return collection

#  기능 functioin : 한 업무에 종속성이 없는 것
#  uri에 의한 Browser 가져오기
def getBrowserFromURI(uri):
    webdriver_manager_directory = ChromeDriverManager().install()

    # ChromeDriver 실행
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # Chrome WebDriver의 capabilities 속성 사용
    capabilities = browser.capabilities

    # - 주소 입력(https://www.w3schools.com/)
    browser.get(uri)
    return browser



def scrapping(browser, current_cate, gall_name):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    # 게시물 리스트 : #idJiwonNm > option////
    element_post = browser.find_elements(by=By.CSS_SELECTOR, value="#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr.ub-content")

    for index in range(len(element_post)) :
        
        select_post = browser.find_element(by=By.CSS_SELECTOR, value=f"table > tbody > tr:nth-child({index+1})")
        cate = select_post.find_element(by=By.CSS_SELECTOR, value="td.gall_num").text
        if cate =='설문' or cate =='공지' or int(cate) >= current_cate :
            pass
        else :
            click = select_post.find_element(by=By.CSS_SELECTOR, value=f"td > a")
            click.click()
            time.sleep(2)
            dc_title = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > h3 > span.title_subject")
            dc_title_text = dc_title.text
            dc_name = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.nickname") 
            dc_name_text = dc_name.text
            dc_date = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.gall_date")
            dc_date_text = dc_date.text
            dc_contents = browser.find_element(by=By.CSS_SELECTOR, value="#container > section > article:nth-child(3) > div.view_content_wrap > div > div.inner.clear > div.writing_view_box > div.write_div")
            dc_contents_text = dc_contents.text
            collection.insert_one({"gall_name":gall_name, "title": dc_title_text, 'name': dc_name_text, 'date': dc_date_text, 'contents': dc_contents_text})
            print(f'현재 게시물 번호: {int(cate)}')
            browser.back()
            pass
    return int(cate)

def quitBrowser(browser):
    # 브라우저 종료
    browser.quit()
    return 0

if __name__ == "__main__" :
    collection = dbconnect('persona1_dcinside_agony')
    i = 65
    print(i)
    gall_list = ["https://gall.dcinside.com/mgallery/board/lists/?id=homeless", "https://gall.dcinside.com/mgallery/board/lists/?id=sosad", "https://gall.dcinside.com/mgallery/board/view/?id=adhd", "https://gall.dcinside.com/board/lists/?id=depression_new1", "https://gall.dcinside.com/board/lists/?id=loan_new1", "https://gall.dcinside.com/mgallery/board/lists/?id=gook", "https://gall.dcinside.com/mgallery/board/lists/?id=safetyreport", "https://gall.dcinside.com/mgallery/board/lists/?id=dsrqsv"]
    gall_name_list = ["노숙자 갤러리_마이너", "조울증 갤러리_마이너", "ADHD 갤러리_마이너", "우울증 갤러리", "대출갤러리", "국제사랑 갤러리_마이너", "안전신문고 갤러리_마이너", "배달대행 기사들 모임 갤러리_마이너"]
    current_cate = 10000000000000000
    for index in range(len(gall_list)) : 
            
        while True :
            try :
                current_cate = scrapping(getBrowserFromURI(uri=f"{gall_list[index]}&page={i}"), current_cate, gall_name_list[index])
                i = i+1
                pass
            except :
                print(f"현재 갤러리:{gall_list[index]} 현재 페이지: {i}")
                current_cate = scrapping(getBrowserFromURI(uri=f"{gall_list[index]}&page={i}"), current_cate, gall_name_list[index])