from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class academicinfo(Document):
    _id : Optional[str] = None
    acade_title: Optional[str] = None
    acade_content: Optional[str] = None
  
    class Settings:
        name = "academicinfo"