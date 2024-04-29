from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from datetime import datetime

class program(Document):
    program_title: Optional[str] = None
    program_date: Optional[datetime] = None
    program_thumbnail: Optional[str] = None
    program_content: Optional[str] = None
  
    class Settings:
        name = "program_list"