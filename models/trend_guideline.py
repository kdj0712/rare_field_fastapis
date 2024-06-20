from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
import datetime

class trend_guideline(Document):
    _id : Optional[str] = None
    importance: Optional[str] = None
    post_cate: Optional[str] = None
    post_title: Optional[str] = None
    order_number: Optional[str] = None
    post_file_name: Optional[str] = None
    post_contents: Optional[str] = None
    date_legislation: Optional[datetime.date] = None
    date_start: Optional[datetime.date] = None
  
    class Settings:
        name = "trend_guideline"