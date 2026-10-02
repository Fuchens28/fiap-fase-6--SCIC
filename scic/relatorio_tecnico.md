# Relatório técnico — SCIC (Sistema de Comunicação Interplanetária da Colônia)

**Aurora Siger · Fase 6 · FIAP · Ciência da Computação · 2026**

Equipe: Matheus Fuchelberguer (RM571321), Carlos Eugenio Andrade (RM570285), Rodrigo Gomes Dias (RM569142)

## 1. Contexto da solução

Nas fases anteriores a colônia deixou de ser só um pouso: o NCAS da Fase 5 já registra eventos, aplica regras lógicas e estima risco. O capítulo 1 desta fase deixa claro o próximo problema: **não basta guardar o dado**. A equipe precisa saber se a latência prevista está perto da observada, se o erro ainda é aceitável e qual alerta atender primeiro.

O SCIC é essa camada. Ele não é um sistema de telemetria real, nem um dashboard web, nem uma rede neural. É um protótipo em Python, no terminal, que:

- carrega a base `dados_aurora_siger.csv`;
- calcula indicadores e erros numéricos;
- treina um modelo linear de latência;
- organiza alertas em um max-heap;
- busca módulos e códigos com trie;
- relaciona o resultado a sensores, bases numéricas e potência do transmissor.

Os dez módulos são os mesmos da Fase 5. Isso mantém a história da missão e evita inventar uma colônia nova só para cumprir checklist.

## 2. Descrição dos dados

A base foi gerada de forma simulada e coerente com a operação (arquivo `scic_core/gerar_base.py`, semente 26). Cada linha é um ciclo de um módulo.

Campos usados:

| Campo | Papel |
|---|---|
| `ciclo` | instante do registro |
| `modulo_id`, `nome_modulo`, `tipo_modulo` | identidade do módulo |
| `latencia_observada_ms` | latência medida (simulada) |
| `latencia_estimada_ms` | baseline operacional da equipe de enlace |
| `tensao_v`, `corrente_a`, `potencia_w` | transmissor (P ≈ V·I) |
| `qualidade_sinal`, `carga_enlace` | condições do canal |
| `status` | ativo, manutenção ou alerta |
| `prioridade`, `peso_prioridade` | P1–P5 herdados do NCAS |
| `codigo_sensor_dec` | identificador do sensor |
| `mensagem_alerta` | texto curto do evento |

Há 12 ciclos × 10 módulos = 120 registros, o bastante para treino/teste sem fingir um dataset industrial.

Pandas lê o CSV, converte colunas numéricas, remove linhas quebradas e agrupa médias por módulo. Listas e dicionários aparecem no catálogo (`MODULOS`) e na trie.

## 3. Análise numérica e erros

Erro absoluto:

\[
E_{abs} = |L_{obs} - L_{est}|
\]

Erro relativo (para comparar módulos com escalas diferentes — MIN não pode ser julgado com o mesmo milissegundo do CTL):

\[
E_{rel} = \frac{E_{abs}}{|L_{obs}|}
\]

Limites adotados no código, pensados para a colônia:

- até 12% — aceitável (ruído de enlace);
- 12% a 25% — atenção;
- acima de 25% — preocupante.

A baseline `latencia_estimada_ms` **não** é o modelo de aprendizado: é o envelope que a operação já usava (fórmula simples com carga e qualidade). O modelo da seção 4 tenta melhorar essa estimativa.

Ponto flutuante: `potencia_w` no CSV é `V * I` arredondado. A diferença máxima entre a coluna e o recálculo costuma ficar na casa de \(10^{-12}\) a \(10^{-4}\), conforme o arredondamento de 4 casas. Isso **não** é falha de transmissor; é representação numérica. Um erro relativo de latência de 40% em módulo P1, ao contrário, é decisão operacional.

Método de Euler (opcional, nível da disciplina): a latência de um enlace perturbado é aproximada por

\[
L_{n+1} = L_n + h \cdot (-k (L_n - L_{eq}))
\]

Na análise final, o SCIC simula o COM caindo de 80 ms rumo a 35 ms. Serve para mostrar discretização, não para fingir física de rádio.

## 4. Modelo simples e métricas

Problema de regressão: prever `latencia_observada_ms` a partir de `carga_enlace`, `qualidade_sinal`, `potencia_w`, `peso_prioridade` e `tensao_v`.

Divisão: 70% treino / 30% teste (`train_test_split`, `random_state=42`). O teste não entra no ajuste.

Algoritmos: regressão linear e Ridge. O Ridge passa por Grid Search em `alpha ∈ {0.01, 0.1, 1.0, 10.0}` com validação cruzada de 3 pastas. Fica o modelo de menor MSE no teste.

Métricas (capítulo 7):

- **MAE** — média dos erros em milissegundos (leitura direta para a operação);
- **MSE** — penaliza picos;
- **RMSE** — volta à unidade da latência;
- **R²** — fração da variação explicada;
- **AIC/BIC** — equilíbrio entre ajuste e número de parâmetros, para comparar especificações.

Interpretação que o enunciado pede: um R² alto não fecha o assunto. Se o RMSE ficar claramente acima do MAE, existem registros com erro grande (os picos de 8% da geração). Um único número não avalia a solução.

Baseline versus modelo: o erro absoluto da coluna `latencia_estimada_ms` é o desempenho da regra operacional antiga; MAE/RMSE do sklearn são o desempenho da regressão no conjunto de teste. São contas diferentes e as duas aparecem no sistema de propósito.

## 5. Heap de alertas

Cada alerta vira um objeto com pontuação:

