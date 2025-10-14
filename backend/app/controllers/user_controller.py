from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate, UserLogin
from utils.auth_utils import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from models.user_model import User

def get_all_users(db: Session):
    return db.query(User).all()

# ... el resto de tus funciones (register_user, login_user)
def register_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserLogin
from utils.auth_utils import verify_password, create_access_token
import traceback

def login_user(db: Session, credentials: UserLogin):
    try:
        user = db.query(User).filter(User.username == credentials.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )

        if not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta"
            )

        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        # ⚠️ Deja pasar las HTTPException sin atraparlas
        raise
    except Exception as e:
        print("💥 ERROR DETECTADO EN login_user:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno: {type(e).__name__} - {str(e)}")
