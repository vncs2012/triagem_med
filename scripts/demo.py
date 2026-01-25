#!/usr/bin/env python3
"""
Script de Demonstração do Sistema de Triagem

Este script demonstra as principais funcionalidades do sistema,
incluindo análise de imagem, consulta de pacientes e geração de relatórios.
"""

import asyncio
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.database.connection import init_database
from src.database.seed import run_seed
from src.agents import TriageAgent, DatabaseAgent, ReportAgent, NotificationAgent
from src.tools import (
    classify_xray,
    validate_image,
    calculate_priority,
    get_patient,
    list_patients,
    save_diagnosis,
    generate_stats,
    send_alert,
)


def print_section(title: str):
    """Imprime cabeçalho de seção."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


async def demo_ml_classification():
    """Demonstra classificação de imagem com ML."""
    print_section("🔬 DEMONSTRAÇÃO: Classificação de Imagem")
    
    # Criar uma imagem de teste (simulada)
    test_image = settings.data_dir / "sample_images" / "test_xray.png"
    
    # Criar imagem de teste simples se não existir
    if not test_image.exists():
        test_image.parent.mkdir(parents=True, exist_ok=True)
        from PIL import Image
        img = Image.new('RGB', (224, 224), color='gray')
        img.save(test_image)
        print(f"📷 Imagem de teste criada: {test_image}")
    
    print(f"\n📋 Validando imagem: {test_image}")
    validation = validate_image(str(test_image))
    print(f"   Válida: {validation['is_valid']}")
    print(f"   Mensagem: {validation['message']}")
    
    if validation["is_valid"]:
        print(f"\n🤖 Classificando imagem...")
        result = classify_xray(str(test_image))
        
        print(f"   Classificação: {result['classification']}")
        print(f"   Confiança: {result['confidence']:.1%}")
        
        if result.get("simulated"):
            print(f"   ⚠️  {result.get('warning', 'Resultado simulado')}")
        
        # Calcular prioridade
        print(f"\n📊 Calculando prioridade...")
        priority = calculate_priority(result['classification'], result['confidence'])
        print(f"   Prioridade: {priority['priority']} (nível {priority['level']})")
        print(f"   Tempo de resposta: {priority['response_time']}")
        print(f"   Recomendação: {priority['recommendation']}")


async def demo_database_operations():
    """Demonstra operações de banco de dados."""
    print_section("🗄️ DEMONSTRAÇÃO: Banco de Dados")
    
    # Listar pacientes
    print("\n📋 Listando pacientes...")
    result = list_patients({"limit": 5})
    
    if result["success"]:
        print(f"   Total encontrado: {result['total']}")
        for p in result["patients"][:3]:
            print(f"   - {p['id']}: {p['name']}")
    
    # Buscar paciente específico
    print("\n🔍 Buscando paciente P001...")
    patient_result = get_patient("P001")
    
    if patient_result["success"]:
        p = patient_result["patient"]
        print(f"   Nome: {p['name']}")
        print(f"   Contato: {p.get('contact', 'N/A')}")
        print(f"   Email: {p.get('email', 'N/A')}")
    
    # Salvar diagnóstico
    print("\n💾 Salvando novo diagnóstico...")
    save_result = save_diagnosis(
        patient_id="P001",
        image_path="/data/sample_images/test_xray.png",
        classification="NORMAL",
        confidence=0.85,
        priority="LOW",
        notes="Diagnóstico de demonstração"
    )
    
    if save_result["success"]:
        print(f"   ✅ Diagnóstico salvo: {save_result['diagnosis_id']}")


async def demo_statistics():
    """Demonstra geração de estatísticas."""
    print_section("📊 DEMONSTRAÇÃO: Estatísticas")
    
    stats = generate_stats("all")
    
    if stats["success"]:
        print(f"\n📈 Estatísticas do Sistema:")
        print(f"   Total de diagnósticos: {stats.get('total_diagnoses', 0)}")
        print(f"   Casos de pneumonia: {stats.get('pneumonia_cases', 0)}")
        print(f"   Casos normais: {stats.get('normal_cases', 0)}")
        print(f"   Taxa de pneumonia: {stats.get('pneumonia_rate', 0):.1%}")
        print(f"   Confiança média: {stats.get('average_confidence', 0):.1%}")
        
        priority_dist = stats.get("priority_distribution", {})
        print(f"\n   Distribuição por prioridade:")
        for level, count in priority_dist.items():
            print(f"     - {level}: {count}")


async def demo_notifications():
    """Demonstra sistema de notificações."""
    print_section("📧 DEMONSTRAÇÃO: Notificações")
    
    print("\n🚨 Enviando alerta de teste...")
    alert_result = send_alert(
        level="HIGH",
        message="Alerta de demonstração - Caso de alta prioridade",
        patient_id="P002"
    )
    
    if alert_result["success"]:
        print(f"   ✅ Alerta enviado: {alert_result['alert_id']}")
        print(f"   Nível: {alert_result['level']}")
        print(f"   Canais: {', '.join(alert_result['channels'])}")


async def demo_agents():
    """Demonstra os agentes do sistema."""
    print_section("🤖 DEMONSTRAÇÃO: Agentes")
    
    # Triage Agent
    print("\n🏥 Agente de Triagem:")
    triage = TriageAgent()
    info = triage.get_model_info()
    print(f"   Modelo disponível: {info.get('available', False)}")
    print(f"   Arquitetura: {info.get('architecture', 'N/A')}")
    print(f"   Classes: {info.get('classes', [])}")
    
    # Database Agent
    print("\n🗄️ Agente de Banco de Dados:")
    db_agent = DatabaseAgent()
    db_stats = await asyncio.to_thread(db_agent.get_database_stats)
    print(f"   Pacientes: {db_stats.get('total_patients', 0)}")
    print(f"   Diagnósticos: {db_stats.get('total_diagnoses', 0)}")


async def run_demo():
    """Executa todas as demonstrações."""
    print("\n")
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "🏥 DEMONSTRAÇÃO DO SISTEMA 🏥" + " " * 14 + "║")
    print("║" + " " * 10 + "Sistema de Triagem Médica - Pneumonia" + " " * 11 + "║")
    print("╚" + "═" * 60 + "╝")
    
    # Inicializar
    print("\n📦 Inicializando sistema...")
    init_database()
    run_seed()
    
    # Executar demonstrações
    await demo_ml_classification()
    await demo_database_operations()
    await demo_statistics()
    await demo_notifications()
    await demo_agents()
    
    print("\n")
    print("═" * 60)
    print("  ✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("═" * 60)
    print("\n💡 Próximos passos:")
    print("   1. Execute 'python -m src.main' para modo interativo")
    print("   2. Treine seu modelo ML com o dataset do Kaggle")
    print("   3. Configure as variáveis de ambiente no arquivo .env")
    print("\n")


def main():
    """Entry point do script de demonstração."""
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
