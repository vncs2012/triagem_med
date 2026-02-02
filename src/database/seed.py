import random
import logging
from datetime import datetime, timedelta
from .connection import DatabaseConnection
from .models import Patient, Diagnosis, MedicalHistory

logger = logging.getLogger(__name__)

class Seed():
    def __init__(self):
        self.database = DatabaseConnection()

    def seed_patients(self):
        """
        Cria pacientes de exemplo.
        """
        patients = [
            Patient(
            id="P001",
            name="Maria Silva Santos",
            birth_date="1985-03-15",
            cpf="123.456.789-00",
            contact="(11) 99999-1234",
            email="maria.silva@email.com",
            address="Rua das Flores, 123 - São Paulo, SP"
        ),
        Patient(
            id="P002",
            name="João Pedro Oliveira",
            birth_date="1972-08-22",
            cpf="987.654.321-00",
            contact="(11) 98888-5678",
            email="joao.oliveira@email.com",
            address="Av. Brasil, 456 - São Paulo, SP"
        ),
        Patient(
            id="P003",
            name="Ana Carolina Ferreira",
            birth_date="1990-11-08",
            cpf="456.789.123-00",
            contact="(21) 97777-9012",
            email="ana.ferreira@email.com",
            address="Rua do Sol, 789 - Rio de Janeiro, RJ"
        ),
        Patient(
            id="P004",
            name="Carlos Eduardo Lima",
            birth_date="1965-05-30",
            cpf="321.654.987-00",
            contact="(31) 96666-3456",
            email="carlos.lima@email.com",
            address="Praça da Liberdade, 321 - Belo Horizonte, MG"
        ),
        Patient(
            id="P005",
            name="Beatriz Souza Costa",
            birth_date="1998-02-14",
            cpf="654.321.789-00",
            contact="(51) 95555-7890",
            email="beatriz.costa@email.com",
            address="Rua dos Andradas, 654 - Porto Alegre, RS"
        ),
    ]
    
        with self.database.get_session() as session:
            for patient in patients:
                existing = session.query(Patient).filter(Patient.id == patient.id).first()
                if not existing:
                    session.add(patient)
                    logger.info(f"Paciente criado: {patient.name}")
        
            return len(patients)


    def seed_diagnoses(self):
        """
        Cria diagnósticos de exemplo.
        """
        diagnoses_data = [
            {
            "id": "D0001",
            "patient_id": "P001",
            "classification": "NORMAL",
            "confidence": 0.92,
            "priority": "BAIXA",
            "notes": "Exame de rotina, sem alterações"
        },
        {
            "id": "D0002",
            "patient_id": "P002",
            "classification": "PNEUMONIA",
            "confidence": 0.87,
            "priority": "ALTA",
            "notes": "Detectada opacidade no pulmão direito"
        },
        {
            "id": "D0003",
            "patient_id": "P003",
            "classification": "NORMAL",
            "confidence": 0.78,
            "priority": "MÉDIA",
            "notes": "Resultado inconclusivo, recomendada reavaliação"
        },
        {
            "id": "D0004",
            "patient_id": "P004",
            "classification": "PNEUMONIA",
            "confidence": 0.95,
            "priority": "ALTA",
            "notes": "Alta probabilidade de pneumonia, encaminhado para UTI"
        },
        {
            "id": "D0005",
            "patient_id": "P001",
            "classification": "NORMAL",
            "confidence": 0.88,
            "priority": "BAIXA",
            "notes": "Acompanhamento de rotina"
        },
    ]
    
        with self.database.get_session() as session:
            for i, diag_data in enumerate(diagnoses_data):
                existing = session.query(Diagnosis).filter(Diagnosis.id == diag_data["id"]).first()
                if not existing:
                    # Criar com timestamp variado
                    timestamp = datetime.now() - timedelta(days=random.randint(1, 30))
                    
                    diagnosis = Diagnosis(
                        id=diag_data["id"],
                        patient_id=diag_data["patient_id"],
                        image_path=f"/data/sample_images/xray_{i+1}.png",
                        classification=diag_data["classification"],
                        confidence=diag_data["confidence"],
                        priority=diag_data["priority"],
                        notes=diag_data["notes"],
                        timestamp=timestamp
                    )
                    session.add(diagnosis)
                    logger.info(f"Diagnóstico criado: {diagnosis.id}")
        
        return len(diagnoses_data)


    def seed_medical_history(self):
        """
        Cria histórico médico de exemplo.
        """
        history_data = [
            {
            "patient_id": "P001",
            "description": "Alergia a Penicilina",
            "condition_type": "alergia"
        },
        {
            "patient_id": "P002",
            "description": "Hipertensão arterial controlada",
            "condition_type": "doença crônica"
        },
        {
            "patient_id": "P002",
            "description": "Diabetes tipo 2",
            "condition_type": "doença crônica"
        },
        {
            "patient_id": "P004",
            "description": "Ex-fumante (parou há 5 anos)",
            "condition_type": "histórico"
        },
        {
            "patient_id": "P004",
            "description": "DPOC leve",
            "condition_type": "doença crônica"
        },
    ]
    
        with self.database.get_session() as session:
            for hist_data in history_data:
                history = MedicalHistory(
                    patient_id=hist_data["patient_id"],
                    description=hist_data["description"],
                    condition_type=hist_data["condition_type"],
                    recorded_by="sistema"
                )
                session.add(history)
                logger.info(f"Histórico criado para paciente: {hist_data['patient_id']}")
    
        return len(history_data)


    def run_seed(self):
        """
        Executa todos os seeds.
        """
        logging.basicConfig(level=logging.INFO)
        
        print("\n" + "=" * 50)
        print("SEED DO BANCO DE DADOS")
        print("=" * 50 + "\n")
        
        print("📦 Inicializando banco de dados...")
        self.database.init_database()
    
        print("\n👤 Criando pacientes...")
        n_patients = self.seed_patients()
        print(f"   ✅ {n_patients} pacientes")
    
        print("\n🏥 Criando diagnósticos...")
        n_diagnoses = self.seed_diagnoses()
        print(f"   ✅ {n_diagnoses} diagnósticos")
    
        print("\n📋 Criando histórico médico...")
        n_history = self.seed_medical_history()
        print(f"   ✅ {n_history} registros")
    
        print("\n" + "=" * 50)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    seed = Seed()
    seed.run_seed()
