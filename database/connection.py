from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId

import random

from models.academicinfo import academicinfo
from models.info_rarediseases import diseases
from models.institution import Institutions
from models.user_member import members
from models.trend_news import news_trends
from models.other_QnA import QnA
from models.manag_notice_list import notice
from models.program_list import program
from models.empo_community import community
from models.trend_documents import trend_documents
from models.trend_guideline import trend_guideline
from models.trend_law import trend_law
from models.trend_site import trend_site
from models.info_academicinfo import info_academicinfo_Riss,info_academicinfo_eng

import os

from motor.motor_asyncio import AsyncIOMotorClient

from pydantic_settings import BaseSettings

from utils.paginations import Paginations

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    container_prefix: Optional[str] = None
    API_KEY : Optional[str] = None
    PUBLIC_API_KEY : Optional[str] = None
    id : Optional[str] = None
    pw : Optional[str] = None
    async def initialize_database(self):
        if self.DATABASE_URL is not None:
            client = AsyncIOMotorClient(self.DATABASE_URL)
            await init_beanie(database=client.get_default_database(),
                              document_models=[academicinfo, diseases, Institutions,
                                                members, news_trends, QnA, program,
                                                notice, community, trend_documents,
                                                trend_guideline, trend_law,
                                                trend_site, info_academicinfo_Riss,info_academicinfo_eng])

    class Config:
        env_file = ".env"

class Database:
    # model 즉 collection
    def __init__(self, model) -> None:
        self.model = model
        pass       

    # 전체 리스트
    async def get_all(self) :
        documents = await self.model.find_all().to_list()   # find({})
        pass
        return documents
    
    # 상세 보기
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)  # find_one()
        if doc:
            return doc
        return False    
    
    # 저장
    async def save(self, document) -> None:
        await document.create()
        return None   
    
    # 업데이트
    async def update_one(self, id: PydanticObjectId, dic) -> Any:
        doc = await self.model.get(id)
        if doc:
            for key, value in dic.items():
                setattr(doc, key, value)
            await doc.save()
            return True
        return False
    
        # 삭제
    # async def delete(self, id: PydanticObjectId) -> Any:
    #     from pymongo import MongoClient
    #     from dotenv import load_dotenv
    #     import os

    #     load_dotenv()
    #     DB_URI = os.getenv('DB_URI')
    #     # MongoDB 연결 설정
    #     client = MongoClient(DB_URI)
    #     db = client['teamplays']
    #     collection = db['QnA']
    #     deleted_doc = await collection.delete_one({"_id": id})
    #     if deleted_doc:
    #         return True
    #     return False
     
    async def delete_one(self, id: PydanticObjectId) -> bool:
        doc = await self.model.get(id)
        if doc:
            await doc.delete()
            return True
        return False

    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict) -> [Any]:
        documents = await self.model.find(conditions).to_list()  # find({})
        if documents:
            return documents
        return []    
    
    # async def getsbyconditions_top4(self, conditions:dict) -> [Any]:
    #     documents = await self.model.find(conditions).sort('news_when').limit(4).to_list(length=4)  # find({})
    #     if documents:
    #         return documents
    #     return []

    # 뉴스 추천 상위 12개 중 random으로 보여주기
    async def getsbyconditions_top4(self, conditions: dict) -> [Any]:
        documents = await self.model.find(conditions).sort('news_when').limit(12).to_list(length=12)  # find({})
        random.shuffle(documents)  # 불러온 데이터를 랜덤하게 섞습니다.
        result = [documents[i:i+4] for i in range(0, len(documents), 4)]  # 리스트를 4개씩 묶어서 결과를 생성합니다.
        i = random.randrange(0,3)
        return result[i]
    
    async def getsbyconditionswithpagination(self
                                             , conditions:dict, page_number, records_per_page=10) -> [Any]:
        # find({})
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number, records_per_page=records_per_page)
        documents = await self.model.find(conditions).skip(pagination.start_record_number-1).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return documents, pagination  

    async def gbcwp_reverse(self, conditions: dict, page_number, records_per_page=10) -> [Any]:
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number, records_per_page=records_per_page)
        # 내림차순으로 정렬하기 위해 sort({_id: -1})를 적용합니다.
        documents = await self.model.find(conditions).sort([('_id', -1)]).skip(pagination.start_record_number-1).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return documents, pagination
    
    async def gbcwp_reverse_date(self, conditions: dict, page_number, records_per_page=10) -> [Any]:
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number, records_per_page=records_per_page)
        # 내림차순으로 정렬하기 위해 sort({_id: -1})를 적용합니다.
        documents = await self.model.find(conditions).sort([('news_datetime', -1)]).skip(pagination.start_record_number-1).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return documents, pagination
    async def gbcwp_reverse_year(self, conditions: dict, page_number, records_per_page=10) -> [Any]:
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number, records_per_page=records_per_page)
        # 내림차순으로 정렬하기 위해 sort({_id: -1})를 적용합니다.
        documents = await self.model.find(conditions).sort([('research_year', -1)]).skip(pagination.start_record_number-1).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return documents, pagination
    async def gbcwp_reverse_year(self, conditions: dict, page_number, records_per_page=10) -> [Any]:
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number, records_per_page=records_per_page)
        # 내림차순으로 정렬하기 위해 sort({_id: -1})를 적용합니다.
        documents = await self.model.find(conditions).sort([('research_date', -1)]).skip(pagination.start_record_number-1).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return documents, pagination


if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(members)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass