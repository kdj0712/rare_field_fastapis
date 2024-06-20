from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from datetime import datetime

class community(Document):
    _id : Optional[str] = None
    community_type: Optional[str] = None
    community_subject: Optional[str] = None
    community_title: Optional[str] = None
    community_related_diseases: Optional[str] = None
    community_content: Optional[str] = None
    community_writer: Optional[str] = None
    community_date : Optional[datetime] = None
  
    class Settings:
        name = "empo_community"
