import smtplib
import json
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from src.config import Settings

class ToolNotification():
    def __init__(self):
        self.settings = Settings()
        self.alerts_file = self.settings.data_dir / "alerts_queue.json"
        
        if not self.alerts_file.exists():
            with open(self.alerts_file, 'w') as f:
                json.dump([], f)

    def enviar_email(self, email: str, paciente: str, diagnostico: str, recomendacao: str) -> dict:
        """Envia um email real para o paciente com o resultado do seu exame.
        
        Args:
            email: O endereço de email do paciente
            paciente: Nome completo do paciente
            diagnostico: O resultado do diagnóstico médico
            recomendacao: As recomendações médicas a serem seguidas
            
        Returns:
            Dicionário confirmando o status do envio
        """
        # Se não houver configurações de SMTP, simula o sucesso para não travar o fluxo
        if not self.settings.smtp_user or not self.settings.smtp_password:
            print(f"[SIMULADO] Email para {email}: Diagnóstico {diagnostico}")
            return {"status": "sucesso", "mensagem": f"Email simualdo enviado para {email} (Configure SMTP no .env para envio real)"}

        try:
            msg = MIMEMultipart()
            msg['From'] = self.settings.smtp_user
            msg['To'] = email
            msg['Subject'] = f"Resultado de Exame - {paciente}"

            corpo = f"""
            Olá {paciente},

            Seu resultado de triagem foi processado:
            Resultado: {diagnostico}
            Recomendação: {recomendacao}

            Atenciosamente,
            Equipe do Sistema de Triagem Médica
            """
            msg.attach(MIMEText(corpo, 'plain'))

            with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as server:
                server.starttls()
                server.login(self.settings.smtp_user, self.settings.smtp_password)
                server.send_message(msg)

            return {"status": "sucesso", "mensagem": f"Email enviado com sucesso para {email}"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Falha ao enviar email: {str(e)}"}

    def enviar_alerta(self, paciente: str, diagnostico: str, recomendacao: str) -> dict:
        """Envia um alerta para o sistema (fila de comunicação interna).
        
        Args:
            paciente: Nome do paciente
            diagnostico: O diagnóstico detectado
            recomendacao: A ação recomendada para a equipe médica
            
        Returns:
            Dicionário confirmando o registro do alerta
        """
        try:
            alerta = {
                "timestamp": datetime.datetime.now().isoformat(),
                "paciente": paciente,
                "diagnostico": diagnostico,
                "recomendacao": recomendacao,
                "lido": False
            }

            with open(self.alerts_file, 'r') as f:
                fila = json.load(f)

            fila.append(alerta)

            with open(self.alerts_file, 'w') as f:
                json.dump(fila, f, indent=4)

            return {"status": "sucesso", "mensagem": f"Alerta registrado no sistema para o paciente {paciente}"}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Falha ao registrar alerta: {str(e)}"}