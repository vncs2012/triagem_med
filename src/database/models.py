from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String(20), primary_key=True)
    name = Column(String(200), nullable=False)
    birth_date = Column(String(10), nullable=True)
    cpf = Column(String(14), unique=True, nullable=True)
    contact = Column(String(20), nullable=True)
    email = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    diagnoses = relationship("Diagnosis", back_populates="patient", lazy="dynamic")
    medical_history = relationship("MedicalHistory", back_populates="patient", lazy="dynamic")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "birth_date": self.birth_date,
            "cpf": self.cpf,
            "contact": self.contact,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name})>"


class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(String(20), primary_key=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    image_path = Column(String(500), nullable=True)
    classification = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    priority = Column(String(20), nullable=False)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), default="system")
    
    patient = relationship("Patient", back_populates="diagnoses")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "image_path": self.image_path,
            "classification": self.classification,
            "confidence": self.confidence,
            "priority": self.priority,
            "notes": self.notes,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "created_by": self.created_by,
        }
    
    def __repr__(self):
        return f"<Diagnosis(id={self.id}, classification={self.classification}, priority={self.priority})>"


class MedicalHistory(Base):
    __tablename__ = "medical_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(20), ForeignKey("patients.id"), nullable=False)
    description = Column(Text, nullable=False)
    condition_type = Column(String(100), nullable=True)
    date_recorded = Column(DateTime, default=datetime.utcnow)
    recorded_by = Column(String(100), nullable=True)
    
    patient = relationship("Patient", back_populates="medical_history")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "description": self.description,
            "condition_type": self.condition_type,
            "date_recorded": self.date_recorded.isoformat() if self.date_recorded else None,
            "recorded_by": self.recorded_by,
        }
    
    def __repr__(self):
        return f"<MedicalHistory(id={self.id}, patient_id={self.patient_id})>"
