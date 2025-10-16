from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class ExcelFileCreate(BaseModel):
    filename: str
    original_name: str
    file_size: int
    uploaded_by: str

class ExcelFileResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    file_size: int
    upload_date: datetime
    uploaded_by: str
    status: str
    processed_data: Optional[Any] = None

    class Config:
        orm_mode = True

class ExcelProcessResponse(BaseModel):
    message: str
    file_id: int
    total_rows: int
    processed_rows: int
    data_preview: list

    
class ExcelDeleteResponse(BaseModel):
    message: str
    file_id: int