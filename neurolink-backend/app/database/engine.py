"""
SQLAlchemy Engine & Auto-Table Creation
========================================
Connects directly to the Supabase PostgreSQL database and auto-creates
all tables defined in models.py on startup.

This is the Python equivalent of Spring Boot's:
    spring.jpa.hibernate.ddl-auto=update

Usage:
    from app.database.engine import init_db
    init_db()  # call once at startup
"""

import os
from sqlalchemy import create_engine
from app.database.models import Base

# ─────────────────────────────────────────────────────────────
# Build the PostgreSQL connection URL from the Supabase URL
#
# Supabase URL format:  https://<project-ref>.supabase.co
# PostgreSQL format:    postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres
#
# You need to set DATABASE_URL in your .env file.
# Find it in: Supabase Dashboard → Settings → Database → Connection string → URI
# ─────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set!\n"
        "Add it to your .env file. You can find it in:\n"
        "  Supabase Dashboard → Settings → Database → Connection string (URI)\n"
        "Example: postgresql://postgres.[ref]:[password]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
    )

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """
    Create all tables in the database (if they don't exist).
    
    This is equivalent to Spring Boot's `ddl-auto=update`:
      - If a table does NOT exist → it is CREATED automatically
      - If a table already EXISTS → it is SKIPPED (no data loss)
      - It does NOT delete or modify existing tables/columns
    """
    print("🔧 Auto-creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
