"""
Módulo de Banco de Dados do Sistema de Triagem
"""

from .connection import DatabaseConnection
from .models import Base, Patient, Diagnosis, MedicalHistory

__all__ = [
    "DatabaseConnection",
    "Base",
    "Patient",
    "Diagnosis",
    "MedicalHistory",
]
