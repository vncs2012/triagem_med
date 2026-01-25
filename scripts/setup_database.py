import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
from src.database.seed import Seed
from src.database.connection import DatabaseConnection

def main():
    parser = argparse.ArgumentParser(description='Configura o banco de dados do sistema')
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reseta o banco de dados (APAGA TODOS OS DADOS)'
    )
    parser.add_argument(
        '--seed',
        action='store_true',
        help='Popula o banco com dados de exemplo'
    )
    parser.add_argument(
        '--init-only',
        action='store_true',
        help='Apenas inicializa as tabelas (padrão)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 50)
    print("   CONFIGURAÇÃO DO BANCO DE DADOS")
    print("=" * 50 + "\n")
    
    database = DatabaseConnection()
    
    if args.reset:
        confirm = input("⚠️  ATENÇÃO: Isso irá APAGAR todos os dados. Confirmar? (s/N): ")
        if confirm.lower() == 's':
            print("\n🗑️  Resetando banco de dados...")
            database.reset_database()
            print("✅ Banco de dados resetado!")
        else:
            print("❌ Operação cancelada.")
            return
    else:
        print("📦 Inicializando banco de dados...")
        database.init_database()
        print("✅ Banco de dados inicializado!")
    
    if args.seed:
        print("\n" + "-" * 50)
        seed = Seed()
        seed.run_seed()
    
    print("\n" + "=" * 50)
    print("   CONFIGURAÇÃO CONCLUÍDA")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
