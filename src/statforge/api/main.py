from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from statforge.db.session import get_db

app = FastAPI(title="StatForge API")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Test DB connection
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": str(e)}

@app.get("/")
def root():
    return {"message": "Welcome to StatForge API"}
