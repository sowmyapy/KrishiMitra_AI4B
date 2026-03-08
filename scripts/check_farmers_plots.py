"""
Quick script to check farmers and their plots in the database
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.database import SessionLocal
from src.models.farmer import Farmer, FarmPlot


def check_database():
    """Check farmers and plots in database"""
    db = SessionLocal()

    try:
        # Get all farmers
        farmers = db.query(Farmer).all()
        print(f"\n{'='*60}")
        print(f"Total Farmers: {len(farmers)}")
        print(f"{'='*60}\n")

        for farmer in farmers:
            print(f"Farmer ID: {farmer.farmer_id}")
            print(f"Phone: {farmer.phone_number}")
            print(f"Language: {farmer.preferred_language}")
            print(f"Timezone: {farmer.timezone}")

            # Get plots for this farmer
            plots = db.query(FarmPlot).filter(FarmPlot.farmer_id == farmer.farmer_id).all()
            print(f"Plots: {len(plots)}")

            if plots:
                for plot in plots:
                    print(f"  - Plot ID: {plot.plot_id}")
                    print(f"    Location: {plot.location}")
                    print(f"    Area: {plot.area_hectares} hectares")
                    print(f"    Crops: {plot.crop_types}")
            else:
                print("  ⚠ No plots found for this farmer")

            print("-" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    check_database()
