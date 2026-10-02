"""Max-heap didático para priorizar alertas da colônia.

Implementa heapify-up (inserção) e heapify-down (remoção da raiz),
como estudado no capítulo de estruturas avançadas. A raiz guarda o
alerta de maior pontuação — o mais urgente.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(order=True)
class Alerta:
    pontuacao: float
    modulo_id: str = field(compare=False)
    nome_modulo: str = field(compare=False)
    ciclo: int = field(compare=False)
    latencia_observada_ms: float = field(compare=False)
    erro_relativo: float = field(compare=False)
    status: str = field(compare=False)
    mensagem: str = field(compare=False)
    motivo: str = field(compare=False)


class MaxHeapAlertas:
    """Heap máximo em lista, com índices de árvore quase completa."""

    def __init__(self) -> None:
        self._dados: list[Alerta] = []

    def __len__(self) -> int:
        return len(self._dados)

    def inserir(self, alerta: Alerta) -> None:
        self._dados.append(alerta)
        self._heapify_up(len(self._dados) - 1)

    def extrair_mais_urgente(self) -> Alerta | None:
        if not self._dados:
            return None
        raiz = self._dados[0]
        ultimo = self._dados.pop()
        if self._dados:
            self._dados[0] = ultimo
            self._heapify_down(0)
        return raiz

    def ver_raiz(self) -> Alerta | None:
        return self._dados[0] if self._dados else None

    def listar_ordenados(self) -> list[Alerta]:
        copia = MaxHeapAlertas()
        copia._dados = list(self._dados)
        ordenados = []
        while copia:
            item = copia.extrair_mais_urgente()
            if item is not None:
                ordenados.append(item)
        return ordenados

    def _pai(self, i: int) -> int:
        return (i - 1) // 2

    def _esquerdo(self, i: int) -> int:
        return 2 * i + 1

    def _direito(self, i: int) -> int:
        return 2 * i + 2

    def _heapify_up(self, i: int) -> None:
        while i > 0:
            pai = self._pai(i)
            if self._dados[i].pontuacao <= self._dados[pai].pontuacao:
                break
            self._dados[i], self._dados[pai] = self._dados[pai], self._dados[i]
            i = pai

    def _heapify_down(self, i: int) -> None:
        n = len(self._dados)
        while True:
            maior = i
            e, d = self._esquerdo(i), self._direito(i)
            if e < n and self._dados[e].pontuacao > self._dados[maior].pontuacao:
                maior = e
            if d < n and self._dados[d].pontuacao > self._dados[maior].pontuacao:
                maior = d
            if maior == i:
                break
            self._dados[i], self._dados[maior] = self._dados[maior], self._dados[i]
            i = maior


def pontuar_alerta(linha: dict, essencial: bool) -> tuple[float, str]:
    """Critério composto, explícito para o relatório e o vídeo."""
    peso = float(linha["peso_prioridade"])
    erro_rel = float(linha.get("erro_relativo", 0.0) or 0.0)
    latencia = float(linha["latencia_observada_ms"])
    bonus_status = 25.0 if linha["status"] == "alerta" else 8.0 if linha["status"] == "manutencao" else 0.0
    bonus_essencial = 20.0 if essencial else 0.0
    bonus_latencia = min(latencia / 4.0, 30.0)
    bonus_erro = min(erro_rel * 80.0, 40.0)
    recencia = float(linha["ciclo"]) * 0.4
    pontuacao = (
        peso * 12.0
        + bonus_status
        + bonus_essencial
        + bonus_latencia
        + bonus_erro
        + recencia
    )
    motivo = (
        f"prioridade={linha['prioridade']} ({peso}*12), "
        f"status={linha['status']} (+{bonus_status:.0f}), "
        f"essencial={essencial} (+{bonus_essencial:.0f}), "
        f"latencia={latencia:.1f}ms, erro_rel={erro_rel:.3f}"
    )
    return pontuacao, motivo
