from fastapi import APIRouter,Request, Query
from typing import Optional, Any, List, Dict
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.responses import HTMLResponse
from aiohttp import ClientSession
from pydantic import BaseModel
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.paginations import Paginations
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import storage
import urllib.parse
import pandas as pd
import requests
import pickle
import os
import sys

load_dotenv()
pubapi_key = os.getenv("PUBLIC_API_KEY")
api_key = os.getenv("API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/teamKim/macro-atom-415806-fd4035d471e1.json"
router = APIRouter()

from fastapi.staticfiles import StaticFiles
router.mount("/data/csv", StaticFiles(directory="data/csv/"), name="static_csv")

from database.connection import Database
from models.info_rarediseases import diseases
collection_disease = Database(diseases)

from models.institution import Institutions
collection_institution = Database(Institutions)

from models.trend_news import news_trends
collection_trend = Database(news_trends)

from models.academicinfo import academicinfo
collection_academicinfo = Database(academicinfo)

from models.info_academicinfo import info_academicinfo_Riss,info_academicinfo_eng

collection_info_academicinfo_Riss = Database(info_academicinfo_Riss)
collection_info_academicinfo_eng = Database(info_academicinfo_eng)


templates = Jinja2Templates(directory="templates/")
### 검색 모델 적용 조건---------------------------------------------------------------------------------------
def load_pickle_from_gcs(bucket_name, file_name):
    """Google Cloud Storage에서 피클 파일을 로드합니다."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    pickle_data = blob.download_as_bytes()
    return pickle.loads(pickle_data)
bucket_name = 'savehomes'
file_name = 'search_symptoms.pkl'
# vectorizer = load_pickle_from_gcs(bucket_name, file_name)

with open('data/pkl/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

with open('data/pkl/tfidf_matrix_symptoms.pkl', 'rb') as file:
    tfidf_matrix_symptoms = pickle.load(file)
df1 = pd.read_csv('data/csv/df1.csv')

def predict_disease(search_word):
    """주어진 검색어에 대해 유사도가 높은 상위 질병을 반환합니다."""
    # 검색어 텍스트를 TF-IDF 벡터로 변환합니다.
    tfidf_vector = vectorizer.transform([search_word])
    # 각 질병에 대한 증상 벡터와의 코사인 유사도를 계산합니다.
    cosine_similarities = cosine_similarity(tfidf_vector, tfidf_matrix_symptoms)
    # 유사도와 질병 인덱스를 함께 저장합니다.
    disease_similarities = list(zip(cosine_similarities[0], range(len(df1))))
    # 유사도가 70% 이상인 질병을 찾습니다.
    similar_diseases = [index for similarity, index in disease_similarities if similarity > 0.7]
    # 유사도가 높은 순서대로 정렬합니다.
    similar_diseases.sort(key=lambda x: -disease_similarities[x][0])
    # 유사도가 높은 상위 질병의 이름을 반환합니다.
    disease_names = [df1['disease_korean_title'].iloc[i] for i in similar_diseases]
    # 중복된 질병 이름을 제거합니다.
    unique_disease_names = list(set(disease_names))
    # 유사도가 높은 상위 질병을 반환합니다.
    return unique_disease_names[:min(100, len(unique_disease_names))]


#### -------------------------------------------------------------------------------------------------------
### 병원 검색 모델 적용 펑션---------------------------------------------------------------------------------------
hospital_types = {
    "일반의": "00", "내과": "01", "신경과": "02", "정신건강의학과": "03", "외과": "04",
    "정형외과": "05", "신경외과": "06", "심장혈관흉부외과": "07", "성형외과": "08", "마취통증의학과": "09",
    "산부인과": "10", "소아청소년과": "11", "안과": "12", "이비인후과": "13", "피부과": "14",
    "비뇨의학과": "15", "영상의학과": "16", "방사선종양학과": "17", "병리과": "18", "진단검사의학과": "19",
    "결핵과": "20", "재활의학과": "21", "핵의학과": "22", "가정의학과": "23", "응급의학과": "24",
    "직업환경의학과": "25", "예방의학과": "26", "기타1(치과)": "27", "기타4(한방)": "28",
    "기타2": "31", "기타2": "40", "보건": "41", "기타3": "42", "보건기관치과": "43",
    "보건기관한방": "44", "치과": "49", "구강악안면외과": "50", "치과보철과": "51", "치과교정과": "52",
    "소아치과": "53", "치주과": "54","치과보존과": "55", "구강내과": "56", "영상치의학과": "57",
    "구강병리과": "58", "예방치과": "59", "치과소계": "60", "통합치의학과": "61", "한방내과": "80",
    "한방부인과": "81", "한방소아과": "82", "한방안·이비인후·피부과": "83", "한방신경정신과": "84",
    "침구과": "85", "한방재활의학과": "86", "사상체질과": "87", "한방응급": "88", "한방응급": "89", "한방소계": "90"
}
under = {
"옹진군": (37.446355, 126.628327),"연천군": (38.096289, 127.074793),"태백시": (37.164045, 128.985565),"횡성군": (37.491219, 127.985382)
,"영월군": (37.183804, 128.461737),'평창군': (37.370474, 128.390291),"정선군": (37.380119, 128.660835),"철원군": (38.146609, 127.313317)
,"화천군": (38.105771, 127.707959),"양구군": (38.107419, 127.989882),"인제군": (38.069391, 128.170699),"고성군(강원도)": (38.380281, 128.467945)
,"양양군": (38.070834, 128.622314),"보은군": (36.489433, 127.729970),"옥천군": (36.306512, 127.572629),"영동군": (36.174465, 127.776433)
,"괴산군": (36.815129, 127.786976),"단양군": (36.984547, 128.365517),"증평군": (36.780657, 127.583056),"계룡시": (36.274680, 127.249748)
,"서천군": (36.078514, 126.691342),"청양군": (36.459448, 126.802978),"진안군": (35.791436, 127.424438),"무주군": (36.010101, 127.660822)
,"장수군": (35.647771, 127.521158),"임실군": (35.617222, 127.288112),"순창군": (35.374355, 127.138868),"부안군": (35.731648, 126.733497)
,"담양군": (35.321545, 126.988917),"곡성군": (35.282315, 127.292356),"구례군": (35.202503, 127.462788),"보성군": (34.771963, 127.080004)
,"장흥군": (34.681282, 126.919883),"강진군": (34.642334, 126.767435),"함평군": (35.065311, 126.516100),"영광군": (35.277481, 126.509277)
,"장성군": (35.300212, 126.785797),"완도군": (34.308197, 126.755875),"진도군": (34.486561, 126.263134),"신안군": (34.831242, 126.351883)
,"군위군": (36.242749, 128.572585),"의성군": (36.352657, 128.697675),"청송군": (36.435111, 129.057789),"영양군": (36.660178, 129.114291)
,"영덕군": (36.415015, 129.365784),"청도군": (35.647155, 128.734038),"고령군": (35.727955, 128.270142),"성주군": (35.919655, 128.285690)
,"칠곡군": (35.995992, 128.401543),"예천군": (36.657354, 128.452748),"봉화군": (36.943612, 128.914506),"울진군": (36.993120, 129.400342)
,"울릉군": (37.484736, 130.902374),"의령군": (35.322579, 128.261414),"함안군": (35.272649, 128.406139),"창녕군": (35.541272, 128.492168)
,"고성군 (경상남도)": (34.976859, 128.322245),"남해군": (34.837592, 127.892423),"하동군": (35.067227, 127.751210),"산청군": (35.413800, 127.873538)
,"함양군": (35.520541, 127.725177),"거창군": (  35.686582, 127.909902),"합천군": (35.565055, 128.165960),"제주시": (33.499621, 126.531188),"서귀포시": (33.254120, 126.560076)
}

def get_hospital_code(hospital_name: str) -> int:
    return hospital_types.get(hospital_name, -1) 

class Position(BaseModel):
    xPos: Optional[float] = None
    yPos: Optional[float] = None
    
def find_hospital_code(input_value: str) -> str:
    """
    입력값을 기반으로 hospital_types에서 대응하는 코드를 찾아 반환합니다.
    정확히 일치하는 항목이 없을 경우 빈 문자열을 반환합니다.
    """
    for department, code in hospital_types.items():
        if department in input_value:
            return code
    return ''
def preprocess_input(input_value):
    """입력값에서 + 기호와 공백을 제거하는 함수"""
    # + 기호를 공백으로 변환
    processed_value = input_value.replace("+", " ")
    # 공백 제거
    processed_value = processed_value.replace(" ", "")
    return processed_value

def search_by_code_or_name(input_value: str):
    """
    입력값을 분석하여 코드로 검색할지, 이름으로 검색할지 결정하고 검색을 수행합니다.
    """
    input_value = preprocess_input(input_value)
    code = find_hospital_code(input_value)
    if code and input_value.strip() in hospital_types:
        # 입력값이 코드의 대표값과 정확히 일치하는 경우 코드로 검색
        code
        # search_logic_using_code(code) # 실제 코드 검색 로직
    else:
        input_value
    # else:
    #     # 일치하는 항목이 없는 경우
    #     print("일치하는 항목이 없습니다.")

def set_search_radius(xPos, yPos, under):
    """
    주어진 사용자의 좌표(xPos, yPos)가 under 딕셔너리에 있는 지역의 좌표로부터 +-0.1 범위 안에 있는 경우,
    검색 반경을 10000으로 설정하고, 그렇지 않은 경우에는 3000으로 설정합니다.

    Parameters:
    xPos (float): 사용자의 X 좌표
    yPos (float): 사용자의 Y 좌표
    under (dict): 지역 이름을 키로 하고, 해당 지역의 위도와 경도를 값으로 하는 딕셔너리

    Returns:
    int: 설정된 검색 반경
    """
    for _, (lon,lat) in under.items():
        # 주어진 좌표가 지역의 좌표로부터 +-0.1 범위 안에 있는지 확인
        if abs(lat - xPos) <= 0.15 and abs(lon - yPos) <= 0.15:
            return 10000  # 범위 안에 있는 경우
    return 3000  # 범위 안에 있는 지역이 없는 경우
# 실제 검색 함수
def search_hospitals(input_value: str, xPos: float, yPos: float, page_number: int = 1):
    input_value = preprocess_input(input_value)
    code = find_hospital_code(input_value)
    radius = set_search_radius(xPos, yPos,under)
    if code and input_value.strip() in hospital_types:
        param = 'dgsbjtCd'
        value = code
        # 코드로 검색할 경우에만 radius 값을 구합니다.
        radius = set_search_radius(xPos, yPos, under)
        queryParams = f'?ServiceKey={pubapi_key}&pageNo={page_number}&{param}={value}&xPos={xPos}&yPos={yPos}&radius={radius}&_type=json'
    else:
        param = 'yadmNm'
        value = input_value
        # 병원 이름으로 검색할 경우에는 radius 파라미터를 추가하지 않습니다.
        queryParams = f'?ServiceKey={pubapi_key}&pageNo={page_number}&{param}={value}&xPos={xPos}&yPos={yPos}&_type=json'
    
    baseUrl = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'
    fullUrl = baseUrl + queryParams
    response = requests.get(fullUrl)
    data = response.json()
    body_data = data['response']['body']['items']['item']
    totalCount = data['response']['body']['totalCount']
    return body_data,totalCount

def paginationforinstitute(data: List[Dict[str, Any]], page_number, total_records, records_per_page=10) -> (List[Dict[str, Any]], Paginations):
    pagination = Paginations(total_records=total_records, current_page=page_number, records_per_page=records_per_page)
    return data, pagination

async def get_excellent_hospital_info(ykiho: str):
    """
    각 병원별 고유 번호(ykiho)를 사용하여 우수 병원 정보를 조회하는 함수입니다.
    """
    ykiho = ykiho.strip("'")  #
    url = f"http://apis.data.go.kr/B551182/exclInstHospAsmInfoService/getExclInstHospAsmInfo?ServiceKey={pubapi_key}&pageNo=1&numOfRows=23&ykiho={ykiho}&_type=json"
    response = requests.get(url)
    ydata = response.json()
    pass
    if ydata['response']['body']['items'] == '':
        return None  # 평가 항목이 없는 경우

    items = ydata['response']['body']['items']['item']
    if isinstance(items, dict):  # 단일 항목인 경우 리스트로 변환
        items = [items]

    return items


#### -------------------------------------------------------------------------------------------------------

@router.get("/info_raredisease/{page_number}")
@router.get("/info_raredisease")
async def disease_list(
    request: Request,
    page_number: int = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None)
    ):
    
    await request.form()
    
    conditions = {}
    
    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')
    if key_name and search_word:
        if key_name == 'dise_name_kr':
            conditions.update({ 'dise_name_kr': { '$regex': search_word }})
        elif key_name == 'dise_KCD_code':
            conditions.update({ 'dise_KCD_code': { '$regex': search_word }})
        elif key_name == 'dise_spc_code':
            conditions.update({ 'dise_spc_code': { '$regex': search_word }})
        elif key_name == 'dise_symptoms':
            similar_diseases_names = predict_disease(search_word)
            conditions.update({'dise_name_kr': {'$in': similar_diseases_names}})

        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
        return templates.TemplateResponse(
            name="/info/info_raredisease.html",
            context={'request': request, 'dise_list': dise_list, 'pagination': pagination,'key_name': key_name,'search_word': search_word})

    elif key_name == 'dise_KCD_code_range':  # KCD 코드 범위를 검색하는 로직
        range_start, range_end = search_word.split('-')
        if range_start != '코드 없음':
            conditions.update({ 'dise_KCD_code': {'$gte': range_start, '$lte': range_end}})
        else:
            conditions.update({ 'dise_KCD_code': { '$regex': '없음' }})
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
        return templates.TemplateResponse(
            name="/info/info_raredisease.html",
            context={'request': request, 'dise_list': dise_list, 'pagination': pagination,'key_name': key_name,'search_word': search_word})

    else: # key_name이 없을 경우 모든 질환의 리스트를 출력
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)

        return templates.TemplateResponse(
            name="/info/info_raredisease.html",
            context={'request': request, 'dise_list': dise_list, 'pagination': pagination})

@router.get("/info_raredisease_nondata", response_class=HTMLResponse) 
async def institution(request:Request):
    return templates.TemplateResponse(name="info/info_raredisease_nondata.html", context={'request':request})

# rest api info_raredisease

@router.post("/raredisease/{page_number}")
@router.post("/raredisease") 
async def raredisease_list(
    request: Request,
    page_number: int = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None)
    ):
    sys.setrecursionlimit(1500)
    
    await request.form()
    
    conditions = {}
    
    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')
    
    if search_word:
        search_word = urllib.parse.unquote(search_word, encoding='utf-8')  # URL 디코딩 처리
    
    if key_name and search_word:
        if key_name == 'dise_name_kr':
            conditions.update({ 'dise_name_kr': { '$regex': search_word }})
        elif key_name == 'dise_KCD_code':
            conditions.update({ 'dise_KCD_code': { '$regex': search_word }})
        elif key_name == 'dise_spc_code':
            conditions.update({ 'dise_spc_code': { '$regex': search_word }})
        elif key_name == 'dise_symptoms':
            similar_diseases_names = predict_disease(search_word)
            conditions.update({'dise_name_kr': {'$in': similar_diseases_names}})

        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
        return {'dise_list': dise_list, 'pagination': pagination.to_dict(),'key_name': key_name,'search_word': search_word}
    elif key_name == 'dise_KCD_code_range':  # KCD 코드 범위를 검색하는 로직
        range_start, range_end = search_word.split('-')
        if range_start != '코드 없음':
            conditions.update({ 'dise_KCD_code': {'$gte': range_start, '$lte': range_end}})
        else:
            conditions.update({ 'dise_KCD_code': { '$regex': '없음' }})
            
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
        return {'dise_list': dise_list, 'pagination': pagination.to_dict(),'key_name': key_name,'search_word': search_word}

    elif key_name==None: # key_name이 없을 경우 모든 질환의 리스트를 출력
        dise_list, pagination = await collection_disease.getsbyconditionswithpagination(conditions, page_number)
        return {'dise_list': dise_list, 'pagination': pagination.to_dict()}


#### -------------------------------------------------------------------------------------------------------

@router.get("/info_institution/{page_number}")
@router.get("/info_institution") 
async def search_hospital(
    request: Request,
    page_number: int = 1,
    keyword: Optional[str] = Query(None),
    pos: Optional[str] = Query(None)):  # Pydantic 모델을 이용해 xPos와 yPos를 pos 객체로 받음):
    await request.form()
    keyword = request.query_params.get('keyword')
    pos = request.query_params.get('pos')
    try: 
        if keyword and pos:
            yPos, xPos = pos.split(',')
            yPos = float(yPos)
            xPos = float(xPos)
            body_data,totalCount = search_hospitals(keyword,xPos,yPos,page_number)
            def safe_float_convert(value):
                try:
                    return float(value)
                except ValueError:
                    return float('inf')
            if isinstance(body_data, dict):
                body_data = [body_data]
            elif not isinstance(body_data, list):
                body_data = [] 
            sorted_data_list = sorted(body_data, key=lambda x: safe_float_convert(x.get('distance', float('inf'))))
            extracted_data = []
            for hospital in sorted_data_list:
                ykiho = hospital['ykiho']
                excellent_info = await get_excellent_hospital_info(ykiho)
                if excellent_info:
                    excellent_info_extracted = [{'asmGrdNm': item['asmGrdNm'], 'asmNm': item['asmNm']} for item in excellent_info]
                    hospital['excellent_info'] = excellent_info_extracted
                else:
                    hospital['excellent_info'] = "없음"
                    
                extracted_data.append({
                    'addr': hospital['addr'],
                    'yadmNm': hospital['yadmNm'],
                    'telno': hospital['telno'],
                    'XPos': hospital['XPos'],
                    'YPos': hospital['YPos'],
                    'ykiho': hospital['ykiho'],
                    'excellent_info': hospital['excellent_info']
                })
            page_data, pagination = paginationforinstitute(extracted_data, page_number, totalCount)
            return templates.TemplateResponse(
                name="info/info_institution.html",
                context={"request": request, 'pagination': pagination, "results": page_data, 'API_KEY': api_key})
        else:
            return templates.TemplateResponse("info/info_institution.html", {"request": request, 'pagination': None, "results": [],'API_KEY': api_key})
    except:
        return templates.TemplateResponse("info/info_institution.html", {"request": request,  'pagination': None, "results": [],'API_KEY': api_key})

@router.post("/institution/{page_number}")
@router.post("/institution") 
async def search_hospital(
    request: Request,
    page_number: int = 1,
    keyword: Optional[str] = Query(None),
    pos: Optional[str] = Query(None)):  # Pydantic 모델을 이용해 xPos와 yPos를 pos 객체로 받음):
    await request.form()
    keyword = request.query_params.get('keyword')
    pos = request.query_params.get('pos')
    try: 
        if keyword and pos:
            keyword = urllib.parse.unquote(keyword)  # URL 디코딩 처리
            yPos, xPos = pos.split(',')
            yPos = float(yPos)
            xPos = float(xPos)
            body_data,totalCount = search_hospitals(keyword,xPos,yPos,page_number)
            def safe_float_convert(value):
                try:
                    return float(value)
                except ValueError:
                    return float('inf')
            if isinstance(body_data, dict):
                body_data = [body_data]
            elif not isinstance(body_data, list):
                body_data = [] 
            sorted_data_list = sorted(body_data, key=lambda x: safe_float_convert(x.get('distance', float('inf'))))
            extracted_data = []
            for hospital in sorted_data_list:
                ykiho = hospital['ykiho']
                excellent_info = await get_excellent_hospital_info(ykiho)
                if excellent_info:
                    excellent_info_extracted = [{'asmGrdNm': item['asmGrdNm'], 'asmNm': item['asmNm']} for item in excellent_info]
                    hospital['excellent_info'] = excellent_info_extracted
                else:
                    hospital['excellent_info'] = "없음"
                    
                extracted_data.append({
                    'addr': hospital['addr'],
                    'yadmNm': hospital['yadmNm'],
                    'telno': hospital['telno'],
                    'XPos': hospital['XPos'],
                    'YPos': hospital['YPos'],
                    'ykiho': hospital['ykiho'],
                    'excellent_info': hospital['excellent_info']
                })
            page_data, pagination = paginationforinstitute(extracted_data, page_number, totalCount)
            return {'pagination': pagination.to_dict(), "results": page_data, 'API_KEY': api_key}
        else:
            return {'pagination': None, "results": [],'API_KEY': api_key}
    except:
        return {'pagination': None, "results": [],'API_KEY': api_key}

#### -------------------------------------------------------------------------------------------------------

# 학술정보
@router.get("/info_academicinfo/{page_number}")
@router.get("/info_academicinfo")
async def paper_list(
    request: Request,
    page_number: int = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None)
    ):
    await request.form()
    conditions = {}

    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')
    if search_word:
        if key_name == 'thesis_name':
            conditions.update({ 'research_title': { '$regex': search_word }})
        elif key_name == 'thesis_date':
            search_word = int(search_word)
            conditions.update({ 'research_year': { '$eq': search_word }})
        pass
        paper_list, pagination = await collection_info_academicinfo_Riss.gbcwp_reverse_year(conditions, page_number)
        return templates.TemplateResponse(
            name="/info/info_academicinfo.html",
            context={'request': request,'papers': paper_list, 'pagination': pagination,'key_name': key_name,'search_word': search_word })

    else:
        paper_list, pagination = await collection_info_academicinfo_Riss.gbcwp_reverse_year(conditions, page_number)

        return templates.TemplateResponse(
            name="/info/info_academicinfo.html",
            context={'request': request,'papers': paper_list, 'pagination': pagination })#'papers': papers, 'pagination': pagination
    
@router.post("/academicinfo/{page_number}")
@router.post("/academicinfo")
async def paper_list(
    request: Request,
    page_number: int = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None)
    ):
    await request.form()
    conditions = {}

    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')

    if search_word:
        search_word = urllib.parse.unquote(search_word)  # URL 디코딩 처리
        if key_name == 'thesis_name':
            conditions.update({ 'research_title': { '$regex': search_word }})
        elif key_name == 'thesis_date':
            search_word = int(search_word)
            conditions.update({ 'research_year': { '$eq': search_word }})
        pass
        paper_list, pagination = await collection_info_academicinfo_Riss.gbcwp_reverse_year(conditions, page_number)
        return {'papers': paper_list, 'pagination': pagination.to_dict(),'key_name': key_name,'search_word': search_word }

    else:
        paper_list, pagination = await collection_info_academicinfo_Riss.gbcwp_reverse_year(conditions, page_number)

        return {'papers': paper_list, 'pagination': pagination.to_dict() }#'papers': papers, 'pagination': pagination

@router.get("/info_academicinfo_pub_med/{page_number}")
@router.get("/info_academicinfo_pub_med")
async def paper_list_pub(
    request: Request,
    page_number: int = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None)
    ):
    await request.form()
    conditions = {}
    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')
    
    if search_word:
        if key_name == 'thesis_name':
            conditions.update({ 'title': { '$regex': search_word }})
        elif key_name == 'thesis_date':
            search_word = int(search_word)
            conditions.update({ 'research_date': { '$eq': search_word }})
        pass
        paper_list, pagination = await collection_info_academicinfo_eng.gbcwp_reverse_year(conditions, page_number)
        return templates.TemplateResponse(
            name="/info/info_academicinfo_pubmed.html",
            context={'request': request,'papers': paper_list, 'pagination': pagination,'key_name': key_name,'search_word': search_word })

    else:
        paper_list, pagination = await collection_info_academicinfo_eng.gbcwp_reverse_year(conditions,page_number)

        return templates.TemplateResponse(
            name="/info/info_academicinfo_pubmed.html",
            context={'request': request,'papers': paper_list, 'pagination': pagination })

@router.post("/academicinfo_pub_med/{page_number}")
@router.post("/academicinfo_pub_med")
async def paper_list_pub(
    request: Request,
    page_number: int = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None)
    ):
    sys.setrecursionlimit(1500)
    await request.form()
    conditions = {}
    key_name = request.query_params.get('key_name')
    search_word = request.query_params.get('search_word')

    if search_word:
        search_word = urllib.parse.unquote(search_word)  
        if key_name == 'thesis_name':
            conditions.update({ 'title': { '$regex': search_word }})
        elif key_name == 'thesis_date':
            search_word = int(search_word)
            conditions.update({ 'research_date': { '$eq': search_word }})
        pass
        paper_list, pagination = await collection_info_academicinfo_eng.gbcwp_reverse_year(conditions, page_number)
        return {'papers': paper_list, 'pagination': pagination.to_dict(),'key_name': key_name,'search_word': search_word }

    else: 
        paper_list, pagination = await collection_info_academicinfo_eng.gbcwp_reverse_year(conditions,page_number)

        return {'papers': paper_list, 'pagination': pagination.to_dict() }#'papers': papers, 'pagination': pagination
##### -------------------------------------------------------------------------------------------------------
