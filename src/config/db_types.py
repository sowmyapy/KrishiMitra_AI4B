"""
Database type utilities for cross-database compatibility
"""
import json
import uuid

from sqlalchemy import JSON, String, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.dialects.postgresql import JSONB as PG_JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class UUID(TypeDecorator):
    """
    Platform-independent UUID type.

    Uses PostgreSQL's UUID type when available, otherwise uses String(36).
    """
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, str):
                return uuid.UUID(value)
            return value


class ARRAY(TypeDecorator):
    """
    Platform-independent ARRAY type.

    Uses PostgreSQL's ARRAY type when available, otherwise uses JSON/Text.
    """
    impl = Text
    cache_ok = True

    def __init__(self, item_type=String, *args, **kwargs):
        self.item_type = item_type
        super().__init__(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_ARRAY(self.item_type))
        else:
            return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            # Store as JSON string for SQLite
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            # Parse JSON string for SQLite
            if isinstance(value, str):
                return json.loads(value)
            return value


class JSONB(TypeDecorator):
    """
    Platform-independent JSONB type.

    Uses PostgreSQL's JSONB type when available, otherwise uses JSON/Text.
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_JSONB())
        else:
            return dialect.type_descriptor(JSON())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            # SQLite JSON type handles this automatically
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        # Both PostgreSQL and SQLite return parsed JSON
        return value


class Geography(TypeDecorator):
    """
    Platform-independent Geography type.

    Uses PostGIS Geography for PostgreSQL, Text (WKT format) for SQLite.
    """
    impl = Text
    cache_ok = True

    def __init__(self, geometry_type='POINT', srid=4326, *args, **kwargs):
        self.geometry_type = geometry_type
        self.srid = srid
        super().__init__(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            try:
                from geoalchemy2 import Geography as PG_Geography
                return dialect.type_descriptor(PG_Geography(geometry_type=self.geometry_type, srid=self.srid))
            except ImportError:
                # Fallback if geoalchemy2 not available
                return dialect.type_descriptor(Text())
        else:
            # For SQLite, store as "lat,lon" text
            return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            # For SQLite, convert WKT or geometry object to "lat,lon"
            # This is a simplified version - in production you'd want proper WKT handling
            if isinstance(value, str):
                return value
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            # For SQLite, return as-is (text format)
            return value
