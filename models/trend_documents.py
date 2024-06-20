from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class trend_documents(Document):
    _id : Optional[str] = None
    post_title: Optional[str] = None
    post_file_name: Optional[str] = None
    post_contents: Optional[str] = None
  
    class Settings:
        name = "trend_documents"