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
        
    news_list, pagination = await collection_trend_news.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="trend/trend_news.html", 
        context={'request': request, 'pagination': pagination, 'news': news_list, 'selected_category': category, 'search_word' : search_word})

@router.post("/trend_news", response_class=HTMLResponse) 
async def trend_news_post(
    request: Request,
    page_number: Optional[int] = 1,
    key_name: Optional[str] = Query(None),
    search_word: Optional[str] = Query(None),
    category: Optional[str] = Query(None)  # 카테고리 정보를 쿼리 파라미터로 받음
):
    await request.form()
    
    conditions = {}
    
    if category:  # 만약 카테고리가 전달되면 해당 카테고리에 맞게 필터링
        conditions['news_topic'] = category
        
    news_list, pagination = await collection_trend_news.getsbyconditionswithpagination(
        conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="trend/trend_news.html", 
        context={'request': request, 'pagination': pagination, 'news': news_list, 'selected_category': category}
    )
    
# news_read

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