from fastapi import APIRouter, Query, Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Union
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId
from models.trend_documents import trend_documents
from models.trend_guideline import trend_guideline
from models.trend_law import trend_law
from models.trend_site import trend_site
from models.trend_news import news_trends # mongodb 추가해서 넣어야 함
import urllib.parse

from typing import List, Dict

collection_trend_news= Database(news_trends)
collection_trend_guideline= Database(trend_guideline)
collection_trend_documents= Database(trend_documents)
collection_trend_law= Database(trend_law)
collection_trend_site= Database(trend_site)

router = APIRouter()

templates = Jinja2Templates(directory="templates/")


#### -------------------------------------------------------------------------------------------------------

# 뉴스
@router.get("/trend_news/{page_number}")
@router.get("/trend_news", response_class=HTMLResponse) 
async def trend_news(
    request:Request
    , page_number: Optional[int] = 1
    , news_title : Optional[Union[str, int, float, bool]] = None
    , news_paper : Optional[Union[str, int, float, bool]] = None
    , category: Optional[str] = Query(None)  # 카테고리 정보를 쿼리 파라미터로 받음
    ):
    
    await request.form()
    
    conditions = {}
    search_word = request.query_params.get('search_word')

    # 검색
    if search_word :
        conditions.update({
            "$or" : [
                {"news_title" : {'$regex': search_word}}
                ,{"news_paper" : {'$regex': search_word}}
            ]
        })

    if news_title:
        conditions.find({ 'news_title': { '$regex': search_word }})
    if news_paper:
        conditions.find({ 'news_paper': { '$regex': search_word }})
    
    # 만약 카테고리가 전달되면 해당 카테고리에 맞게 필터링
    if category:  
        conditions['news_topic'] = category
        
    news_list, pagination = await collection_trend_news.gbcwp_reverse_date(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="trend/trend_news.html", 
        context={'request': request, 'pagination': pagination, 'news': news_list, 'selected_category': category, 'search_word' : search_word})

@router.get("/trend_news_read/{object_id}", response_class=HTMLResponse)
async def trend_news_read_function(
    request: Request, 
    object_id:PydanticObjectId
    ):
    
    news = await collection_trend_news.get(object_id)

    return templates.TemplateResponse(
        name="trend/trend_news_read.html",
        context={"request": request, "news": news})
        
@router.post("/trend_news_read/{object_id}", response_class=HTMLResponse)
async def trend_news_read_function(
    request: Request, 
    ):
    
    await request.form()
    print(dict(await request.form()))
    
    return templates.TemplateResponse(
        name="trend/trend_news.html",
        context={"request": request}
    )


# restapi 생성
@router.post("/trend_news_data")
async def get_news_data(
    request:Request
    , page_number: Optional[int] = 1
    , news_title : Optional[Union[str, int, float, bool]] = None
    , news_paper : Optional[Union[str, int, float, bool]] = None
    , category: Optional[str] = Query(None)
):

    await request.form()

    if category:
        category = urllib.parse.unquote(category, encoding='utf-8')  # URL 디코딩 처리    

    conditions = {}
    search_word = request.query_params.get('search_word')
    if search_word:
        search_word = urllib.parse.unquote(search_word, encoding='utf-8')  # URL 디코딩 처리

    # 검색
    if search_word :
        conditions.update({
            "$or" : [
                {"news_title" : {'$regex': search_word}}
                ,{"news_paper" : {'$regex': search_word}}
            ]
        })

    if news_title:
        conditions.find({ 'news_title': { '$regex': search_word }})
    if news_paper:
        conditions.find({ 'news_paper': { '$regex': search_word }})
    
    # 만약 카테고리가 전달되면 해당 카테고리에 맞게 필터링
    if category:  
        conditions['news_topic'] = category
        
    news_list, pagination = await collection_trend_news.gbcwp_reverse_date(
    conditions, page_number
    )

    # 모든 결과를 하나의 json 형태로 변환
    return {
        'pagination' : pagination.to_dict(), 'news' : news_list
        , 'selected_category' : category, 'search_word' : search_word
    }



@router.get("/trend_news_data/{object_id}")
async def trend_news_read_function(
    request: Request, 
    object_id:PydanticObjectId
    ):
    
    news = await collection_trend_news.get(object_id)

    return {"news": news}
        

#### -------------------------------------------------------------------------------------------------------

