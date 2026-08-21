from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os

# Import your tracking classes from your test.py file
from test import Books, ApiImportedData  

app = FastAPI(title="SDE Spatial Database API")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/api_db")
engine = create_engine(DATABASE_URL)

# Safe raw SQL table creation block
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR,
            author VARCHAR
        );
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS api_imported_data (
            external_id TEXT PRIMARY KEY,
            imported_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            srid BIGINT,
            srtext TEXT,
            auth_name TEXT,
            auth_srid BIGINT,
            proj4text TEXT
        );
    """))
    conn.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. GET Endpoint - Fetch books
@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Books).all()

# 2. NEW: POST Endpoint - Add a book into your live cloud database
@app.post("/books")
def create_book(title: str, author: str, db: Session = Depends(get_db)):
    """Inserts a brand new record into your live production table!"""
    new_book = Books(title=title, author=author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# 3. GET Endpoint - Fetch imported data
@app.get("/imported-data")
def get_imported_data(db: Session = Depends(get_db)):
    return db.query(ApiImportedData).all()
