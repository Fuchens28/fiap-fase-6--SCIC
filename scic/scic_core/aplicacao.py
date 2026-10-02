"""Menu de terminal do Sistema de Comunicação Interplanetária da Colônia."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from scic_core.catalogo import MODULOS, PALAVRAS_CHAVE
from scic_core.dados import RepositorioDados
from scic_core.erros import analisar_erros, euler_latencia, indicadores_comunicacao, nota_ponto_flutuante
from scic_core.graficos import (
    garantir_pasta,
    grafico_erros,
    grafico_euler,
    grafico_latencia_por_modulo,
    grafico_modelo,
)
from scic_core.hardware import converter_codigo, potencia_transmissor, texto_dispositivos
from scic_core.heap_alertas import Alerta, MaxHeapAlertas, pontuar_alerta
from scic_core.modelo import treinar_modelo
from scic_core.trie_busca import Trie

RAIZ = Path(__file__).resolve().parent.parent
CSV_PADRAO = RAIZ / "dados_aurora_siger.csv"
PASTA_GRAFICOS = RAIZ / "graficos_ou_imagens"


def _pausar() -> None:
    input("\nPressione Enter para voltar ao menu...")


def _imprimir_tabela(df: pd.DataFrame, colunas: list[str], n: int = 12) -> None:
    visivel = df[colunas].head(n)
    print(visivel.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    if len(df) > n:
        print(f"... ({len(df)} registros no total)")


class AplicacaoSCIC:
    def __init__(self) -> None:
        self.repo = RepositorioDados(CSV_PADRAO)
        self.ultimo_modelo = None
        self.trie = Trie()
        self._montar_trie_base()

    def executar(self) -> None:
        while True:
            self._menu()
            escolha = input("Escolha uma opcao: ").strip()
            acoes = {
                "1": self.carregar_dados,
                "2": self.consultar_registros,
                "3": self.cadastrar_registro,
                "4": self.indicadores_e_erros,
                "5": self.executar_modelo,
                "6": self.priorizar_alertas,
                "7": self.busca_trie,
                "8": self.hardware_e_bases,
                "9": self.analise_final,
                "10": self.demonstracao_completa,
                "0": None,
            }
            if escolha == "0":
                print("Encerrando o SCIC. Aurora Siger fora.")
                return
            acao = acoes.get(escolha)
            if acao is None:
                print("Opcao invalida.")
                continue
            try:
                acao()
            except Exception as erro:  # pylint: disable=broad-except
                print(f"Nao foi possivel concluir a operacao: {erro}")
            _pausar()

    def _menu(self) -> None:
        print(
            """
============================================================
 SCIC  |  Sistema de Comunicacao Interplanetaria da Colonia
 Aurora Siger  ·  Fase 6  ·  FIAP
============================================================
 1  Carregar dados operacionais (CSV)
 2  Consultar registros
 3  Cadastrar um registro simulado
 4  Calcular indicadores e erros numericos
 5  Treinar modelo simples de latencia
 6  Priorizar alertas com heap
 7  Buscar por prefixo com trie
 8  Dispositivos, bases numericas e eletricidade
 9  Analise final dos resultados
10  Demonstracao completa (fluxo do video)
 0  Sair
