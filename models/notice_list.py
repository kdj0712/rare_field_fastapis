from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from datetime import datetime

class notice(Document):
    notice_title: Optional[str] = None
    notice_date: Optional[datetime] = None
    notice_type: Optional[str] = None
    notice_content: Optional[str] = None
    
    class Settings:
        name = "notice_list"