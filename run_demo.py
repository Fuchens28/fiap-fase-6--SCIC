#!/usr/bin/env python3
"""Executar demonstração completa do SCIC e gerar gráficos."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scic"))

from scic_core.aplicacao import AplicacaoSCIC

def main():
    print("🚀 Iniciando demonstração completa do SCIC...\n")
    app = AplicacaoSCIC()
    
    try:
        app.carregar_dados()
        print("✓ Dados carregados com sucesso\n")
        
        app.demonstracao_completa()
        print("\n✅ Demonstração concluída!")
        print("   Gráficos gerados em: graficos_ou_imagens/")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
