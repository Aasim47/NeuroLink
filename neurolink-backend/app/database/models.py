"""
SQLAlchemy ORM Models for NeuroLink
===================================
These models define the database schema. Tables are auto-created on startup
using `Base.metadata.create_all(engine)` — similar to Spring Boot's
`spring.jpa.hibernate.ddl-auto=update`.

Tables created:
  - patients
  - family_members
  - memories
  - routines
  - alerts
  - location_history
  - conversation_logs
  - safe_zones
  - photos
"""

from sqlalchemy import (
    Column, String, Integer, Float, Text, DateTime, JSON,
    ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    caregiver_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    relationship = Column(String(100))
    description = Column(Text)
    face_embedding = Column(JSON)  # stored as JSON array of floats
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Memory(Base):
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Routine(Base):
    __tablename__ = "routines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255))
    description = Column(Text)
    time = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    alert_type = Column(String(100))
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LocationHistory(Base):
    __tablename__ = "location_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    user_message = Column(Text)
    assistant_response = Column(Text)
    intent = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SafeZone(Base):
    __tablename__ = "safe_zones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    label = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_meters = Column(Float, default=200)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Photo(Base):
    __tablename__ = "photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text)
    description = Column(Text)
    embedding_vector = Column(Text)  # stored as pgvector string format
    created_at = Column(DateTime(timezone=True), server_default=func.now())
