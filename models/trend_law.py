from typing import Optional, List
from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class trend_law(Document):
    law_name: Optional[str] = None
    promulgation_number: Optional[str] = None
    promulgation_date : Optional[datetime] = None
    start_date : Optional[datetime] = None
    link : Optional[str] = None

    class Settings:
        name = "trend_law"