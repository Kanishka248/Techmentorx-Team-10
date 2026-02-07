# users.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from ..database import get_connection

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

# ------------------------
# Utility functions
# ------------------------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------
# Schemas
# ------------------------

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # Donor / Volunteer / Admin

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    points: int

    class Config:
        orm_mode = True

# ------------------------
# Routes
# ------------------------

@router.post("/signup", response_model=UserResponse)
def signup(user: SignupRequest, db=Depends(get_db)):

    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    # your users table requires contact and location; insert empty strings for now
    cursor.execute(
        "INSERT INTO users (name, contact, location, role, email, password, points) VALUES (?,?,?,?,?,?,?)",
        (user.name, "", "", user.role, user.email, hashed, 0),
    )
    db.commit()
    user_id = cursor.lastrowid

    cursor.execute("SELECT id, name, email, role, points FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return {"id": row[0], "name": row[1], "email": row[2], "role": row[3], "points": row[4]}


@router.post("/login")
def login(user: LoginRequest, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, name, email, password, role, points FROM users WHERE email = ? AND role = ?",
        (user.email, user.role),
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = row[3]
    if not verify_password(user.password, stored_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "message": "Login successful",
        "user": {"id": row[0], "name": row[1], "email": row[2], "role": row[4], "points": row[5]}
    }