============================================================
"""
        )

    def _montar_trie_base(self) -> None:
        for codigo, info in MODULOS.items():
            self.trie.inserir(codigo, f"{codigo} — {info['nome']}")
            self.trie.inserir(info["nome"], f"{codigo} — {info['nome']}")
            self.trie.inserir(format(info["codigo_sensor"], "X"), f"sensor {codigo}")
        for palavra in PALAVRAS_CHAVE:
            self.trie.inserir(palavra)

    def carregar_dados(self) -> None:
        df = self.repo.carregar()
        print(f"Base carregada: {len(df)} registros em {CSV_PADRAO.name}")
        print("Colunas:", ", ".join(df.columns))
        print("\nAmostra:")
        _imprimir_tabela(
            df,
            ["ciclo", "modulo_id", "latencia_observada_ms", "status", "prioridade"],
            n=10,
        )
        print("\nResumo por modulo:")
        print(self.repo.resumo_modulos().to_string(index=False, float_format=lambda v: f"{v:.2f}"))

    def consultar_registros(self) -> None:
        self.repo.exigir_carregado()
        modulo = input("Filtrar por modulo (CTL/PWR/... ou Enter para todos): ").strip()
        status = input("Filtrar por status (ativo/manutencao/alerta ou Enter): ").strip()
        df = self.repo.consultar(modulo or None, status or None)
        if df.empty:
            print("Nenhum registro encontrado com esse filtro.")
            return
        _imprimir_tabela(
            df,
            [
                "ciclo",
                "modulo_id",
                "nome_modulo",
                "latencia_observada_ms",
                "latencia_estimada_ms",
                "status",
                "mensagem_alerta",
            ],
            n=20,
        )

    def cadastrar_registro(self) -> None:
        df = self.repo.exigir_carregado()
        print("Modulos:", ", ".join(MODULOS))
        modulo = input("ID do modulo: ").strip().upper()
        if modulo not in MODULOS:
            print("Modulo desconhecido.")
            return
        info = MODULOS[modulo]
        latencia = float(input("Latencia observada (ms): ").strip())
        qualidade = float(input("Qualidade do sinal (0-100): ").strip())
        carga = float(input("Carga do enlace (0-100): ").strip())
        ciclo = int(df["ciclo"].max()) + 1
        tensao = info["tensao_nominal_v"]
        corrente = info["corrente_nominal_a"]
        potencia = tensao * corrente
        estimada = info["latencia_base_ms"] + 0.25 * carga
        status = "alerta" if latencia > estimada * 1.2 else "ativo"
        registro = {
            "ciclo": ciclo,
            "modulo_id": modulo,
            "nome_modulo": info["nome"],
            "tipo_modulo": info["tipo"],
            "latencia_observada_ms": latencia,
            "latencia_estimada_ms": round(estimada, 3),
            "tensao_v": tensao,
            "corrente_a": corrente,
            "potencia_w": round(potencia, 4),
            "qualidade_sinal": qualidade,
            "carga_enlace": carga,
            "status": status,
            "prioridade": info["prioridade"],
            "peso_prioridade": info["peso_prioridade"],
            "codigo_sensor_dec": info["codigo_sensor"],
            "mensagem_alerta": "Registro manual do operador" if status == "alerta" else "Operacao nominal",
        }
        self.repo.cadastrar_registro(registro)
        print("Registro gravado em dados_aurora_siger.csv")

    def indicadores_e_erros(self) -> dict:
        df = self.repo.exigir_carregado()
        ind = indicadores_comunicacao(df)
        print("--- Indicadores de comunicacao ---")
        print(f"Registros              : {ind['n_registros']}")
        print(f"Latencia media         : {ind['latencia_media_ms']:.3f} ms")
        print(f"Latencia mediana       : {ind['latencia_mediana_ms']:.3f} ms")
        print(f"Potencia media         : {ind['potencia_media_w']:.3f} W")
        print(f"Qualidade media        : {ind['qualidade_media']:.2f}")
        print(f"Erro absoluto medio    : {ind['erro_abs_medio_ms']:.3f} ms")
        print(f"Erro relativo medio    : {ind['erro_rel_medio']*100:.2f} %")
        print(f"Erros preocupantes     : {ind['registros_preocupantes']}")
        print(f"Registros em alerta    : {ind['registros_em_alerta']}")
        print(f"Max |P_csv - V*I|      : {ind['max_dif_potencia_w']:.3e} W")
        print()
        print("Limites adotados: relativo <= 12% aceitavel; 12-25% atencao; >25% preocupante.")
        print(nota_ponto_flutuante())
        print("\nMaiores erros relativos:")
        piores = ind["erros"].sort_values("erro_relativo", ascending=False).head(8)
        _imprimir_tabela(
            piores,
            ["ciclo", "modulo_id", "latencia_observada_ms", "latencia_estimada_ms", "erro_absoluto_ms", "erro_relativo", "classificacao_erro"],
        )
        pasta = garantir_pasta(PASTA_GRAFICOS)
        grafico_latencia_por_modulo(df, pasta)
        grafico_erros(ind["erros"], pasta)
        print(f"\nGraficos salvos em {pasta}")
        return ind

    def executar_modelo(self):
        df = self.repo.exigir_carregado()
        resultado = treinar_modelo(df)
        self.ultimo_modelo = resultado
        print("--- Modelo linear de latencia ---")
        print("Alvo: latencia_observada_ms")
        print("Atributos:", ", ".join(["carga_enlace", "qualidade_sinal", "potencia_w", "peso_prioridade", "tensao_v"]))
        print(f"Treino/teste : {resultado.n_treino} / {resultado.n_teste} (70/30)")
        print(f"MAE          : {resultado.mae:.4f} ms")
        print(f"MSE          : {resultado.mse:.4f}")
        print(f"RMSE         : {resultado.rmse:.4f} ms")
        print(f"R2           : {resultado.r2:.4f}")
        print(f"AIC / BIC    : {resultado.aic:.2f} / {resultado.bic:.2f}")
        if resultado.melhor_alpha is not None:
            print(f"Ridge escolhido pelo Grid Search com alpha={resultado.melhor_alpha}")
        else:
            print("Regressao linear simples ficou melhor que o Ridge no conjunto de teste.")
        print("Coeficientes:")
        for nome, valor in resultado.coeficientes.items():
            print(f"  {nome:18s} {valor:+.4f}")
        print(f"  intercepto         {resultado.intercepto:+.4f}")
        print()
        print(resultado.interpretacao)
        pasta = garantir_pasta(PASTA_GRAFICOS)
        caminho = grafico_modelo(resultado, pasta)
        print(f"Grafico do modelo: {caminho.name}")
        return resultado

    def priorizar_alertas(self) -> list:
        df = self.repo.exigir_carregado()
        erros = analisar_erros(df)
        candidatos = erros[erros["status"].isin(["alerta", "manutencao"])]
        if candidatos.empty:
            candidatos = erros.sort_values("erro_relativo", ascending=False).head(8)
            print("Nao ha status alerta/manutencao; usando os maiores erros relativos.")
        heap = MaxHeapAlertas()
        for _, linha in candidatos.iterrows():
            essencial = bool(MODULOS.get(linha["modulo_id"], {}).get("essencial", False))
            pontuacao, motivo = pontuar_alerta(linha.to_dict(), essencial)
            heap.inserir(
                Alerta(
                    pontuacao=pontuacao,
                    modulo_id=str(linha["modulo_id"]),
                    nome_modulo=str(linha["nome_modulo"]),
                    ciclo=int(linha["ciclo"]),
                    latencia_observada_ms=float(linha["latencia_observada_ms"]),
                    erro_relativo=float(linha["erro_relativo"]),
                    status=str(linha["status"]),
                    mensagem=str(linha["mensagem_alerta"]),
                    motivo=motivo,
                )
            )
        print("--- Heap de alertas (max-heap) ---")
        print("A raiz e o alerta mais urgente. Insercao usa heapify-up; extração usa heapify-down.")
        print("Vantagem sobre lista: obter o mais urgente e O(1) na raiz e O(log n) para inserir/remover,")
        print("enquanto uma lista exigiria varrer todos os elementos a cada consulta.\n")
        print(f"Alertas na heap: {len(heap)}")
        raiz = heap.ver_raiz()
        if raiz:
            print(f"Mais urgente agora: {raiz.modulo_id} ciclo {raiz.ciclo} (pontuacao {raiz.pontuacao:.1f})")
        print("\nOrdem de atendimento:")
        ordenados = heap.listar_ordenados()
        for i, alerta in enumerate(ordenados[:10], start=1):
            print(
                f"{i:02d}. [{alerta.pontuacao:6.1f}] {alerta.modulo_id} "
                f"ciclo {alerta.ciclo} | {alerta.status} | {alerta.latencia_observada_ms:.1f} ms | {alerta.mensagem}"
            )
        return ordenados

    def busca_trie(self) -> None:
        print("A trie organiza caracteres por prefixo. Digitar 'com' encontra Comunicacao, Comando, Controle.")
        prefixo = input("Prefixo (ex.: com, CTL, 6AE, lat): ").strip()
        if not prefixo:
            print("Prefixo vazio.")
            return
        achados = self.trie.autocomplete(prefixo)
        if not achados:
            print("Nenhum registro com esse prefixo.")
            return
        print(f"Resultados para '{prefixo}':")
        for item in achados:
            print(f"  - {item}")

    def hardware_e_bases(self) -> None:
        print(texto_dispositivos())
        print("\n--- Conversao de codigo de sensor ---")
        modulo = input("Modulo para converter (Enter = COM): ").strip().upper() or "COM"
        if modulo not in MODULOS:
            print("Modulo desconhecido.")
            return
        info = MODULOS[modulo]
        conv = converter_codigo(info["codigo_sensor"])
        print(f"{modulo} | sensor decimal {conv['decimal']}")
        print(f"  binario      : {conv['binario']}")
        print(f"  hexadecimal  : {conv['hex_formatado']}")
        pot = potencia_transmissor(info["tensao_nominal_v"], info["corrente_nominal_a"])
        print("\n--- Lei de Ohm / potencia do transmissor ---")
        print(f"V = {pot['tensao_v']} V, I = {pot['corrente_a']} A")
        print(f"P = V * I = {pot['potencia_w']:.4f} W")
        print(f"R = V / I = {pot['resistencia_ohm']:.4f} ohm")
        df = self.repo.df
        if df is not None:
            recorte = df[df["modulo_id"] == modulo].tail(1)
            if not recorte.empty:
                linha = recorte.iloc[0]
                print(
                    f"No ultimo ciclo do CSV, potencia registrada = {linha['potencia_w']:.4f} W "
                    f"(bate com V*I a menos de erro de ponto flutuante)."
                )

    def analise_final(self) -> None:
        df = self.repo.exigir_carregado()
        ind = indicadores_comunicacao(df)
        print("=== Analise final do SCIC ===")
        print(
            "A Aurora Siger precisa interpretar a comunicacao, nao so armazenar logs. "
            "O SCIC organiza o CSV, mede o desvio entre latencia prevista e observada, "
            "treina um modelo linear, atende alertas pela heap e localiza registros pela trie."
        )
        print(
            f"\nSinal operacional: latencia media {ind['latencia_media_ms']:.2f} ms, "
            f"{ind['registros_em_alerta']} alertas, "
            f"{ind['registros_preocupantes']} erros relativos preocupantes."
        )
        if self.ultimo_modelo:
            print(
                f"Modelo: MAE {self.ultimo_modelo.mae:.2f} ms, "
                f"RMSE {self.ultimo_modelo.rmse:.2f} ms, R2 {self.ultimo_modelo.r2:.3f}."
            )
        else:
            print("Modelo ainda nao treinado nesta sessao (opcao 5).")
        print("\nGestao inteligente (a partir destes numeros, nao de um texto generico):")
        print("- sensores e medidores: cada linha do CSV simula uma leitura de enlace, tensao e corrente;")
        print("- monitoramento continuo: erro relativo > 25% vira atencao operacional;")
        print("- automacao: a heap escolhe o proximo alerta sem varrer a lista inteira;")
        print("- redundancia: COM e CTL concentram comunicacao; um pico de latencia la e mais grave;")
        print("- manutencao preditiva: o modelo estima latencia antes do enlace falhar de fato;")
        print("- microrrede: potencia do transmissor (P=V*I) liga o enlace a energia local da colônia.")
        print("\nDecisao automatizada nao substitui a tripulacao: o menu exige confirmacao humana.")

        print("\nSimulacao de Euler (enlace COM se recuperando):")
        valores = euler_latencia(latencia_inicial=80.0, latencia_equilibrio=35.0)
        print("  " + " -> ".join(f"{v:.2f}" for v in valores))
        pasta = garantir_pasta(PASTA_GRAFICOS)
        grafico_euler(valores, pasta)
        print(f"Grafico de Euler salvo em {pasta / 'euler_latencia.png'}")

    def demonstracao_completa(self) -> None:
        print(">>> 1/7 Carregando dados")
        self.carregar_dados()
        print("\n>>> 2/7 Indicadores e erros")
        self.indicadores_e_erros()
        print("\n>>> 3/7 Modelo")
        self.executar_modelo()
        print("\n>>> 4/7 Heap")
        self.priorizar_alertas()
        print("\n>>> 5/7 Trie (prefixo 'com')")
        achados = self.trie.autocomplete("com")
        for item in achados:
            print(f"  - {item}")
        print("\n>>> 6/7 Hardware do modulo COM")
        info = MODULOS["COM"]
        conv = converter_codigo(info["codigo_sensor"])
        pot = potencia_transmissor(info["tensao_nominal_v"], info["corrente_nominal_a"])
        print(f"codigo {conv['decimal']} = {conv['hex_formatado']} = {conv['binario']}b")
        print(f"P = {pot['potencia_w']:.4f} W | R = {pot['resistencia_ohm']:.4f} ohm")
        print("\n>>> 7/7 Analise final")
        self.analise_final()
        print("\nDemonstracao concluida. Graficos em graficos_ou_imagens/.")
