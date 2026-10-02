# 📹 Guia para Gravação do Vídeo - SCIC Fase 6

## Duração Máxima: 5 minutos

## Roteiro Sugerido

### 1️⃣ Apresentação do Projeto (0:00 - 0:30)
- **O que é**: Sistema de análise de comunicação interplanetária da colônia Aurora Siger
- **Objetivo**: Demonstrar integração de estruturas de dados (heap, trie) com análise numérica
- **Equipe**: Matheus Fuchelberguer, Carlos Eugenio Andrade, Rodrigo Gomes Dias

### 2️⃣ Execução do Menu Principal (0:30 - 1:30)
```bash
python codigo_fonte.py
```
Mostrar:
- Menu com 10 opções disponíveis
- Opção 1: Carregar dados (120 registros, 10 módulos)
- Opção 4: Indicadores e erros (MAE, erro relativo, classificação)
- Opção 5: Modelo de latência (R² = 0.683, MAE = 6.363 ms)

### 3️⃣ Demonstração Completa (1:30 - 4:00)
```bash
python codigo_fonte.py --demo
```
Explicar durante execução:

#### 🔢 Indicadores e Erros (1:30 - 1:50)
- Latência média: 51.974 ms
- Erro absoluto médio: 10.370 ms
- Erro relativo: 18.84%
- **Por que importa**: Detectar quando a comunicação sai do esperado

#### 🤖 Modelo de Previsão (1:50 - 2:10)
- Features usadas: carga, qualidade, potência, prioridade, tensão
- Regressão Linear vs Ridge (Grid Search)
- Divisão: 70% treino / 30% teste
- **MAE vs RMSE**: RMSE > MAE indica picos de erro (esperado)

#### 📚 Heap de Alertas (2:10 - 2:30)
- Pontuação: peso_prioridade × 12 + bônus de status + recência
- Centro de Controle (CTL) e Suporte de Vida (LSS) = essenciais → +20
- Operações O(1) para ver urgente / O(log n) para inserir/remover
- **Vantagem**: Fila de prioridade vs lista simples (O(n))

#### 🔍 Trie e Busca (2:30 - 2:50)
- Busca por prefixo: digita `com` → encontra COM, Complexo, Comando
- Operações por caractere, não por registros
- **Caso real**: Operador em emergência digita 3 letras, SCIC retorna alvos

#### ⚡ Hardware e Bases Numéricas (2:50 - 3:10)
- Código de sensor: decimal 419 → hex 0x1A3 → binário 110100011
- Lei de Ohm: R = V / I
- Potência: P = V × I
- Exemplo: COM nominal = 28V × 1.60A ≈ 44.8W

#### 📊 Gráficos Gerados (3:10 - 3:45)
Mostrar 4 gráficos criados em `graficos_ou_imagens/`:
1. **latencia_por_modulo.png**: Latência média de cada módulo
2. **erros_latencia.png**: Observada vs Estimada (baseline)
3. **modelo_observado_previsto.png**: Scatter plot do modelo (R²)
4. **euler_latencia.png**: Simulação de Euler da latência

#### 💡 Gerenciamento Inteligente (3:45 - 4:00)
- Sensores → Monitoramento contínuo → Automação (heap + trie) → Ação
- Redundância de dados em CSV
- Manutenção preditiva: modelo estima antes de alerta
- Potência do transmissor liga comunicação à energia (PWR)

### 4️⃣ Conclusão (4:00 - 4:30)
- Código em [GitHub - Aurora Siger Fase 6](link-se-houver)
- Dependências: numpy, pandas, matplotlib, scikit-learn
- README.md e relatório técnico no .zip
- **Pontos-chave**: Heap + trie + regressão linear = prototipagem eficiente

---

## Dicas de Gravação

### 📱 Equipamento
- Tela com resolução 1920×1080 ou superior
- Terminal em tamanho legível (fonte ≥ 14pt)
- Áudio claro (microfone)

### ⏱️ Timing
- Fale devagar e claro
- Deixar ~0:30 para apresentação
- ~2:30 para execução e explicações
- ~0:30 para conclusão

### 🎯 Evitar
- Não minimizar/maximizar janelas constantemente
- Não correr a demonstração muito rápido
- Não entrar em detalhes matemáticos complexos (foco no **resultado**)
- Não mencionar "redes neurais" ou "telemetria real"

### ✅ Fazer
- Pausar entre seções
- Apontar os resultados importantes (MAE, R², alertas)
- Relate a história: "dados → erros → modelo → priorização → ação"
- Mostre confiança: é um protótipo, não é fingimento

---

## Publicação no YouTube

1. Gravar e salvar vídeo (máx 300 MB recomendado)
2. Ir para [youtube.com](https://www.youtube.com)
3. Fazer login na conta da FIAP/grupo
4. Criar > Enviar vídeo
5. Título: `SCIC - Sistema de Comunicação Interplanetária da Colônia (Aurora Siger Fase 6)`
6. Descrição:
   ```
   Equipe: Matheus Fuchelberguer, Carlos Eugenio Andrade, Rodrigo Gomes Dias
   FIAP - Ciência da Computação - Fase 6
   
   Protótipo de análise de comunicação para colônia interplanetária Aurora Siger.
   Integra heap para priorização de alertas, trie para busca rápida, 
   análise numérica de erros e modelo linear de previsão.
   
   Repositório: [link do GitHub, se houver]
   ```
7. **Privacidade**: Selecionar "Não listado"
8. Publicar e copiar URL
9. Colar URL em `link_video.txt`

---

## Checklist Final Antes do Upload

- ✅ Vídeo tem menos de 5 minutos
- ✅ Áudio é claro e audível
- ✅ Demonstração completa funcionou sem erros
- ✅ Gráficos foram visualizados
- ✅ Menu do terminal é legível
- ✅ Explicações conectam heap/trie/modelo aos resultados
- ✅ Arquivo `link_video.txt` será atualizado após publicação
- ✅ Equipe revisou antes de publicar

---

## Após Publicar

1. Copiar URL do YouTube (ex: `https://youtu.be/XXXXXXXXXXX`)
2. Atualizar `link_video.txt` com a URL
3. Compactar pasta `scic/` em `scic.zip`
4. Verificar conteúdo do .zip:
   - ✅ `codigo_fonte.py`
   - ✅ `dados_aurora_siger.csv`
   - ✅ `relatorio_tecnico.md`
   - ✅ `README.md`
   - ✅ `link_video.txt` (com URL)
   - ✅ `requirements.txt`
   - ✅ `scic_core/` (todos os módulos)
   - ✅ `graficos_ou_imagens/` (4 gráficos PNG)

---

## Dúvidas Técnicas Comuns

**P: Por que o R² é 0.683?**
R: Porque os dados têm ruído intencional e picos de 8%. Um R² "alto" (0.8+) seria suspeito para dados simulados sem overfitting.

**P: Por que RMSE > MAE?**
R: Porque RMSE penaliza picos mais. Existem erros grandes nos dados, então RMSE cresce.

**P: Posso usar GPU?**
R: Não é necessário. Os dados são pequenos (120 registros, 5 features).

**P: E se o Menu não Iniciar?**
R: Verificar que `python codigo_fonte.py` está sendo rodado na pasta `scic/` e que `dados_aurora_siger.csv` existe.
