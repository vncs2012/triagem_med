from src.database.connection import DatabaseConnection
from src.database.models import Patient, MedicalHistory, Diagnosis
from sqlalchemy import or_

class ToolDatabase():
    def __init__(self, database: DatabaseConnection):
        self.database = database

    def obter_paciente(self, paciente_id: str) -> dict:
        """Busca os dados de um paciente pelo ID.
        
        Args:
            paciente_id: O ID do paciente (ex: P001, P002, P003, P004, P005)
            
        Returns:
            Dicionário com os dados do paciente
        """
        with self.database.get_session() as session:
            paciente = session.query(Patient).filter(Patient.id == paciente_id).first()
            if not paciente:
                return {"erro": f"Paciente {paciente_id} não encontrado"}
            return paciente.to_dict()
    
    def obter_historico_paciente(self, paciente_id: str) -> list:
        """Busca o histórico médico de um paciente pelo ID.
        
        Args:
            paciente_id: O ID do paciente (ex: P001, P002, P003, P004, P005)
            
        Returns:
            Lista com os registros do histórico médico
        """
        with self.database.get_session() as session:
            historico = session.query(MedicalHistory).filter(
                MedicalHistory.patient_id == paciente_id
            ).all()
            if not historico:
                return []
            return [h.to_dict() for h in historico]

    def listar_pacientes(self) -> list:
        """Lista todos os pacientes cadastrados no sistema.
        
        Returns:
            Lista com os dados de todos os pacientes
        """
        with self.database.get_session() as session:
            pacientes = session.query(Patient).all()
            return [p.to_dict() for p in pacientes]

    def obter_diagnosticos(self) -> list:
        """Lista todos os diagnosticos cadastrados no sistema.
        
        Returns:
            Lista com os dados de todos os diagnosticos
        """
        with self.database.get_session() as session:
            diagnosticos = session.query(Diagnosis).all()
            return [d.to_dict() for d in diagnosticos]
            

    def obter_diagnostico(self, identificador: str) -> dict:
        """Busca diagnóstico por ID do paciente ou ID do diagnóstico.
        
        Args:
            identificador: ID do paciente (ex: P001) ou ID do diagnóstico
            
        Returns:
            Dicionário ou lista com os dados do(s) diagnóstico(s)
        """
        with self.database.get_session() as session:
            diagnostico = session.query(Diagnosis).filter(Diagnosis.id == identificador).first()
            if diagnostico:
                return diagnostico.to_dict()
            
            diagnosticos = session.query(Diagnosis).filter(Diagnosis.patient_id == identificador).all()
            if diagnosticos:
                diagnosticos_ordenados = sorted(diagnosticos, key=lambda d: d.timestamp, reverse=True)
                return [d.to_dict() for d in diagnosticos_ordenados]
            
            return {"erro": f"Nenhum diagnóstico encontrado para '{identificador}'"}

    def _gerar_proximo_id(self, prefixo: str, modelo) -> str:
        """Gera o próximo ID sequencial para um modelo (ex: P001 -> P002)."""
        with self.database.get_session() as session:
            ultimo = session.query(modelo).order_by(modelo.id.desc()).first()
            
            if not ultimo:
                return f"{prefixo}001"
            
            try:
                numero_atual = int(ultimo.id[1:])
                proximo_numero = numero_atual + 1
                return f"{prefixo}{proximo_numero:03d}"
            except ValueError:
                return f"{prefixo}001"

    def cadastrar_paciente(
        self, 
        name: str, 
        birth_date: str = None, 
        cpf: str = None, 
        contact: str = None, 
        email: str = None, 
        address: str = None
    ) -> dict:
        """Cadastra um novo paciente no sistema.
        
        Args:
            name: Nome completo do paciente
            birth_date: Data de nascimento (YYYY-MM-DD) - opcional
            cpf: CPF do paciente (XXX.XXX.XXX-XX) - opcional
            contact: Telefone de contato - opcional
            email: E-mail do paciente - opcional
            address: Endereço do paciente - opcional
            
        Returns:
            Dicionário com os dados do paciente cadastrado e seu novo ID
        """
        with self.database.get_session() as session:
            if cpf:
                existente = session.query(Patient).filter(Patient.cpf == cpf).first()
                if existente:
                    return {"erro": f"CPF {cpf} já cadastrado para o paciente {existente.name} (ID: {existente.id})"}
            
            novo_id = self._gerar_proximo_id("P", Patient)
            
            novo_paciente = Patient(
                id=novo_id,
                name=name,
                birth_date=birth_date,
                cpf=cpf,
                contact=contact,
                email=email,
                address=address
            )
            
            try:
                session.add(novo_paciente)
                session.commit()
                return {
                    "mensagem": "Paciente cadastrado com sucesso",
                    "paciente": novo_paciente.to_dict()
                }
            except Exception as e:
                session.rollback()
                return {"erro": f"Erro ao cadastrar paciente: {str(e)}"}

    def cadastrar_diagnostico(
        self, 
        patient_id: str, 
        classification: str, 
        confidence: float, 
        priority: str, 
        image_path: str = None, 
        notes: str = None,
        created_by: str = "system"
    ) -> dict:
        """Cadastra um novo diagnóstico para um paciente.
        
        Args:
            patient_id: ID do paciente (ex: P001)
            classification: Classificação (NORMAL ou PNEUMONIA)
            confidence: Confiança da classificação (0.0 a 1.0) ou percentual em string
            priority: Prioridade (BAIXA, MÉDIA, ALTA, CRÍTICA)
            image_path: Caminho da imagem analisada - opcional
            notes: Observações adicionais - opcional
            created_by: Quem registrou (padrão: "system")
            
        Returns:
            Dicionário com os dados do diagnóstico cadastrado
        """
        if classification.upper() not in ["NORMAL", "PNEUMONIA"]:
            return {"erro": f"Classificação inválida: {classification}. Use NORMAL ou PNEUMONIA."}

        prioridades_validas = ["BAIXA", "MÉDIA", "ALTA", "CRÍTICA", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if priority.upper() not in prioridades_validas:
             return {"erro": f"Prioridade inválida: {priority}. Valores aceitos: {prioridades_validas}"}

        mapa_prioridade = {
            "BAIXA": "LOW", "MÉDIA": "MEDIUM", "ALTA": "HIGH", "CRÍTICA": "CRITICAL",
            "LOW": "LOW", "MEDIUM": "MEDIUM", "HIGH": "HIGH", "CRITICAL": "CRITICAL"
        }
        priority_en = mapa_prioridade.get(priority.upper(), priority.upper())

        conf_float = confidence
        if isinstance(confidence, str):
            try:
                conf_clean = confidence.replace("%", "")
                conf_float = float(conf_clean)
                if conf_float > 1.0:
                     conf_float = conf_float / 100.0
            except ValueError:
                pass

        with self.database.get_session() as session:
            paciente = session.query(Patient).filter(Patient.id == patient_id).first()
            if not paciente:
                return {"erro": f"Paciente {patient_id} não encontrado. Cadastre o paciente antes de registrar diagnóstico."}
            novo_id = self._gerar_proximo_id("D", Diagnosis)
            
            novo_diagnostico = Diagnosis(
                id=novo_id,
                patient_id=patient_id,
                image_path=image_path,
                classification=classification.upper(),
                confidence=float(conf_float),
                priority=priority_en,
                notes=notes,
                created_by=created_by
            )
            
            try:
                session.add(novo_diagnostico)
                session.commit()
                return {
                    "mensagem": "Diagnóstico registrado com sucesso",
                    "diagnostico": novo_diagnostico.to_dict()
                }
            except Exception as e:
                session.rollback()
                return {"erro": f"Erro ao registrar diagnóstico: {str(e)}"}

    def cadastrar_historico(
        self, 
        patient_id: str, 
        description: str, 
        condition_type: str = "observacao", 
        recorded_by: str = "system"
    ) -> dict:
        """Cadastra um novo registro no histórico médico do paciente.
        
        Args:
            patient_id: ID do paciente (ex: P001)
            description: Descrição do histórico (ex: "Alergia a Penicilina")
            condition_type: Tipo da condição (ex: "alergia", "doença_cronica", "cirurgia")
            recorded_by: Quem registrou (padrão: "system")
            
        Returns:
            Dicionário com o registro criado ou erro.
        """
        with self.database.get_session() as session:
            paciente = session.query(Patient).filter(Patient.id == patient_id).first()
            if not paciente:
                return {"erro": f"Paciente {patient_id} não encontrado."}
            
            novo_historico = MedicalHistory(
                patient_id=patient_id,
                description=description,
                condition_type=condition_type,
                recorded_by=recorded_by
            )
            
            try:
                session.add(novo_historico)
                session.commit()
                return {
                    "mensagem": "Histórico registrado com sucesso",
                    "historico": novo_historico.to_dict()
                }
            except Exception as e:
                session.rollback()
                return {"erro": f"Erro ao registrar histórico: {str(e)}"}
        