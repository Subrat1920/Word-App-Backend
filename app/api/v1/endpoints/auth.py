from fastapi import APIRouter, HTTPException
from app.schemas.user_schemas import UserCreate, UserLogin
from app.core.database import SessionLocal
from app.models.models import User
from passlib.context import CryptContext
import hashlib

from app.core.security import create_access_token
from fastapi import HTTPException
import hashlib

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ NEW: Safe password hashing
def hash_password(password: str):
    sha = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    sha = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha, hashed_password)


@router.post("/auth/signup")
def signup(user: UserCreate):
    db = SessionLocal()

    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ FIXED hashing
    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

print("SIGNUP FUNCTION HIT")




@router.post("/auth/login")
def login(user: UserLogin):
    db = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "name": db_user.name
    }