from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os  # Added to read system settings

# Import only your simple text models
from test import Books, ApiImportedData  

app = FastAPI(title="SDE Spatial Database API")

# FIXED: This reads your Render cloud database URL first, 
# and only uses localhost as a backup fallback for your laptop testing!
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/api_db")

engine = create_engine(DATABASE_URL)

# Safe raw SQL table creation block - No GeoAlchemy or permission issues!
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

@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Books).all()

@app.get("/imported-data")
def get_imported_data(db: Session = Depends(get_db)):
    return db.query(ApiImportedData).all()
