from typing import Optional, List, Union

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
import datetime

class info_academicinfo_Riss(Document):
    research_title: Optional[str] = None
    research_url: Optional[str] = None
    research_author: Optional[str] = None
    research_institution: Optional[str] = None
    research_name: Optional[str] = None
    research_volumn: Optional[str] = None
    research_year: Optional[int] = None
    research_language: Optional[str] = None
    research_subject: Optional[Union[str, int, float, bool]] = None
    research_type: Optional[Union[str, int, float, bool]] = None
    research_page: Optional[str] = None
  
    class Settings:
        name = "info_academicinfo_Riss"




class info_academicinfo_eng(Document):
    title: Optional[str] = None
    Article_date: Optional[str] = None
    abstract: Optional[str] = None
    research_date: Optional[int] = None

    class Settings:
        name = "info_academicinfo_ENG"