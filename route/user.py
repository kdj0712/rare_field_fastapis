from fastapi import APIRouter, HTTPException, Request, FastAPI
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from beanie import PydanticObjectId

app = FastAPI()
router = APIRouter()

from database.connection import Database
from models.user_member import members
collection_member = Database(members)

templates = Jinja2Templates(directory="templates/")

from fastapi.staticfiles import StaticFiles
app.mount("/data/img", StaticFiles(directory="data/img"), name="static_img")


#### -------------------------------------------------------------------------------------------------------

# 로그인
@router.get("/user_login", response_class=HTMLResponse) 
async def user_login(request:Request):
    return templates.TemplateResponse(name="user/user_login.html", context={'request':request})

@router.post("/user_login", response_class=HTMLResponse) 
async def user_login(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    member = members(**dict_form_data)
    await collection_member.save(member)
    return templates.TemplateResponse(name="user/user_login.html", context={'request':request, 'users':dict_form_data})

# 로그인 체킹 페이지
@router.get("/user_logincheck", response_class=HTMLResponse) 
async def mypage(request:Request,user_id:PydanticObjectId ):
    return templates.TemplateResponse(name="user/user_logincheck.html", context={'request':request,'user_id':PydanticObjectId})

@router.post("/user_logincheck", response_class=HTMLResponse) 
async def mypage(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    pass
    inputID = dict_form_data['user_ID']
    inputPSWD = dict_form_data['user_pswd']

    check_list = await collection_member.get_all()
    checks_list = [answer.dict() for answer in check_list]

    logcheck = False
    pass
    for i in checks_list:
        if i['user_ID'] == inputID and i['user_pswd'] == inputPSWD:
            logcheck = True
            break
    if logcheck:
        return templates.TemplateResponse(name="mainpage.html", context={'request':request})
    else: 
        return templates.TemplateResponse(name="user/user_logincheck.html", context={'request':request,'user_id':PydanticObjectId})

#### -------------------------------------------------------------------------------------------------------

# 회원가입
@router.get("/user_join", response_class=HTMLResponse)
async def user_join(request:Request):
    # email_list = await collection_member.get('user_email')
    # ID_list = await collection_member.get('user_ID')
    return templates.TemplateResponse(name="user/user_join.html", context={'request':request})

@router.post("/user_join", response_class=HTMLResponse)
async def user_join(request:Request):
    # email_list = await collection_member.get('user_email')
    # ID_list = await collection_member.get('user_ID')
    return templates.TemplateResponse(name="user/user_join.html", context={'request':request})

# 회원가입 ID 중복확인 페이지
@router.get("/user_joincheck_ID", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_joincheck_ID.html", context={'request':request})

@router.post("/user_joincheck_IDcheck", response_class=HTMLResponse) 
async def mypage(request:Request ):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    inputID = dict_form_data['user_ID']

    check_list = await collection_member.get_all()
    checks_list = [check.dict() for check in check_list]
    
    check_ID = False
    # pass
    for i in checks_list:
        if i['user_ID'] == inputID :
            check_ID = True
            break
    if check_ID:
        return templates.TemplateResponse(name="user/user_joincheck_IDcheck_fail.html", context={'request':request})
    else :
        return templates.TemplateResponse(name="user/user_joincheck_IDcheck_suc.html", context={'request':request})


# 회원가입 페이지 이메일 확인 페이지
    
@router.get("/user_joincheck_email", response_class=HTMLResponse) 
async def mypage(request:Request):
    pass
    return templates.TemplateResponse(name="user/user_joincheck_email.html", context={'request':request})

# 이메일 체킹
@router.post("/user_joincheck_emailcheck", response_class=HTMLResponse) 
async def mypage(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    inputemail = dict_form_data['user_email']

    check_list = await collection_member.get_all()
    checks_list = [check.dict() for check in check_list]

    check_email = False
    pass
    for i in checks_list:
        if i['user_email'] == inputemail :
            check_email = True
            break
    if check_email:
        return templates.TemplateResponse(name="user/user_joincheck_emailcheck_fail.html", context={'request':request})
    else :
        return templates.TemplateResponse(name="user/user_joincheck_emailcheck_suc.html", context={'request':request})

# 회원가입 성공 페이지
@router.get("/user_join_suc", response_class=HTMLResponse) 
async def mypage(request:Request):
    pass
    return templates.TemplateResponse(name="user/user_join_suc.html", context={'request':request})

@router.post("/user_join_suc", response_class=HTMLResponse) 
async def mypage(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    member = members(**dict_form_data)
    await collection_member.save(member)
    
    pass
    return templates.TemplateResponse(name="user/user_join_suc.html", context={'request':request})

# 회원가입 최종 확인 페이지

@router.get("/user_join_finalcheck", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_joincheck_ID.html", context={'request':request})

@router.post("/user_join_finalcheck", response_class=HTMLResponse) 
async def mypage(request:Request ):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d")
    # 이 시간을 item 객체의 'ques_time' 속성에 저장한다.
    dict_form_data['join_date'] = formatted_time
    inputID = dict_form_data['user_ID']
    inputEmail = dict_form_data['user_email']


    check_list = await collection_member.get_all()
    checks_list = [check.dict() for check in check_list]
    
    check_ID = False
    # pass
    for i in checks_list:
        if i['user_ID'] == inputID :
            check_ID = True
            break
        else:
            if i['user_email'] == inputEmail:
                check_ID = True
                break

    if check_ID:
        return templates.TemplateResponse(name="user/user_join_fail.html", context={'request':request})
    else :
        member = members(**dict_form_data)
        await collection_member.save(member)
        return templates.TemplateResponse(name="user/user_join_suc.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 마이 페이지
@router.get("/user_mypage", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_mypage.html", context={'request':request})

@router.post("/user_mypage", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_mypage.html", context={'request':request})


# 이메일로 아이디/비밀번호 찾기
@router.get("/user_infosearch", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_infosearch.html", context={'request':request})

@router.get("/user_searchcheck_email", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_searchcheck_email.html", context={'request':request})

@router.post("/user_searchcheck_emailcheck", response_class=HTMLResponse) 
async def mypage(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    inputemail = dict_form_data['user_email']

    check_list = await collection_member.get_all()
    checks_list = [check.dict() for check in check_list]


    member_info = {}
    check_member=False
    for member in checks_list:
        if member['user_email'] == inputemail:
            member_info = {
                "user_ID": member['user_ID'],  
                "user_pswd": member['user_pswd']  
            }
            check_member = True
            break

    if check_member:
        return templates.TemplateResponse("user/user_searchemail_found.html", context={'request': request, "member": member_info})
    else:
        return templates.TemplateResponse("user/user_searchemail_notfound.html", context={'request': request})

# 이용약관
@router.get("/user_privacypolicy", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_privacypolicy.html", context={'request':request})

@router.post("/user_privacypolicy", response_class=HTMLResponse) 
async def mypage(request:Request):
    return templates.TemplateResponse(name="user/user_privacypolicy.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# 찜 목록
@router.get("/user_mypage_like", response_class=HTMLResponse) 
async def mypage_like_get(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_like.html", context={'request':request})

@router.post("/user_mypage_like", response_class=HTMLResponse) 
async def mypage_like_post(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_like.html", context={'request':request})

# 내가 쓴 글

@router.get("/user_mypage_post", response_class=HTMLResponse) 
async def mypage_post_get(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_post.html", context={'request':request})

@router.post("/user_mypage_post", response_class=HTMLResponse) 
async def mypage_post_post(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_post.html", context={'request':request})

# 계정관리인증화면
@router.get("/user_mypage_account_check", response_class=HTMLResponse) 
async def mypage_account_check_get(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_account_check.html", context={'request':request})

@router.post("/user_mypage_account_check", response_class=HTMLResponse) 
async def mypage_account_check_post(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_account_check.html", context={'request':request})


# 계정관리 수정화면
@router.get("/user_mypage_account_reply/{object_id}") 
async def mypage_account_reply_get(request:Request,object_id : PydanticObjectId):
    user = await collection_member.get(object_id)
    return templates.TemplateResponse(name="user/user_mypage_account_reply.html", context={'request':request,"user" : user})

@router.post("/user_mypage_account_reply", response_class=HTMLResponse) 
async def mypage_account_reply_post(request:Request):
    await request.form()
    return templates.TemplateResponse(name="user/user_mypage_account_reply.html", context={'request':request})

# 프로그램 신청내역 화면
@router.get("/user_mypage_program", response_class=HTMLResponse) 
async def mypage_program_get(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_program.html", context={'request':request})

@router.post("/user_mypage_program", response_class=HTMLResponse) 
async def mypage_program_post(request:Request):
    return templates.TemplateResponse(name="user/user_mypage_program.html", context={'request':request})
