from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import SessionLocal
router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/health/db")
def db_check():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1")) 
        return {"status": "db connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()