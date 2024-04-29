from database.connection import Database
from fastapi import APIRouter, Request, FastAPI
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from beanie import PydanticObjectId
from typing import Optional
from datetime import datetime

app = FastAPI()
router = APIRouter()

# db 연결
from models.program_list import program
collection_manag_program = Database(program)

from models.empo_community import community
collection_empo_community = Database(community)

templates = Jinja2Templates(directory="templates/")

#### -------------------------------------------------------------------------------------------------------

# program
@router.get("/empo_program", response_class=HTMLResponse) 
async def empo_program_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_program.html", context={'request':request})

@router.post("/empo_program", response_class=HTMLResponse) 
async def empo_program_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_program.html", context={'request':request})

#### -------------------------------------------------------------------------------------------------------

# community
@router.get("/empo_community/{page_number}", response_class=HTMLResponse)
@router.get("/empo_community", response_class=HTMLResponse) 
async def empo_community_function(
    request:Request,
    page_number: Optional[int] = 1
    ):
    
    conditions = {}
    
    community_list, pagination = await collection_empo_community.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(
        name="empo/empo_community.html", 
        context={'request':request, 'pagination': pagination, 'communitys': community_list})

@router.post("/empo_community/{page_number}", response_class=HTMLResponse)
@router.post("/empo_community", response_class=HTMLResponse) 
async def empo_community_function(
    request:Request,
    page_number: Optional[int] = 1
    ):
    
    conditions = {}
    
    community_list, pagination = await collection_empo_community.getsbyconditionswithpagination(
    conditions, page_number
    )
    
    return templates.TemplateResponse(name="empo/empo_community.html", context={'request':request, 'communitys': community_list})

@router.get("/empo_community_write", response_class=HTMLResponse) 
async def empo_community_write_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_community_write.html", context={'request':request})

@router.post("/empo_community_write", response_class=HTMLResponse) 
async def empo_community_write_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_community_write.html", context={'request':request})

@router.get("/empo_community_read/{object_id}", response_class=HTMLResponse) 
async def empo_community_read_function(request:Request,
                                        object_id:PydanticObjectId):
    
    community_list = await collection_empo_community.get(object_id)
        
    return templates.TemplateResponse(name="empo/empo_community_read.html", context={'request':request, 'communitys':community_list})

@router.post("/empo_community_read/{object_id}", response_class=HTMLResponse) 
async def empo_community_read_function(request:Request):
    return templates.TemplateResponse(name="empo/empo_community_read.html", context={'request':request})
