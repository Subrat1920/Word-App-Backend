from sqlalchemy import text
from app.core.database import engine

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'users';
    """))
    
    for row in result:
        print(row[0])