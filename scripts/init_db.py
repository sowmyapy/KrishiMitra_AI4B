"""
Database initialization script
Creates all tables and optionally seeds initial data
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging

from src.config.database import Base, engine
from src.config.logging_config import setup_logging
from src.config.settings import settings

# Import all models to register them with Base

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database tables"""
    logger.info("Initializing database...")
    logger.info(f"Database URL: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'local'}")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully")

        # List created tables
        tables = Base.metadata.tables.keys()
        logger.info(f"✓ Created {len(tables)} tables:")
        for table in sorted(tables):
            logger.info(f"  - {table}")

        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {e}")
        return False


def drop_database():
    """Drop all database tables (use with caution!)"""
    logger.warning("Dropping all database tables...")

    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("✓ Database tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to drop database: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating (WARNING: destroys all data)"
    )

    args = parser.parse_args()

    if args.drop:
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            drop_database()
        else:
            logger.info("Operation cancelled")
            sys.exit(0)

    success = init_database()
    sys.exit(0 if success else 1)
