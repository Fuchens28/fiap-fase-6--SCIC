"""Trie para busca por prefixo de módulos, códigos e palavras-chave."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NoTrie:
    filhos: dict[str, "NoTrie"] = field(default_factory=dict)
    fim: bool = False
    payload: list[str] = field(default_factory=list)


class Trie:
    """Cada nível corresponde a um caractere; um caminho é um prefixo."""

    def __init__(self) -> None:
        self.raiz = NoTrie()

    def inserir(self, palavra: str, etiqueta: str | None = None) -> None:
        no = self.raiz
        chave = palavra.strip()
        for char in chave.lower():
            if char not in no.filhos:
                no.filhos[char] = NoTrie()
            no = no.filhos[char]
        no.fim = True
        texto = etiqueta or chave
        if texto not in no.payload:
            no.payload.append(texto)

    def buscar_exata(self, palavra: str) -> bool:
        no = self._caminhar(palavra)
        return bool(no and no.fim)

    def autocomplete(self, prefixo: str, limite: int = 12) -> list[str]:
        no = self._caminhar(prefixo)
        if no is None:
            return []
        encontrados: list[str] = []
        self._coletar(no, encontrados, limite)
        return encontrados

    def _caminhar(self, prefixo: str) -> NoTrie | None:
        no = self.raiz
        for char in prefixo.strip().lower():
            if char not in no.filhos:
                return None
            no = no.filhos[char]
        return no

    def _coletar(self, no: NoTrie, encontrados: list[str], limite: int) -> None:
        if len(encontrados) >= limite:
            return
        if no.fim:
            encontrados.extend(no.payload)
        for filho in no.filhos.values():
            self._coletar(filho, encontrados, limite)
