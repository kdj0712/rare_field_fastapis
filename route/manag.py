from fastapi import APIRouter, Request,Query
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, Union
from datetime import datetime
from database.connection import Database
from beanie import PydanticObjectId
from pydantic import BaseModel, Field, EmailStr

# db 연결
from models.academicinfo import academicinfo
collection_acade = Database(academicinfo)
from models.info_rarediseases import diseases
collection_dise = Database(diseases)
from models.institution import Institutions
collection_insti = Database(Institutions)
from models.trend_news import news_trends as news
collection_trend = Database(news)
from models.user_member import members
collection_member = Database(members)
from models.other_QnA import QnA
collection_QnA = Database(QnA)
from models.notice_list import notice
collection_manag_notice = Database(notice)
from models.program_list import program
collection_manag_program = Database(program)
from models.empo_community import community
collection_empo_community = Database(community)

# 라우터 연결
router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# url 경로, 자원 물리 경로, 프로그래밍 측면
from fastapi.staticfiles import StaticFiles
router.mount("/data/img", StaticFiles(directory="data/img/"), name="static_img")

#### -------------------------------------------------------------------------------------------------------

# manag main - 대시보드

@router.get("/managmain", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/managmain.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# user_main

@router.get("/manag_user_main/{page_number}")
@router.get("/manag_user_main") # 검색 with pagination

async def list(
    request: Request,
    page_number: Optional[int] = 1, 
    user_ID: Optional[Union[str, int, float, bool]] = None,
    user_name: Optional[Union[str, int, float, bool]] = None,
    user_phone : Optional[Union[str, int, float, bool]] = None,
    user_email: Optional[EmailStr] = None   
    ):

    conditions = {}
    search_word = request.query_params.get('search_word')

    if search_word:
        conditions.update({
            "$or": [
                {"user_ID": {'$regex': search_word}},
                {"user_name": {'$regex': search_word}},
                {"user_phone": {'$regex': search_word}},
                {"user_email": {'$regex': search_word}}
            ]
        })
    pass

    if user_ID:
        conditions.find({ 'user_ID': { '$regex': search_word }})
    if user_name:
        conditions.find({ 'user_name': { '$regex': search_word }})
    if user_phone:
        conditions.find({ 'user_phone': { '$regex': search_word }})
    if user_email:
        conditions.find({ 'user_email': { '$regex': search_word }})

    # try:
    User_list, pagination = await collection_member.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
    name="manag/user/manag_user_main.html",
    context={'request': request, 'user_list': User_list, 'pagination': pagination,'search_word' : search_word}
    )

#### -------------------------------------------------------------------------------------------------------

# community_main

@router.get("/manag_community_main/{page_number}", response_class=HTMLResponse)
@router.get("/manag_community_main", response_class=HTMLResponse) 
async def community_main_function(
    request:Request,
    page_number: Optional[int] = 1
    , community_type: Optional[Union[str, int, float, bool]] = None
    , community_title: Optional[Union[str, int, float, bool]] = None
    , community_writer: Optional[Union[str, int, float, bool]] = None
    , community_date: Optional[Union[str, int, float, bool]] = None
    ):

    conditions = {}
    search_word = request.query_params.get('search_word')

    if search_word:
        conditions.update({
            "$or": [
                {"community_type": {'$regex': search_word}},
                {"community_title": {'$regex': search_word}},
                {"community_writer": {'$regex': search_word}},
                {"community_date": {'$regex': search_word}}
            ]
        })
    pass

    if community_type:
        conditions.find({ 'community_type': { '$regex': search_word }})
    if community_title:
        conditions.find({ 'community_title': { '$regex': search_word }})
    if community_writer:
        conditions.find({ 'community_writer': { '$regex': search_word }})
    if community_date:
        conditions.find({ 'community_date': { '$regex': search_word }})

    community_list, pagination = await collection_empo_community.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="manag/community/manag_community_main.html", 
        context={'request':request, 'pagination': pagination, 'communitys': community_list, 'search_word' : search_word})

@router.post("/manag_community_main", response_class=HTMLResponse) 
async def community_main_function(request:Request):
    
    await request.form()
    dict(await request.form())
    
    community_list = await collection_empo_community.get_all()
        
    return templates.TemplateResponse(
        name="manag/community/manag_community_main.html", 
        context={'request':request, 'communitys': community_list})

@router.get("/manag_community_read/{object_id}", response_class=HTMLResponse) 
async def manag_community_read_function(request:Request,
                                        object_id:PydanticObjectId):
    
    community_list = await collection_empo_community.get(object_id)
        
    return templates.TemplateResponse(name="manag/community/manag_community_read.html", context={'request':request, 'communitys':community_list})

