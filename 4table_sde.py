from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import json

# Import your models along with the Base tracker class
from test import Books, ApiImportedData, Base  

app = FastAPI(title="SDE Spatial Database API")

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/api_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FIXED: This builds ONLY standard tables (Books, ApiImportedData) 
# and skips the unprivileged spatial PostGIS layers!
Base.metadata.create_all(bind=engine, tables=[
    Base.metadata.tables['books'],
    Base.metadata.tables['api_imported_data']
])

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
