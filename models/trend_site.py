from typing import Optional, List
from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class trend_site(Document):
    site_link: Optional[str] = None
    site_name: Optional[str] = None
    site_where : Optional[str] = None

    class Settings:
        name = "trend_site"