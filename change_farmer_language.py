"""
Change farmer language
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config.database import SessionLocal
from src.models.farmer import Farmer

db = SessionLocal()

# Find farmer
farmer = db.query(Farmer).filter(Farmer.phone_number.like("%8095666788%")).first()

if farmer:
    print(f"Current language: {farmer.preferred_language}")
    
    # Change to Telugu
    farmer.preferred_language = "te"
    db.commit()
    
    print(f"Updated language to: {farmer.preferred_language}")
    print("\nNow generate a new advisory and make a call to test Telugu!")
else:
    print("Farmer not found")

db.close()