# 법, 시행령, 시행규칙

@router.get("/trend_law", response_class=HTMLResponse) 
async def trend_law(request:Request,
                    page_number: Optional[int] = 1
                    ):
    condition ={}
    laws, pagination=await collection_trend_law.getsbyconditionswithpagination(condition, page_number)
    
    return templates.TemplateResponse(name="trend/trend_law.html", context={'request':request,
                                                                                  'laws':laws,
                                                                                  'pagination':pagination})

@router.post("/trend_law", response_class=HTMLResponse) 
async def trend_law(request:Request):
    return templates.TemplateResponse(name="trend/trend_law.html", context={'request':request})


# restapi 생성
@router.post("/trend_law_data", response_model=Dict[str, List])
async def get_law_data():
    data_law = await collection_trend_law.get_all()

    # 모든 결과를 하나의 json 형태로 변환
    return {
        "trend_law" : data_law
    }

#### -------------------------------------------------------------------------------------------------------

# 고시, 지침dd

@router.get("/trend_guideline", response_class=HTMLResponse) 
async def guideline(request:Request, page_number: Optional[int] = 1):
    condition ={}
    guidelines, pagination=await collection_trend_guideline.getsbyconditionswithpagination(condition, page_number)
    return templates.TemplateResponse(name="trend/trend_guideline.html", context={'request':request,
                                                                                  'guidelines':guidelines,
                                                                                  'pagination':pagination})

@router.get("/trend_guideline", response_class=HTMLResponse) 
async def guideline(request:Request):
    return templates.TemplateResponse(name="trend/trend_guideline.html", context={'request':request})

# 안으로 들어가서
@router.get("/trend_guideline_read/{object_id}", response_class=HTMLResponse)
async def trend_guideline_read_func(
    request:Request
    ,object_id : PydanticObjectId
):
    
    guideline = await collection_trend_guideline.get(object_id)

    return templates.TemplateResponse(
        name="trend/trend_guideline_read.html"
        , context={"request" : request, "guidelines" : guideline}
    )

@router.post("/guideline_read/{object_id}")
async def guideline_read_func(
            request:Request
            ,object_id : PydanticObjectId
            ):
    
    guideline = await collection_trend_guideline.get(object_id)

    return {"request" : request, "guidelines" : guideline}
    


# restapi 생성
@router.post("/trend_guideline_data", response_model=Dict[str, List])
async def get_guideline_data():
    data_guideline = await collection_trend_guideline.get_all()

    # 모든 결과를 하나의 json 형태로 변환
    return {
        "trend_guideline" : data_guideline
    }


#### -------------------------------------------------------------------------------------------------------

# # 민원서식 삭제 처리

# @router.get("/trend_document", response_class=HTMLResponse) 
# async def document(request:Request, page_number: Optional[int] = 1):
#     condition ={}
#     documents, pagination=await collection_trend_documents.getsbyconditionswithpagination(condition, page_number)
#     return templates.TemplateResponse(name="trend/trend_document.html", context={'request':request,
#                                                                                   'documents':documents,
#                                                                                   'pagination':pagination})


# @router.get("/trend_document_read/{object_id}" ) 
# async def document(request:Request,  object_id:PydanticObjectId):
#     documents = collection_trend_documents.get(object_id)

#     return templates.TemplateResponse(name="trend/trend_document.html", context={'request':request,
#                                                                                  'documents':documents})

# #### -------------------------------------------------------------------------------------------------------

# 관련사이트

@router.get("/trend_site", response_class=HTMLResponse) 
async def trend_site(
    request:Request
    , page_number: Optional[int] = 1
    ):
    
    condition ={}
    sites_list, pagination = await collection_trend_site.getsbyconditionswithpagination(condition, page_number)
    
    return templates.TemplateResponse(name="trend/trend_site.html", context={'request':request, 'sites':sites_list, 'pagination' : pagination})

@router.post("/trend_site", response_class=HTMLResponse) 
async def trend_site(request:Request):
    return templates.TemplateResponse(name="trend/trend_site.html", context={'request':request})

# restapi 생성
@router.post("/trend_site_data", response_model=Dict[str, List])
async def get_site_data():
    data_site = await collection_trend_site.get_all()

    # 모든 결과를 하나의 json 형태로 변환
    return {
        "trend_site" : data_site
    }
