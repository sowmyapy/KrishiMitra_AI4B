"""Debug advisory columns"""
import sys
sys.path.insert(0, '.')

from src.models.advisory import Advisory
from sqlalchemy import inspect

# Get the mapper for Advisory
mapper = inspect(Advisory)

print("Advisory model columns:")
for column in mapper.columns:
    print(f"  {column.name}: {column.type} (nullable={column.nullable})")

print("\nChecking if advisory_text and risk_score are in the model:")
print(f"  advisory_text: {hasattr(Advisory, 'advisory_text')}")
print(f"  risk_score: {hasattr(Advisory, 'risk_score')}")
