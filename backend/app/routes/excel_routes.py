from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from controllers.excel_controller import save_uploaded_file, process_excel_file, get_user_files, get_all_files
from schemas.excel_schema import ExcelFileResponse, ExcelProcessResponse
from utils.auth_utils import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from controllers.excel_controller import (
    save_uploaded_file, 
    process_excel_file, 
    get_user_files, 
    get_all_files,
    delete_excel_file,  # ✅ Asegúrate de que esta importación esté presente
    get_file_by_id
)

security = HTTPBearer()
router = APIRouter(prefix="/excel", tags=["Archivos Excel"])

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    return payload.get("sub")  # Retorna el username

@router.post("/upload", response_model=ExcelFileResponse)
async def upload_excel_file(
    file: UploadFile = File(...),
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"📤 Usuario {username} subiendo archivo: {file.filename}")
    return save_uploaded_file(file, username, db)

@router.post("/process/{file_id}", response_model=ExcelProcessResponse)
async def process_file(
    file_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"🔄 Usuario {username} procesando archivo ID: {file_id}")
    return process_excel_file(file_id, db)

@router.get("/my-files", response_model=List[ExcelFileResponse])
async def get_my_files(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"📥 Usuario {username} solicitando sus archivos")
    return get_user_files(username, db)

@router.get("/all-files", response_model=List[ExcelFileResponse])
async def get_all_files_route(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"📥 Usuario {username} solicitando todos los archivos")
    return get_all_files(db)

    
@router.get("/{file_id}", response_model=ExcelFileResponse)
async def get_file(
    file_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"📥 Usuario {username} solicitando archivo ID: {file_id}")
    return get_file_by_id(file_id, username, db)

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"🗑️ Usuario {username} eliminando archivo ID: {file_id}")
    return delete_excel_file(file_id, username, db)