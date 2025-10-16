import os
import shutil
import pandas as pd
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from models.excel_model import ExcelFile
from schemas.excel_schema import ExcelFileCreate, ExcelFileResponse
from datetime import datetime
import traceback

# Configuración
UPLOAD_DIR = "uploads/excel"
ALLOWED_EXTENSIONS = {'.xls', '.xlsx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Crear directorio si no existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile, username: str, db: Session):
    try:
        # Validar extensión
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se permiten archivos Excel (.xls, .xlsx)"
            )

        # Validar tamaño
        file.file.seek(0, 2)  # Ir al final del archivo
        file_size = file.file.tell()
        file.file.seek(0)  # Volver al inicio

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo es demasiado grande. Máximo: {MAX_FILE_SIZE//1024//1024}MB"
            )

        # Generar nombre único
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{username}_{timestamp}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Guardar en base de datos
        db_file = ExcelFile(
            filename=safe_filename,
            original_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            uploaded_by=username,
            status="pending"
        )
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file

    except Exception as e:
        print(f"💥 Error al guardar archivo: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar archivo: {str(e)}"
        )

def process_excel_file(file_id: int, db: Session):
    try:
        # Buscar archivo en BD
        db_file = db.query(ExcelFile).filter(ExcelFile.id == file_id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Leer archivo Excel
        df = pd.read_excel(db_file.file_path)
        
        # Convertir a diccionario para almacenar
        processed_data = df.to_dict('records')
        total_rows = len(processed_data)
        
        # Actualizar estado en BD
        db_file.processed_data = processed_data
        db_file.status = "processed"
        db.commit()

        # Preparar vista previa (primeras 5 filas)
        data_preview = processed_data[:5]

        return {
            "message": "Archivo procesado exitosamente",
            "file_id": file_id,
            "total_rows": total_rows,
            "processed_rows": len(processed_data),
            "data_preview": data_preview
        }

    except Exception as e:
        # Actualizar estado a error
        db_file.status = "error"
        db.commit()
        
        print(f"💥 Error al procesar Excel: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar archivo Excel: {str(e)}"
        )

def get_user_files(username: str, db: Session):
    return db.query(ExcelFile).filter(ExcelFile.uploaded_by == username).order_by(ExcelFile.upload_date.desc()).all()

def get_all_files(db: Session):
    return db.query(ExcelFile).order_by(ExcelFile.upload_date.desc()).all()

def get_file_by_id(file_id: int, username: str, db: Session):
    """Obtener un archivo específico por ID con verificación de permisos"""
    db_file = db.query(ExcelFile).filter(ExcelFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Verificar permisos (solo el dueño o admin puede ver)
    if db_file.uploaded_by != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este archivo"
        )
    
    return db_file

def delete_excel_file(file_id: int, username: str, db: Session):
    try:
        # Buscar el archivo en la base de datos
        db_file = db.query(ExcelFile).filter(ExcelFile.id == file_id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        # Verificar que el usuario que intenta eliminar es el que lo subió
        if db_file.uploaded_by != username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para eliminar este archivo"
            )

        # Eliminar el archivo físico del sistema de archivos
        if os.path.exists(db_file.file_path):
            os.remove(db_file.file_path)
            print(f"✅ Archivo físico eliminado: {db_file.file_path}")

        # Eliminar el registro de la base de datos
        db.delete(db_file)
        db.commit()

        return {"message": "Archivo eliminado exitosamente", "file_id": file_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"💥 Error al eliminar archivo: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar archivo: {str(e)}"
        )