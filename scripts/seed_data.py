"""
Seed database with sample data for testing
"""
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging

from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.config.logging_config import setup_logging
from src.models.farmer import Farmer, FarmPlot

setup_logging()
logger = logging.getLogger(__name__)


def create_sample_farmers(db: Session, count: int = 10):
    """Create sample farmers"""
    logger.info(f"Creating {count} sample farmers...")

    languages = ["hi", "bn", "te", "mr", "ta", "gu", "kn", "ml", "pa", "or"]
    timezones = ["Asia/Kolkata", "Asia/Kolkata", "Asia/Kolkata"]

    farmers = []
    for i in range(count):
        farmer = Farmer(
            phone_number=f"+91{9000000000 + i}",
            preferred_language=random.choice(languages),
            timezone=random.choice(timezones),
            registration_date=datetime.utcnow() - timedelta(days=random.randint(1, 365))
        )
        db.add(farmer)
        farmers.append(farmer)

    db.commit()
    logger.info(f"✓ Created {count} farmers")
    return farmers


def create_sample_farm_plots(db: Session, farmers: list, plots_per_farmer: int = 2):
    """Create sample farm plots"""
    logger.info(f"Creating {plots_per_farmer} plots per farmer...")

    crop_types_options = [
        ["wheat", "rice"],
        ["cotton"],
        ["sugarcane"],
        ["maize", "soybean"],
        ["rice"],
        ["wheat"],
        ["vegetables"],
    ]

    # Sample locations in India (lat, lon)
    locations = [
        (28.6139, 77.2090),  # Delhi
        (19.0760, 72.8777),  # Mumbai
        (13.0827, 80.2707),  # Chennai
        (22.5726, 88.3639),  # Kolkata
        (12.9716, 77.5946),  # Bangalore
        (17.3850, 78.4867),  # Hyderabad
        (23.0225, 72.5714),  # Ahmedabad
        (18.5204, 73.8567),  # Pune
    ]

    total_plots = 0
    for farmer in farmers:
        for _ in range(plots_per_farmer):
            lat, lon = random.choice(locations)
            # Add some random offset
            lat += random.uniform(-0.5, 0.5)
            lon += random.uniform(-0.5, 0.5)

            plot = FarmPlot(
                farmer_id=farmer.farmer_id,
                location=f"POINT({lon} {lat})",
                area_hectares=round(random.uniform(0.5, 5.0), 2),
                crop_types=random.choice(crop_types_options),
                planting_date=datetime.utcnow().date() - timedelta(days=random.randint(30, 120)),
                expected_harvest_date=datetime.utcnow().date() + timedelta(days=random.randint(30, 90))
            )
            db.add(plot)
            total_plots += 1

    db.commit()
    logger.info(f"✓ Created {total_plots} farm plots")


def main():
    """Seed database with sample data"""
    logger.info("Seeding database with sample data...")

    db = SessionLocal()
    try:
        # Create sample data
        farmers = create_sample_farmers(db, count=10)
        create_sample_farm_plots(db, farmers, plots_per_farmer=2)

        logger.info("✓ Database seeded successfully!")
        logger.info(f"  - {len(farmers)} farmers")
        logger.info(f"  - {len(farmers) * 2} farm plots")

        return 0
    except Exception as e:
        logger.error(f"✗ Failed to seed database: {e}")
        db.rollback()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