@router.post("/manag_community_read{object_id}", response_class=HTMLResponse) 
async def manag_community_read_function(request:Request):
    return templates.TemplateResponse(name="manag/community/manag_community_read.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# program_main

@router.get("/manag_program_main/{page_number}", response_class=HTMLResponse)
@router.get("/manag_program_main", response_class=HTMLResponse) 

async def program_main_function(
    request:Request
    , page_number: Optional[int] = 1
    , program_title: Optional[Union[str, int, float, bool]] = None
    ):
    
    conditions = {}
    search_word = request.query_params.get('search_word')

    if search_word:
        conditions.update({
            "$or":[
                {"program_title": {'$regex': search_word}}
            ]
        })

    if program_title:
        conditions.find({ 'program_title': { '$regex': search_word }})

    program_list, pagination = await collection_manag_program.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="manag/program/manag_program_main.html", 
        context={'request':request, 'pagination': pagination, 'programs': program_list, 'search_word':search_word})

@router.post("/manag_program_main", response_class=HTMLResponse) 
async def program_main_function(request:Request):
    
    await request.form()
    print(dict(await request.form()))
    
    programs = await collection_manag_program.get_all()
    
    return templates.TemplateResponse(
        name="manag/program/manag_program_main.html", 
        context={'request':request, 'programs': programs})

@router.get("/manag_program_write", response_class=HTMLResponse) 
async def program_write_function(request:Request):    
    return templates.TemplateResponse(name="manag/program/manag_program_write.html", context={'request':request})

@router.post("/manag_program_write", response_class=HTMLResponse) 
async def program_write_function(request:Request):
    return templates.TemplateResponse(name="manag/program/manag_program_write.html", context={'request':request})

@router.get("/manag_program_reply/{object_id}", response_class=HTMLResponse) 
async def program_reply_function(request:Request, object_id:PydanticObjectId):
    
    program = await collection_manag_program.get(object_id)
    
    return templates.TemplateResponse(name="manag/program/manag_program_reply.html", context={'request':request, 'program': program})

@router.post("/manag_program_reply/{object_id}", response_class=HTMLResponse) 
async def program_reply_function(request:Request):
    return templates.TemplateResponse(name="manag/program/manag_program_reply.html", context={'request':request})


#### -------------------------------------------------------------------------------------------------------


@router.get("/QnA/manag_QnA_manager_nonpage", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_manager_nonpage.html", context={'request':request})

@router.post("/QnA/manag_QnA_manager_nonpage", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_manager_nonpage.html", context={'request':request})

@router.post("/manag_QnA_main", response_class=HTMLResponse) 
@router.get("/manag_QnA_main/{page_number}")
@router.get("/manag_QnA_main") # 검색 with pagination

async def QNA_list(
    request : Request
    , page_number : Optional[int] =1
    , ques_title : Optional[Union[str, int, float, bool]] = None
    ):

    conditions = {}
    search_word = request.query_params.get('search_word')

    if search_word :
        conditions.update({
            "$or" : [
                {"ques_title" : {'$regex' : search_word}}
            ]
        })
    pass

    if ques_title :
        conditions.find({'ques_title' : {'$regex' : search_word}})

    QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
    conditions, page_number
    )

    return templates.TemplateResponse(
        name='manag/QnA/manag_QnA_main.html'
        ,context={'request' : request, 'pagination' : pagination
                 , 'QnAs' : QnA_list, 'search_word' : search_word})

# 글쓰기 창
@router.get("/manag_QnA_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_write.html", context={'request':request})

@router.post("/manag_QnA_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_write.html", context={'request':request})

# 글 확인

@router.get("/manag_QnA_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    dict(request._query_params)
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_read.html", context={'request':request,'QnAs' : QnA,'object_id':object_id})


@router.post("/manag_QnA_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    await collection_QnA.update_one(object_id, dict_form_data)
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="manag/QnA/manag_QnA_read.html", context={'request':request ,'QnAs' : QnA})

        
# 글 삭제
@router.post("/manag_QnA_delete/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request,object_id:PydanticObjectId,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None):
    await collection_QnA.delete_one(object_id)
    
    form_data = await request.form()
    dict_form_data = dict(form_data)

    conditions = {}

    search_word = request.query_params.get('search_word')
  
    if search_word:
        conditions.update({
            "$or": [
                {"ques_title": {'$regex': search_word}},
                {"ques_writer": {'$regex': search_word}},
                {"ques_content": {'$regex': search_word}},
                {"ques_time": {'$regex': search_word}},
                {"ques_answer": {'$regex': search_word}},
            ]
        })
    pass

    if ques_title:
        conditions.find({ 'ques_title': { '$regex': search_word }})
    pass
    try:
        QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
        conditions, page_number
    )
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_main.html",
        context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    )

    except:
        return templates.TemplateResponse(
        name="manag/QnA/manag_QnA_manager_nonpage.html",
        context={'request': request},
    )

@router.post("/manag_user_detail/{object_id}") # 펑션 호출 방식
async def reads(request:Request,object_id:PydanticObjectId):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="manag/user/manag_user_detail.html", context={'request':request, 'object_id':object_id})


