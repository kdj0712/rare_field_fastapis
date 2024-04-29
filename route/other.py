from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from beanie import PydanticObjectId
from typing import Optional
from datetime import datetime
from database.connection import Database

# 라우터 연결
router = APIRouter()
templates = Jinja2Templates(directory="templates/")

# db 연결
from models.other_QnA import QnA
collection_QnA = Database(QnA)
from models.notice_list import notice
collection_other_notice = Database(notice)



#### -------------------------------------------------------------------------------------------------------

# 공지사항

@router.get("/other_notice", response_class=HTMLResponse)
async def NOTICE(
    request:Request
    , page_number: Optional[int] = 1
    ):
    
    conditions = {}
    
    notice_list, pagination = await collection_other_notice.getsbyconditionswithpagination(
    conditions, page_number)
    
    return templates.TemplateResponse(name="other/other_notice.html", context={'request' :request, 'notices' : notice_list, 'pagination' : pagination})

@router.post("/other_notice", response_class=HTMLResponse)
async def NOTICE(request:Request):
    return templates.TemplateResponse(name="other/other_notice.html", context={'request' :request})

#### -------------------------------------------------------------------------------------------------------

# QnA

@router.get("/other_QnA_main/{page_number}")
@router.get("/other_QnA_main") # 검색 with pagination
# http://127.0.0.1:8000/users/list_jinja_pagination?key_name=name&word=김
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=
# http://127.0.0.1:8000/users/list_jinja_pagination/2?key_name=name&word=김
async def QnA_function(
    request: Request,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
):
    # db.answers.find({'name':{ '$regex': '김' }})
    # { 'name': { '$regex': user_dict.word } }
    
    user_dict = dict(request._query_params)
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

    # if ques_title:
    #     conditions.find({ 'ques_title': { '$regex': search_word }})
    # pass

    # try:
    #     QnA_list, pagination = await collection_QnA.gbcwp_reverse(
    #     conditions, page_number
    # )
    #     return templates.TemplateResponse(
    #     name="other/other_QnA_main.html",
    #     context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    # )

    # except:
    #     return templates.TemplateResponse(
    #     name="other/other_QnA_nonpage.html",
    #     context={'request': request},
    # )

@router.post("/other_QnA_main", response_class=HTMLResponse) 
async def QnA_function(request:Request,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None
    ):
    
    form_data = await request.form()
    dict_form_data = dict(form_data)
    
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # 이 시간을 item 객체의 'ques_time' 속성에 저장한다.
    dict_form_data['ques_time'] = formatted_time

    if dict_form_data['ques_title'] =='': # title은 필수조건, 오류로 인한 저장을 방지하기 위한 구문
        pass
    else:
        QnAs = QnA(**dict_form_data)
        await collection_QnA.save(QnAs)
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

#     if ques_title:
#         conditions.find({ 'ques_title': { '$regex': search_word }})
#     pass
#     try:
#         QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
#         conditions, page_number
#     )
#         return templates.TemplateResponse(
#         name="other/other_QnA_main.html",
#         context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
#     )

#     except:
#         return templates.TemplateResponse(
#         name="other/other_QnA_nonpage.html",
#         context={'request': request},
#     )

# @router.get("/other_QnA_nonpage", response_class=HTMLResponse) 
# async def QnA_function(request:Request):
#     return templates.TemplateResponse(name="other/other_QnA_nonpage.html", context={'request':request})



# 글쓰기 창
@router.get("/other_QnA_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="other/other_QnA_write.html", context={'request':request})

@router.post("/other_QnA_write", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="other/other_QnA_write.html", context={'request':request})

# 글 확인

@router.get("/other_QnA_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    dict(request._query_params)
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="other/other_QnA_read.html", context={'request':request,'QnAs' : QnA})


@router.post("/other_QnA_read/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId):
    await request.form()
    QnA = await collection_QnA.get(object_id)
    return templates.TemplateResponse(name="other/other_QnA_read.html", context={'request':request ,'QnAs' : QnA})


# 답글 달기
@router.post("/other_reply/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request, object_id:PydanticObjectId,
    page_number: Optional[int] = 1, 
    ques_title: Optional[str] = None,
    ques_writer: Optional[str] = None,
    ques_content: Optional[str] = None,
    ques_time: Optional[datetime] = None,
    ques_answer: Optional[str] = None):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    await collection_QnA.update_one(object_id, dict_form_data)
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

    # if ques_title:
    #     conditions.find({ 'ques_title': { '$regex': search_word }})
    # pass
    # try:
    #     QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
    #     conditions, page_number
    # )
    #     return templates.TemplateResponse(
    #     name="other/other_QnA_main.html",
    #     context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    # )

    # except:
    #     return templates.TemplateResponse(
    #     name="other/other_QnA_nonpage.html",
    #     context={'request': request},
    # )
        
# 글 삭제
@router.post("/other_delete/{object_id}", response_class=HTMLResponse) 
async def FAQ(request:Request,object_id:PydanticObjectId):
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

    # if ques_title:
    #     conditions.find({ 'ques_title': { '$regex': search_word }})
    # pass
    # try:
    #     QnA_list, pagination = await collection_QnA.getsbyconditionswithpagination(
    #     conditions, page_number
    # )
    #     return templates.TemplateResponse(
    #     name="other/other_QnA.html",
    #     context={'request': request, 'QnAs': QnA_list, 'pagination': pagination,'search_word':search_word},
    # )

    # except:
    #     return templates.TemplateResponse(
    #     name="other/other_QnA_nonpage.html",
    #     context={'request': request},
    # )

# 글쓰기 창
@router.get("/other_notice", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="other/other_notice.html", context={'request':request})

@router.post("/other_notice", response_class=HTMLResponse) 
async def FAQ(request:Request):
    return templates.TemplateResponse(name="other/other_notice.html", context={'request':request})
