#!/usr/bin/env python3
"""Script de teste para validar o sistema SCIC."""

import sys
from pathlib import Path

# Adicionar scic ao path
sys.path.insert(0, str(Path(__file__).parent / "scic"))

from scic_core.dados import RepositorioDados
from scic_core.erros import indicadores_comunicacao
from scic_core.modelo import treinar_modelo

def test_carregar_dados():
    print("✓ Testando carregamento de dados...")
    repo = RepositorioDados(Path(__file__).parent / "scic" / "dados_aurora_siger.csv")
    df = repo.carregar()
    print(f"  → {len(df)} registros carregados")
    assert len(df) > 0, "Nenhum registro carregado"
    print("  ✓ OK")

def test_indicadores():
    print("✓ Testando indicadores de comunicação...")
    repo = RepositorioDados(Path(__file__).parent / "scic" / "dados_aurora_siger.csv")
    df = repo.carregar()
    ind = indicadores_comunicacao(df)
    print(f"  → {len(ind)} indicadores calculados")
    assert "erro_abs_medio_ms" in ind, "MAE não calculado"
    print(f"  → MAE: {ind['erro_abs_medio_ms']:.3f} ms")
    print("  ✓ OK")

def test_modelo():
    print("✓ Testando modelo de latência...")
    repo = RepositorioDados(Path(__file__).parent / "scic" / "dados_aurora_siger.csv")
    df = repo.carregar()
    resultado = treinar_modelo(df)
    print(f"  → R²: {resultado.r2:.3f}, MAE: {resultado.mae:.3f} ms")
    assert resultado.r2 > -1.0, "R² inválido"
    print("  ✓ OK")

if __name__ == "__main__":
    try:
        test_carregar_dados()
        test_indicadores()
        test_modelo()
        print("\n✅ Todos os testes passaram!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
