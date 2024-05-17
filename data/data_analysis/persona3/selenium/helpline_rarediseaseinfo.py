## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona2_helpline_rarediseaseinfo']
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
for i in range(129):
    url = f"https://helpline.kdca.go.kr/cdchelp/ph/supbiz/selectMdepSupList.do?menu=B0102&pageIndex={i+66}&schGubun=tit&schSuplDcd=&schText="
    html_source = browser.get(url)
    for j in range(1, 11):
        time.sleep(1)
        num =  browser.find_element(By.CSS_SELECTOR,value=f"#frm > div > table > tbody > tr:nth-child({j}) > th").text
        
        raredisease_title = browser.find_element(By.CSS_SELECTOR,value=f"#frm > div > table > tbody > tr:nth-child({j}) > td > dl > dt").text
        raredisease_title_list = raredisease_title.split('\n')
        raredisease_title_KO = raredisease_title_list[0]
        raredisease_title_ENG = raredisease_title_list[1]
        
        KCD_code = browser.find_element(By.CSS_SELECTOR,value=f"#frm > div > table > tbody > tr:nth-child({j}) > td > dl > dd > ul > li:nth-child(1)").text
        KCD_code_list = KCD_code.split(' : ')
        KCD_code = KCD_code_list[1]
        
        special_calculation = browser.find_element(By.CSS_SELECTOR,value=f"#frm > div > table > tbody > tr:nth-child({j}) > td > dl > dd > ul > li:nth-child(2)").text
        special_calculation_list = special_calculation.split(' : ')
        special_calculation = special_calculation_list[1]
        
        support = browser.find_element(By.CSS_SELECTOR,value=f"#frm > div > table > tbody > tr:nth-child({j}) > td > dl > dd > ul > li:nth-child(3)").text
        support_list = support.split(' : ')
        support_text = []
        for x in range(len(support_list)):
            try : 
                support_num = support_list[x+1]
                support_text.append(support_num)
            except : 
                pass
        
        print(num)
        print(raredisease_title_KO)
        print(raredisease_title_ENG)
        print(KCD_code)
        print(special_calculation)
        print(support_text)
        pass    
    
        collection.insert_one({"num": num, "raredisease_title_KO":raredisease_title_KO, "raredisease_title_ENG":raredisease_title_ENG, "KCD_code": KCD_code, "special_calculation": special_calculation, "support_text": support_text})

pass