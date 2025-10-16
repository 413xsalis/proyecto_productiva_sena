from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from core.database import Base
from datetime import datetime

class ExcelFile(Base):
    __tablename__ = "excel_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(String(50), nullable=False)
    processed_data = Column(JSON, nullable=True)  # Para almacenar datos procesados
    status = Column(String(20), default="pending")  # pending, processed, error