# 🚀 SCIC — Sistema de Comunicação Interplanetária da Colônia

![Python](https://img.shields.io/badge/PYTHON-3.10%2B-3776AB?labelColor=0a0f1e&logo=python&logoColor=c5d8f0)
![Status](https://img.shields.io/badge/STATUS-EM%20OPERACAO-52be80?labelColor=0a0f1e&logo=startrek&logoColor=c5d8f0)
![Fase](https://img.shields.io/badge/FASE-6-c5d8f0?labelColor=0a0f1e&logoColor=c5d8f0)

*Atividade Integradora · Fase 6 · Ciência da Computação · FIAP · 2026*

## 🧑‍🚀 Equipe

- [Matheus Fuchelberguer | RM571321](https://www.linkedin.com/in/seu-perfil-matheus)
- [Carlos Eugenio Andrade | RM570285](https://www.linkedin.com/in/seu-perfil-carlos)
- [Rodrigo Gomes Dias | RM569142](https://www.linkedin.com/in/seu-perfil-rodrigo)

> Ajuste os links do LinkedIn acima com os perfis reais da equipe antes de publicar o projeto.

## 🌌 O que é o SCIC

O SCIC é um protótipo de monitoramento e análise de comunicação da colônia Aurora Siger. Ele simula o comportamento dos módulos da missão e avalia a latência, os erros operacionais, a prioridade dos alertas e a eficiência da comunicação entre os elementos da infraestrutura.

A proposta do sistema não é apenas registrar dados: ela envolve interpretar o estado da rede, prever anomalias, priorizar eventos críticos e oferecer suporte para tomada de decisão em tempo real.

O projeto continua a linha do NCAS da Fase 5, mas agora com foco em comunicação e inteligência operacional. Os módulos da colônia passam a ser avaliados em termos de latência, qualidade de sinal, carga de enlace, prioridade operacional e risco de falha.

---

## 📡 Objetivo do projeto

O sistema foi criado para:

- carregar e organizar registros simulados de comunicação
- comparar latência estimada e observada
- classificar erros e alertas por gravidade
- treinar um modelo simples para prever latência
- priorizar eventos críticos com heap max
- buscar registros por prefixo com trie
- relacionar comunicação com eletricidade, potência e dispositivos
- gerar gráficos e relatórios de análise

---

## 🛰 Arquitetura do sistema

O projeto está dividido em módulos com responsabilidades bem definidas:

- `codigo_fonte.py` — entrada principal e menu interativo
- `dados_aurora_siger.csv` — base de dados simulada
- `scic_core/aplicacao.py` — lógica de aplicação e fluxo principal
- `scic_core/dados.py` — carregamento e manipulação dos dados
- `scic_core/erros.py` — indicadores e classificação de erros
- `scic_core/modelo.py` — treinamento e avaliação do modelo de latência
- `scic_core/heap_alertas.py` — processo de priorização por heap
- `scic_core/trie_busca.py` — busca por prefixo e autocomplete
- `scic_core/hardware.py` — dispositivos, bases numéricas e eletricidade
- `scic_core/graficos.py` — geração dos gráficos
- `scic_core/gerar_base.py` — geração da base de dados simulada

---

## 🧠 O que ele analisa

O SCIC trabalha com dados simulados dos módulos da colônia, incluindo:

- `latencia_observada_ms`
- `latencia_estimada_ms`
- `qualidade_sinal`
- `carga_enlace`
- `tensao_v`
- `corrente_a`
- `potencia_w`
- `status`
- `prioridade`
- `codigo_sensor_dec`
- `mensagem_alerta`

A partir disso, o projeto calcula:

- erro absoluto
- erro relativo
- média, mediana e máxima de latência
- classificação do fenômeno como aceitável, atenção ou preocupante
- previsão de latência por regressão linear
- ranking de alertas mais urgentes
- busca eficiente por prefixo de módulo ou código

---

## 📊 Técnicas e estruturas implementadas

O trabalho incorpora conceitos fundamentais de computação aplicada:

- Regressão linear e Ridge para previsão de latência
- Métricas de avaliação: MAE, MSE, RMSE e R²
- Heap máximo para priorização de alertas
- Trie para busca de prefixo rápida
- Conversão entre bases numéricas (decimal, binário e hexadecimal)
- Cálculo de potência elétrica e relações com o hardware
- Geração de relatórios e gráficos para interpretação visual

---

## ▶️ Como executar

Na pasta do projeto:

```bash
cd scic
python codigo_fonte.py
```

### Menu principal

1. Carregar dados
2. Consultar registros
3. Cadastrar registro
4. Indicadores e erros
5. Modelo de latência
6. Heap de alertas
7. Trie (prefixo)
8. Dispositivos, bases e eletricidade
9. Análise final
10. Demonstração completa
0. Sair

### Execução automática para gerar gráficos

```bash
python codigo_fonte.py --demo
```

---

## 🧪 Dependências

O projeto utiliza as bibliotecas:

- NumPy
- Pandas
- Matplotlib
- scikit-learn

Para instalar:

```bash
pip install -r requirements.txt
```

---

## 📁 Estrutura de arquivos

```text
scic/
├── codigo_fonte.py
├── dados_aurora_siger.csv
├── README.md
├── relatorio_tecnico.md
├── requirements.txt
├── link_video.txt
├── graficos_ou_imagens/
│   ├── latencia_por_modulo.png
│   ├── erros_latencia.png
│   ├── modelo_observado_previsto.png
│   └── euler_latencia.png
├── scic_core/
│   ├── __init__.py
│   ├── aplicacao.py
│   ├── catalogo.py
│   ├── dados.py
│   ├── erros.py
│   ├── gerar_base.py
│   ├── graficos.py
│   ├── hardware.py
│   ├── heap_alertas.py
│   ├── modelo.py
│   └── trie_busca.py
└── ...
```

---

## 🧭 Importância do trabalho

Este projeto combina teoria e aplicação prática:

- analisa comunicação em ambiente simulado
- aplica conceitos de dados, machine learning e estruturas de dados
- conecta o problema técnico à operação da colônia
- demonstra como análise de indicadores pode orientar decisões críticas

Em outras palavras, o SCIC funciona como um laboratório de supervisão operacional para uma missão interplanetária, com foco em comunicação, confiabilidade e resposta rápida.

---

## 📌 Observações finais

- A base é simulada e determinística
- O sistema foi pensado para uso em terminal
- Os gráficos podem ser gerados com a execução em modo demo
- O link do vídeo deve ser atualizado em `link_video.txt`

---

## 📝 Refs e entrega

- [Relatório técnico](scic/relatorio_tecnico.md)
- [Entrega final](ENTREGA_FINAL.md)
- [Resumo visual](RESUMO_VISUAL.md)
- [Guia do vídeo](GUIA_VIDEO.md)

> O objetivo da entrega é demonstrar um sistema funcional, bem documentado e alinhado com os requisitos da Fase 6 da FIAP.

> Teste de validação do fluxo de PR no GitHub.

