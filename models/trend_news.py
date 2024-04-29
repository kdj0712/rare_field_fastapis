from typing import Optional, List
from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class news_trends(Document):
    news_title: Optional[str] = None
    news_datetime: Optional[datetime] = None
    news_contents : Optional[str] = None
    news_url : Optional[str] = None
    news_topic : Optional[str] = None
    news_paper : Optional[str] = None
    news_clicks : Optional[int] = None
    news_image : Optional[str] = None

    class Settings:
        name = "trend_news"