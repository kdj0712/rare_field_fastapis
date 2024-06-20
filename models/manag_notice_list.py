from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from datetime import datetime

class notice(Document):
    _id : Optional[str] = None
    notice_title: Optional[str] = None
    notice_date: Optional[datetime] = None
    notice_type: Optional[str] = None
    notice_content: Optional[str] = None
    
    class Settings:
        name = "manag_notice_list"