`12·peso + bônus de status + 20 se o módulo é essencial + parcela da latência + parcela do erro relativo + recência do ciclo`.

A estrutura é um **max-heap em lista**, com filho esquerdo `2i+1`, direito `2i+2` e pai `(i-1)//2`. Inserção faz heapify-up; tirar a raiz faz heapify-down. Não usamos `heapq` justamente para mostrar as operações do capítulo 4.

A raiz é o mais urgente. Vantagem sobre lista simples: olhar o topo é O(1); inserir e remover são O(log n). Na lista, achar o máximo é O(n) toda vez — ruim quando o Centro de Controle precisa da próxima ocorrência, não de uma ordenação completa.

## 6. Trie

A trie guarda IDs (`COM`), nomes (`Sistema de Comunicacao`), códigos hexadecimais de sensor e palavras (`Comando`, `Controle`, `Latencia`). Cada caractere é um nível. Buscar o prefixo `com` percorre c-o-m e lista o que pende daquele nó (autocomplete).

Por que a trie: consulta por prefixo não precisa varrer todos os nomes. Em emergência, o operador digita três letras e o SCIC devolve os alvos possíveis. Complexidade da busca cresce com o tamanho do prefixo, não com o número total de registros da colônia.

## 7. Dispositivos, bases e eletricidade

Entrada simulada: sensores de latência, tensão e corrente (linhas do CSV) e teclado do operador. Saída: terminal, relatório e gráficos. Interfaces só conceituais (rede da colônia, USB de bancada, rádio Terra–Marte no COM).

Exemplo do módulo COM: código decimal **1710** = **0x6AE** = binário `11010101110`. Esse número é o identificador que um barramento entregaria à CPU.

Potência do transmissor (lei de Ohm / potência elétrica):

\[
P = V \cdot I, \qquad R = V / I
\]

No COM nominal, \(V = 28\,\mathrm{V}\), \(I = 1{,}60\,\mathrm{A}\), logo \(P \approx 44{,}8\,\mathrm{W}\) e \(R = 17{,}5\,\Omega\). O valor entra no CSV e também como atributo do modelo: enlace mais “pesado” em potência não é independente da latência na simulação.

## 8. Gerenciamento inteligente da comunicação

A discussão parte dos resultados do SCIC, não de um texto genérico de IoT.

- **Sensores e medidores:** cada ciclo grava latência, qualidade, V e I. Sem essa tabela não existe monitoramento.
- **Monitoramento contínuo:** a classificação do erro relativo marca o que saiu do envelope de 12%/25%.
- **Automação:** a heap escolhe o próximo atendimento; a trie reduz o tempo de achar o módulo. Automação aqui é fila e busca, não um agente solto.
- **Redundância e armazenamento:** CSV persiste o histórico; COM e CTL são essenciais de comunicação — um alerta neles sobe na heap. Enlace redundante, na prática da colônia, significaria não depender de um único módulo COM saturado.
- **Manutenção preditiva:** o modelo estima latência **antes** de o status virar alerta. Se carga e qualidade já apontam atraso, a manutenção pode entrar no ciclo seguinte.
- **Redes inteligentes e microrredes:** a potência do transmissor liga o enlace à energia local (PWR). Na Aurora Siger, comunicação e energia não são departamentos separados: um pico de corrente no COM é ao mesmo tempo problema de rádio e de microrrede.

O SCIC não implementa SCADA nem telemetria industrial. Ele mostra **quais indicadores** essa supervisão usaria.

## 9. Reflexão social, cultural e sustentável

Tecnologia na colônia é usada por pessoas. Três pontos ligados a este protótipo:

1. **Uso eficiente da comunicação e sustentabilidade.** Priorizar pela heap evita gastar energia e atenção humana em alerta de mineração enquanto o suporte de vida espera. Menos retransmissão inútil também é menos potência de rádio (os watts calculados na seção 7).

2. **Conhecimentos tradicionais e respeito à natureza.** Culturas indígenas tratam recurso como relação, não como estoque infinito. No SCIC isso vira critério: qualidade do sinal e potência do transmissor são recursos finitos de Marte. Estimar latência para não “abrir o rádio no máximo” o tempo todo é a versão técnica dessa prudência.

3. **Transparência e responsabilidade humana.** A pontuação da heap é uma fórmula explícita, não uma caixa preta. O modelo aprende pesos, mas o menu não fecha o enlace sozinho: o operador confirma. Diversidade na equipe que rotula `status` e escolhe o que é “essencial” importa — o mesmo aviso da Fase 5: um viés no rótulo vira um modelo consistente e injusto. Linguagem dos alertas ficou operacional (`Enlace nominal`, `Latencia acima do envelope`), sem termos que hierarquizem pessoas.

Decisão automatizada sem revisão humana é exatamente o que o capítulo 1 pede para evitar. O SCIC apoia; a tripulação valida.

## 10. Limitações e melhorias

- A base é simulada; não há atraso real Terra–Marte.
- O modelo é linear. Picos foram colocados de propósito, então o RMSE deve superar o MAE.
- Heap e trie são didáticos, em memória.
- Não há autenticação nem redundância física de enlace.

Melhorias possíveis na próxima fase, ainda sem sair do nível da disciplina: mais ciclos, validação temporal (não só split aleatório) e um segundo modelo só para módulos P1.

## 11. Como reproduzir os gráficos

```text
python codigo_fonte.py --demo
```

Arquivos em `graficos_ou_imagens/`: latência por módulo, observado × estimado, observado × previsto do modelo, curva de Euler.
