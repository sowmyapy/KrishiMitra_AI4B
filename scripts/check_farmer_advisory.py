"""
Check farmer and advisory status
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.database import SessionLocal
from src.models.farmer import Farmer
from src.models.advisory import Advisory

db = SessionLocal()

# Find farmer
farmer = db.query(Farmer).filter(Farmer.phone_number.like("%8095666788%")).first()

if farmer:
    print(f"Farmer ID: {farmer.farmer_id}")
    print(f"Phone: {farmer.phone_number}")
    print(f"Language: {farmer.preferred_language}")
    
    # Get latest advisory
    advisory = db.query(Advisory).filter(
        Advisory.farmer_id == farmer.farmer_id
    ).order_by(Advisory.created_at.desc()).first()
    
    if advisory:
        print(f"\nLatest Advisory:")
        print(f"ID: {advisory.advisory_id}")
        print(f"Risk Score: {advisory.risk_score}")
        print(f"Text length: {len(advisory.advisory_text) if advisory.advisory_text else 0}")
        print(f"Text preview: {advisory.advisory_text[:200] if advisory.advisory_text else 'NULL'}")
        print(f"Created: {advisory.created_at}")
    else:
        print("\nNo advisory found")
else:
    print("Farmer not found")

db.close()