@router.get("/manag_user_detail/{object_id}") 
async def FAQ(request:Request, object_id:PydanticObjectId):
    dict(request._query_params)
    user_list = await collection_member.get(object_id)
    return templates.TemplateResponse(name="manag/user/manag_user_detail.html", context={'request':request,'User' : user_list})

#### -------------------------------------------------------------------------------------------------------

# notice_main
@router.get("/manag_notice_main/{page_number}")
@router.get("/manag_notice_main", response_class=HTMLResponse)

async def notice_main_function(
    request:Request,
    page_number: Optional[int] = 1,
    notice_title: Optional[Union[str, int, float, bool]] = None,
    notice_date: Optional[Union[str, int, float, bool]] = None,
    notice_type : Optional[Union[str, int, float, bool]] = None):
    
    conditions = {}
    search_word = request.query_params.get('search_word')

    if search_word:
        conditions.update({
            "$or" : [
                {"notice_type" : {'$regex' : search_word}}
                , {"notice_title" : {'$regex' : search_word}}
                , {"notice_date" : {'$regex' : search_word}}
            ]
        })
    if notice_title:
        conditions.find({'notice_title' : {'$regex' : search_word}})
    if notice_type:
        conditions.find({'notice_type' : {'$regex' : search_word}})
    if notice_date:
        conditions.find({'notice_date' : {'$regex' : search_word}})
    
    notices, pagination = await collection_manag_notice.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(name="manag/notice/manag_notice_main.html", context={'request': request, 'pagination':pagination, 'notices':notices, 'search_word' : search_word})

@router.post("/manag_notice_main/{page_number}", response_class=HTMLResponse)

# notice_write

@router.get("/manag_notice_write", response_class=HTMLResponse) 
async def notice_write_function(request:Request):
    return templates.TemplateResponse(name="manag/notice/manag_notice_write.html", context={'request':request})

@router.post("/manag_notice_write/{page_number}", response_class=HTMLResponse)
@router.post("/manag_notice_write", response_class=HTMLResponse) 
async def notice_main_function(
    request:Request,
    page_number: Optional[int] = 1
    ):
    
    form_data = await request.form()
    dict_form_data = dict(form_data)
    
    ## notice 작성 부분
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # 이 시간을 item 객체의 'ques_time' 속성에 저장한다.
    dict_form_data['notice_date'] = formatted_time

    if dict_form_data['notice_title'] ==' ': # title은 필수조건, 오류로 인한 저장을 방지하기 위한 구문
        pass
    else:
        notice_list = notice(**dict_form_data)
        await collection_manag_notice.save(notice_list)
    
     ## db 불러오기 + 페이지네이션
    
    conditions = {}
    
    notices, pagination = await collection_manag_notice.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(name="manag/notice/manag_notice_main.html", context={'request':request, 'notices':notices, 'pagination': pagination})

# notice_reply

@router.get("/manag_notice_reply/{object_id}", response_class=HTMLResponse) 
async def notice_reply_function(request:Request, object_id:PydanticObjectId):
    
    notices = await collection_manag_notice.get(object_id)
    
    return templates.TemplateResponse(name="manag/notice/manag_notice_reply.html", context={'request':request, 'notices':notices})

@router.post("/manag_notice_reply/{object_id}", response_class=HTMLResponse) 
async def notice_reply_function(request:Request, object_id:PydanticObjectId):
    
    await request.form()
    notices = await collection_manag_notice.get(object_id)
    
    return templates.TemplateResponse(name="manag/notice/manag_notice_reply.html", context={'request':request, 'notices':notices})

#### -------------------------------------------------------------------------------------------------------
    
# data analytics

@router.get("/data_analytics", response_class=HTMLResponse) 
async def data_analytics(request:Request):
    return templates.TemplateResponse(name="manag/data_analytics/manag_data_analytics.html", context={'request':request})

@router.post("/data_analytics", response_class=HTMLResponse) 
async def data_analytics(request:Request):
    return templates.TemplateResponse(name="manag/data_analytics/manag_data_analytics.html", context={'request':request})