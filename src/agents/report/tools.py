import datetime
import json
from pathlib import Path
from typing import Optional, List, Union
from src.config import Settings

class ToolReport():
    def __init__(self):
        self.settings = Settings()
        self.reports_dir = self.settings.reports_dir

    def generate_pdf(self, patient_id: str, diagnosis_data: dict, output_path: str = None) -> dict:
        """Gera um relatório em PDF com o diagnóstico do paciente.
        
        Args:
            patient_id: ID do paciente
            diagnosis_data: Dados do diagnóstico (dict com classification, confidence, priority, etc)
            output_path: Caminho de saída do PDF (opcional)
            
        Returns:
            Dicionário confirmando o status da geração
        """
        try:
            if output_path is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"relatorio_{patient_id}_{timestamp}.txt"
                output_path = self.reports_dir / filename
            else:
                output_path = Path(output_path)
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Gera o relatório em texto simples (simulação de PDF)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("SISTEMA DE TRIAGEM MÉDICA - RELATÓRIO DE DIAGNÓSTICO\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Código do Paciente: {patient_id}\n\n")
                
                f.write("-" * 80 + "\n")
                f.write("RESULTADO DO DIAGNÓSTICO\n")
                f.write("-" * 80 + "\n\n")
                
                f.write(f"Classificação: {diagnosis_data.get('classification', 'N/A')}\n")
                f.write(f"Confiança: {diagnosis_data.get('confidence', 0):.2%}\n")
                f.write(f"Prioridade: {diagnosis_data.get('priority', 'N/A')}\n")
                
                if diagnosis_data.get('notes'):
                    f.write(f"\nObservações: {diagnosis_data['notes']}\n")
                
                f.write("\n" + "-" * 80 + "\n")
                f.write("DISCLAIMER\n")
                f.write("-" * 80 + "\n\n")
                f.write("Este é um sistema de triagem automatizada.\n")
                
                f.write("=" * 80 + "\n")
            
            return {
                "status": "sucesso", 
                "mensagem": f"Relatório gerado com sucesso",
                "arquivo": str(output_path)
            }
        except Exception as e:
            print(f"Erro ao gerar relatório: {str(e)}")
            return {"status": "erro", "mensagem": f"Falha ao gerar relatório: {str(e)}"}

    def generate_stats(self, diagnosticos: Union[List[dict], str]) -> dict:
        """Gera estatísticas a partir de uma lista de diagnósticos.
        
        Args:
            diagnosticos: Lista de dicionários ou string JSON com dados de diagnósticos
            
        Returns:
            Dicionário com estatísticas calculadas
        """
        if isinstance(diagnosticos, str):
            try:
                diagnosticos = json.loads(diagnosticos)
            except Exception as e:
                return {"status": "erro", "mensagem": f"Dados de diagnósticos inválidos: {str(e)}"}
        try:
            total = len(diagnosticos)
            
            if total == 0:
                return {
                    "status": "sucesso",
                    "mensagem": "Nenhum diagnóstico fornecido para análise",
                    "total": 0
                }
            
            pneumonia_count = sum(1 for d in diagnosticos if d.get('classification') == "PNEUMONIA")
            normal_count = total - pneumonia_count
            
            priority_stats = {}
            for d in diagnosticos:
                priority = d.get('priority', 'DESCONHECIDO')
                priority_stats[priority] = priority_stats.get(priority, 0) + 1
            
            confidences = [d.get('confidence', 0) for d in diagnosticos]
            avg_confidence = sum(confidences) / total if total > 0 else 0
            
            stats = {
                "status": "sucesso",
                "total_diagnosticos": total,
                "pneumonia": pneumonia_count,
                "normal": normal_count,
                "taxa_pneumonia": f"{(pneumonia_count/total*100):.1f}%",
                "confianca_media": f"{avg_confidence:.2%}",
                "por_prioridade": priority_stats
            }
            
            return stats
                
        except Exception as e:
            return {"status": "erro", "mensagem": f"Falha ao gerar estatísticas: {str(e)}"}