from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter(prefix="/mentor", tags=["Mentor"])

# =========================
# Database Connection
# =========================
def get_connection():
    return sqlite3.connect("social_mentor.db")

# =========================
# Mentor Input Model
# =========================
class MentorCreate(BaseModel):
    name: str
    contact: str
    location: str
    email: str
    password: str

# =========================
# Add Mentor (Admin Only logic later)
# =========================
@router.post("/add")
def add_mentor(mentor: MentorCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, contact, location, role, email, password)
            VALUES (?, ?, ?, 'Mentor', ?, ?)
        """, (
            mentor.name,
            mentor.contact,
            mentor.location,
            mentor.email,
            mentor.password
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Mentor already exists")

    conn.close()
    return {"message": "Mentor added successfully"}

# =========================
# Get All Mentors
# =========================
@router.get("/all")
def get_all_mentors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, contact, location, email, points
        FROM users
        WHERE role = 'Mentor'
    """)

    mentors = cursor.fetchall()
    conn.close()

    return mentors

# =========================
# Get Mentor By ID
# =========================
@router.get("/{mentor_id}")
def get_mentor_by_id(mentor_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, contact, location, email, points
        FROM users
        WHERE id = ? AND role = 'Mentor'
    """, (mentor_id,))

    mentor = cursor.fetchone()
    conn.close()

    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")

    return mentor

# =========================
# Delete Mentor
# =========================
@router.delete("/delete/{mentor_id}")
def delete_mentor(mentor_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ? AND role = 'Mentor'
    """, (mentor_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Mentor not found")

    conn.commit()
    conn.close()

    return {"message": "Mentor deleted successfully"}
