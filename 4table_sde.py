from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import json

# Import your database definitions from your test.py file
from test import Books, ApiImportedData  

app = FastAPI(title="SDE Spatial Database API")

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/api_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Keep your endpoint functions for /books, /imported-data, and /india-outline below exactly as they are...


# 1. Endpoint for the Books Table
@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    """Fetches all rows from the books catalog."""
    return db.query(Books).all()

# 2. Endpoint for the API Imported Data Table
@app.get("/imported-data")
def get_imported_data(db: Session = Depends(get_db)):
    """Fetches records inside the api_imported_data table."""
    return db.query(ApiImportedData).all()

# 3. Endpoint for the India Outline Spatial Table
# 3. Endpoint for the India Outline Spatial Table (With Pagination)
#@app.get("/india-outline")
@app.get("/india-outline")
def get_india_outline(limit: int = 10, offset: int = 0):
    """
    Fetches map row attributes safely. 
    Geometry coordinates are excluded to prevent Swagger UI browser crashes.
    """
    output = []
    
    with engine.raw_connection() as conn:
        with conn.cursor() as cursor:
            # FIXED: Removed ST_AsGeoJSON(geom) entirely. We only select text attributes.
            sql_query = """
                SELECT id, "STATE"
                FROM "India_Outline" 
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql_query, (limit, offset))
            raw_results = cursor.fetchall()
            
            for row in raw_results:
                row_id, state = row
                
                output.append({
                    "id": row_id,
                    "state": state,
                    "geometry": "Excluded to prevent browser crash"
                })
                
    return output