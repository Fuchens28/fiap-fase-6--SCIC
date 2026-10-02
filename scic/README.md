# SCIC — Sistema de Comunicação Interplanetária da Colônia

**Atividade Integradora · Fase 6 · Ciência da Computação · FIAP · 2026**

## Equipe

- Matheus Fuchelberguer · RM571321
- Carlos Eugenio Andrade · RM570285
- Rodrigo Gomes Dias · RM569142

## Objetivo

O SCIC é o protótipo desta fase da Aurora Siger. Ele organiza dados simulados de comunicação da colônia, calcula erros entre latência prevista e observada, treina um modelo linear simples, prioriza alertas com heap, busca registros por prefixo com trie e relaciona o resultado a dispositivos, bases numéricas e potência do transmissor.

O sistema continua o [NCAS da Fase 5](https://github.com/Fuchens28/fiap-fase-5-aurora-siger): os mesmos dez módulos (CTL, PWR, LSS, HAB, MED, COM, AGR, LOG, MIN, RES) agora ganham uma camada de avaliação de comunicação.

## Arquivos da entrega

| Arquivo | Função |
|---|---|
| `codigo_fonte.py` | Entrada do sistema (menu no terminal) |
| `dados_aurora_siger.csv` | Base simulada obrigatória |
| `relatorio_tecnico.md` | Relatório técnico |
| `README.md` | Este arquivo |
| `link_video.txt` | Link do vídeo (YouTube não listado) |
| `requirements.txt` | Dependências da fase |
| `scic_core/` | Código organizado por responsabilidade |
| `graficos_ou_imagens/` | Gráficos gerados na execução |

## Dependências

Bibliotecas trabalhadas na fase: NumPy, Pandas, Matplotlib e scikit-learn.

```text
pip install -r requirements.txt
```

Não há APIs externas, sensores físicos, dashboard web nem redes neurais.

## Como executar

Na pasta `scic`:

```text
python codigo_fonte.py
```

Menu:

1. Carregar dados  
2. Consultar registros  
3. Cadastrar um registro  
4. Indicadores e erros  
5. Modelo de latência  
6. Heap de alertas  
7. Trie (prefixo)  
8. Dispositivos, bases e eletricidade  
9. Análise final  
10. Demonstração completa (útil para o vídeo)  
0. Sair  

Fluxo automático (sem menu), usado para gerar os gráficos:

```text
python codigo_fonte.py --demo
```

## Recriar a base (opcional)

```text
python -m scic_core.gerar_base
```

A semente é fixa (`26`), então o CSV volta ao mesmo conteúdo.

## Observação sobre o vídeo

Grave no máximo 5 minutos, publique como **Não listado** no YouTube e cole o URL em `link_video.txt` antes de compactar o `.zip`.
