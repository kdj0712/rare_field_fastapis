from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class diseases(Document):
    dise_id : Optional[str] = None
    dise_KCD_code : Optional[str] = None
    dise_spc_code : Optional[str] = None
    dise_group : Optional[str] = None
    dise_name_kr: Optional[str] = None
    dise_name_en: Optional[str] = None
    dise_support: Optional[str] = None
    dise_url : Optional[str] = None
  
    class Settings:
        name = "info_rarediseases"