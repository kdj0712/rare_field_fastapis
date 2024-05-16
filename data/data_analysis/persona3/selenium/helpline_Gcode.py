## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['persona2_helpline_Gcode_details']
# insert 작업 진행
# 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


# Chrome 드라이버 설치 디렉터리 설정
# webdriver_manager_directory = ChromeDriverManager().install()

# Chrome 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# WebDriver 생성
browser = webdriver.Chrome()

# DB초기화
collection.delete_many({})

# 웹 페이지 열기  
# 크롤링할 웹 페이지 URL
for i in range(1, 13):
    url = f"https://helpline.kdca.go.kr/cdchelp/ph/rdiz/selectRdizInfList.do?menu=A0100&pageIndex={i}&fixRdizInfTab=&rdizCd=&schKor=&schEng=&schCcd=06&schGuBun=dizNm&schText=&schSort=kcdCd&schOrder=desc"
    html_source = browser.get(url)
    time.sleep(1)
    pagelist = browser.find_elements(by=By.CSS_SELECTOR,value="tr > td:nth-child(3) > a")
    
    # 질환정보 바로가기
    for j in range(len(pagelist)): 
        pagelist = browser.find_elements(by=By.CSS_SELECTOR,value="tr > td:nth-child(3) > a")
        pagelist[j].click()
        
        time.sleep(2)
        
        KCD_code = browser.find_element(by=By.CSS_SELECTOR,value="tbody > tr > td:nth-child(1)").text
        disease = browser.find_element(by=By.CSS_SELECTOR,value="table.listT2.help_list > tbody > tr > td.subject").text
        disease_KO = browser.find_element(by=By.CSS_SELECTOR,value="tbody > tr > td.subject > em").text
        
        affected_area = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(1) > td:nth-child(4)").text
        symptoms = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(2) > td:nth-child(2) > pre").text
        cause = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(2) > td:nth-child(4) > pre").text
        diagnostics = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(3) > td:nth-child(2) > pre").text
        treatment = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(3) > td:nth-child(4) > pre").text
        calculation_special_codes = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(4) > td:nth-child(2) > pre").text
        medical_assistance = browser.find_element(by=By.CSS_SELECTOR,value="#frm > div > table.dic_viewT > tbody > tr:nth-child(4) > td:nth-child(4) > pre").text
        
        disease_details_overview = browser.find_element(by=By.CSS_SELECTOR,value="#detail01 > dd").text
        disease_details_symptoms = browser.find_element(by=By.CSS_SELECTOR,value="#detail02 > dd").text
        disease_details_causes = browser.find_element(by=By.CSS_SELECTOR,value="#detail03 > dd").text
        disease_details_diagnosis = browser.find_element(by=By.CSS_SELECTOR,value="#detail04 > dd").text
        disease_details_treatment = browser.find_element(by=By.CSS_SELECTOR,value="#detail05 > dd").text
        disease_details_reference = browser.find_element(by=By.CSS_SELECTOR,value="#detail07 > dd").text

        # 페이지 내리기
        element_body = browser.find_element(by=By.CSS_SELECTOR,value='body')
        element_body.send_keys(Keys.END)
        time.sleep(1)
        back_button = browser.find_element(By.CSS_SELECTOR,value="p.btn_areaR.three > button")
        back_button.click()
        time.sleep(2)
        
    
        collection.insert_one({"KCD_code": KCD_code
                                , "disease": disease
                                , "disease_KO": disease_KO
                                , "affected_area": affected_area
                                , "symptoms": symptoms
                                , "cause": cause
                                , "diagnostics": diagnostics
                                , "treatment": treatment
                                , "calculation_special_codes": calculation_special_codes
                                , "medical_assistance": medical_assistance
                                , "disease_details_overview": disease_details_overview
                                , "disease_details_symptoms": disease_details_symptoms
                                , "disease_details_causes": disease_details_causes
                                , "disease_details_diagnosis": disease_details_diagnosis
                                , "disease_details_treatment": disease_details_treatment
                                , "disease_details_reference": disease_details_reference
                               })

pass