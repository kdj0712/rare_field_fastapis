from typing import Optional, List, Union
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from datetime import datetime

class members(Document):
    user_ID: Optional[Union[str, int, float, bool]] = None
    user_pswd: Optional[Union[str, int, float, bool]] = None
    user_email: Optional[EmailStr] = None    
    user_name: Optional[Union[str, int, float, bool]] = None
    user_phone : Optional[Union[str, int, float, bool]] = None
    user_birth : Optional[Union[str, int, float, bool]] = None
    user_postcode : Optional[Union[str, int, float, bool]] = None
    user_address : Optional[Union[str, int, float, bool]] = None
    user_detailed_address : Optional[Union[str, int, float, bool]] = None
    user_sex : Optional[Union[str, int, float, bool]] = None
    path_select : Optional[Union[str, int, float, bool]] = None
    user_who : Optional[Union[str, int, float, bool]] = None
    ralated_diseases : Optional[Union[str, int, float, bool]] = None
    hope_info : Optional[Union[str, int, float, bool]] = None
    join_date : Optional[datetime] = None
    
    class Settings:
        name = "user_member"