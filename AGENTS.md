# Contexto da dissertação (para IA / agentes)

Este ficheiro resume a **base lógica** do trabalho de mestrado para qualquer assistente de IA manter coerência com o código, a metodologia e o texto académico.

---

## 1. Tema e foco analítico

**Área:** análise estatística e modelagem de dados aplicada à saúde cardiovascular.

**Foco central:** identificar **associações** entre variáveis clínicas/exames e a **presença de doença cardíaca** (desfecho binário), incluindo:

- **Correlações / associações positivas** (maior valor de uma variável associado a **maior** probabilidade de doença, ou direção coerente com o desfecho, conforme a variável).
- **Anti-correlações / associações negativas** (maior valor associado a **menor** probabilidade de doença, ou Spearman negativo com o desfecho, quando aplicável).

Ou seja: o interesse não é só “quem correlaciona positivamente”, mas **o sinal e a força** da relação com o desfecho, na bivariada e após **ajuste multivariado**.

---

## 2. Natureza dos dados (leitura correta para a dissertação)

O estudo usa **dados secundários, públicos e anonimizados** do repositório **UCI Machine Learning Repository** (subconjunto **Cleveland**, 14 atributos clássicos + diagnóstico angiográfico).

**No projeto, o ficheiro principal é:** `heart_disease_uci.csv` (filtrado apenas a linhas `dataset = Cleveland`), carregado e recodificado em `heart_cleveland_load.py`.

**Importante para redação académica:** quando o autor fala em “dados falsos” no sentido **didático**, refere-se a **não serem dados primários coletados pelo mestrando** (não há coleta clínica própria, nem pacientes identificáveis). **Não** significa que o ficheiro da UCI seja “inventado”: é um **dataset histórico real**, amplamente usado em ensino e pesquisa metodológica. Na dissertação, prefira termos como **dados secundários**, **públicos**, **repositório UCI**, **fins metodológicos**.

**Após exclusão de valores em falta** em `ca`, `thal` e `slope`, a análise principal trabalha com **N ≈ 297** observações (não 303 brutas).

---

## 3. Variáveis (14 preditoras + desfecho)

**Desfecho (`target`), após processamento no código:**

- **`target = 0`:** ausência de doença angiográfica significativa (código UCI `num = 0`, estenose &lt; 50%).
- **`target = 1`:** presença de doença (`num ≥ 1`).

**Preditoras (nomes no código):** `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`.

**Codificação:** no CSV exportado, vários campos vêm em texto (ex.: sexo Male/Female, tipo de dor, slope em palavras). O módulo `heart_cleveland_load.py` converte para os **códigos numéricos da documentação UCI** (ex.: `thal` 3/6/7; `cp` 1–4; `slope` 1–3). A coluna de frequência máxima no CSV chama-se `thalch` e é renomeada para `thalach`.

---

## 4. Problema de pesquisa

**Pergunta central:** quais variáveis clínicas e de exame estão **associadas** à presença de doença cardíaca na análise bivariada e **quais mantêm associação independente** após ajuste simultâneo pelas demais (modelo multivariado)?

---

## 5. Objetivos

**Geral:** identificar e analisar fatores associados à presença de doença cardíaca com métodos bivariados e multivariados.

**Específicos (alinhados ao pipeline):**

1. Caracterizar a amostra (estatística descritiva).
2. Avaliar associações bivariadas com o desfecho (Spearman; qui-quadrado; exemplo de OR bruto).
3. Estimar efeitos **ajustados** por regressão logística binária (OR ajustados / coeficientes).
4. Avaliar desempenho de classificação probabilística do modelo (ROC/AUC; **Brier score** e comparação com modelo nulo de prevalência constante).

---

## 6. Hipóteses (formulação defendível)

**Hipótese nula (H0):** após ajuste multivariado pelas covariáveis incluídas no modelo, **não há associação** entre as variáveis explicativas e a probabilidade de doença cardíaca (coeficientes nulos — formulação global via teste de razão de verossimilhança do modelo).

**Hipótese alternativa (H1):** após o ajuste, **pelo menos uma** variável permanece associada independentemente ao desfecho (pelo menos um coeficiente ≠ 0).

**Hipótese específica (opcional no texto):** o sexo masculino permanece associado à maior odds de doença após controle pelas demais variáveis (teste do coeficiente de `sex`).

_(Ajuste = inclusão simultânea das preditoras na regressão logística; interpretação: efeito **marginal** de cada variável mantendo as outras fixas.)_

---

## 7. Metodologia (o que a IA deve assumir que foi feito)

### 7.1 Dados e pré-processamento

- Leitura de `heart_disease_uci.csv`, filtro **Cleveland**.
- Recodificação texto → códigos UCI (`heart_cleveland_load.py`).
- Criação de `target` binário a partir de `num`.
- `dropna()` nas variáveis com falhas (`ca`, `thal`, `slope`).

### 7.2 Estatística descritiva

- `describe()` e contagens do desfecho.

### 7.3 Análise bivariada

| Tipo de variável                        | Técnica                                   | Papel                                                                                                     |
| --------------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Contínuas + `ca` (contagem ordinal 0–3) | **Spearman** vs `target`                  | Associação monotônica; coeficiente pode ser **positivo** ou **negativo** (“anti-correlação” estatística). |
| Categóricas                             | **Qui-quadrado** de independência         | Associação global; não informa direção.                                                                   |
| Exemplo                                 | **OR bruto** (tabela 2×2 sexo × desfecho) | Magnitude da associação bruta.                                                                            |

**Justificativas curtas:** Spearman é robusto para relações monotônicas com desfecho binário; χ² é padrão para tabelas de contingência; OR exemplifica medida de efeito em escala de chances.

### 7.4 Análise multivariada

- **Regressão logística binária** (`statsmodels.Logit`), todas as preditoras + intercepto.
- Interpretação dos **coeficientes**, **p-valores** e **OR ajustados** `exp(β)` com IC95% (quando reportados no texto ou em tabelas exportadas).

### 7.5 Avaliação do modelo

- **Curva ROC** e **AUC** (discriminação).
- **Brier score** do modelo vs **Brier de referência** (probabilidade constante = prevalência do desfecho) — erro quadrático médio das probabilidades preditas; **menor é melhor**.
- **Limitação explícita:** AUC e Brier calculados **na mesma amostra do ajuste** (in-sample) tendem a ser **otimistas** para generalização; mencionar validação externa / treino-teste / CV como trabalho futuro.

---

## 8. Código principal (repositório)

| Ficheiro                  | Função                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `dataset3.py`             | Pipeline completo: descritiva → Spearman → χ² → OR sexo → logística → ROC/AUC + Brier + figura `curva_roc_dataset3.png`. |
| `heart_cleveland_load.py` | Carrega e harmoniza `heart_disease_uci.csv` (Cleveland + códigos UCI).                                                   |
| `gerar_tabelas_txt.py`    | Gera `tabelas_dissertacao.txt` com tabelas para copiar à dissertação (mesma lógica que `dataset3.py`).                   |

**Dependências típicas:** `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`.

---

## 9. O que a IA **não** deve fazer ao ajudar neste projeto

- Não inverter o significado de `target` sem verificar o código e a documentação UCI (`num` → `target`).
- Não afirmar que o dataset UCI é “falso” no sentido de **fabricado**; usar **secundário / público / metodológico**.
- Não substituir metodologia acordada (logística + bivariada) por “só machine learning” sem alinhamento com o orientador.
- Não omitir limitações de **AUC/Brier in-sample**.

---

## 10. Contribuição esperada do trabalho (mensagem para discussão)

- Demonstrar o contraste entre associação **bruta** e **ajustada** (papel do confundimento).
- Relacionar sinais dos coeficientes e correlações com a **lógica clínica**, quando a codificação UCI estiver corretamente aplicada.
- Entregar um **protocolo reprodutível** (código + tabelas) adequado a dissertação de mestrado em modelagem estatística aplicada à saúde.

---

## 11. Referência rápida do ficheiro de dados

- **Entrada principal:** `heart_disease_uci.csv` (na pasta do projeto).
- **Saídas auxiliares:** `tabelas_dissertacao.txt`, `curva_roc_dataset3.png`.

Esses são os resultados :

Fonte dos dados: Arquivo local heart_disease_uci.csv (apenas Cleveland, codificação numérica UCI, após dropna em ca/thal/slope)
Colunas: ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']

Amostra final: 297 pacientes (após remoção de missing em ca/thal/slope)
Target: 0 (sem doença) = 160, 1 (com doença) = 137

Primeiras linhas:
age sex cp trestbps chol fbs restecg thalach exang oldpeak slope ca thal target
0 63 1 1 145 233 1 2 150 0 2.3 3 0.0 6 0
1 67 1 4 160 286 0 2 108 1 1.5 2 3.0 3 1
2 67 1 4 120 229 0 2 129 1 2.6 2 2.0 7 1
3 37 1 3 130 250 0 0 187 0 3.5 3 0.0 3 0
4 41 0 2 130 204 0 2 172 0 1.4 1 0.0 3 0

Informações:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 297 entries, 0 to 296
Data columns (total 14 columns):

# Column Non-Null Count Dtype

---

0 age 297 non-null int64  
 1 sex 297 non-null int64  
 2 cp 297 non-null int64  
 3 trestbps 297 non-null int64  
 4 chol 297 non-null int64
5 fbs 297 non-null int64
6 restecg 297 non-null int64
7 thalach 297 non-null int64
8 exang 297 non-null int64
9 oldpeak 297 non-null float64
10 slope 297 non-null int64
11 ca 297 non-null float64
12 thal 297 non-null int64
13 target 297 non-null int64
dtypes: float64(2), int64(12)
memory usage: 32.6 KB
None

Estatística descritiva:
age sex cp trestbps chol ... oldpeak slope ca thal target
count 297.000000 297.000000 297.000000 297.000000 297.000000 ... 297.000000 297.000000 297.000000 297.000000 297.000000
mean 54.542088 0.676768 3.158249 131.693603 247.350168 ... 1.055556 1.602694 0.676768 4.730640 0.461279
std 9.049736 0.468500 0.964859 17.762806 51.997583 ... 1.166123 0.618187 0.938965 1.938629 0.499340
min 29.000000 0.000000 1.000000 94.000000 126.000000 ... 0.000000 1.000000 0.000000 3.000000 0.000000
25% 48.000000 0.000000 3.000000 120.000000 211.000000 ... 0.000000 1.000000 0.000000 3.000000 0.000000
50% 56.000000 1.000000 3.000000 130.000000 243.000000 ... 0.800000 2.000000 0.000000 3.000000 0.000000
75% 61.000000 1.000000 4.000000 140.000000 276.000000 ... 1.600000 2.000000 1.000000 7.000000 1.000000
max 77.000000 1.000000 4.000000 200.000000 564.000000 ... 6.200000 3.000000 3.000000 7.000000 1.000000

[8 rows x 14 columns]

===== CORRELAÇÃO SPEARMAN =====
age vs target -> Spearman = 0.240, p-value = 0.00003
trestbps vs target -> Spearman = 0.132, p-value = 0.02317
chol vs target -> Spearman = 0.116, p-value = 0.04643
thalach vs target -> Spearman = -0.429, p-value = 0.00000
oldpeak vs target -> Spearman = 0.411, p-value = 0.00000
ca vs target -> Spearman = 0.492, p-value = 0.00000

===== TESTE QUI-QUADRADO =====

sex vs target
Chi2 = 21.851612168613475
p-value = 2.945690038078843e-06

cp vs target
Chi2 = 77.27579978222383
p-value = 1.1782838465918115e-16

fbs vs target
Chi2 = 0.0
p-value = 1.0

restecg vs target
Chi2 = 9.575507229251564
p-value = 0.008331151353680854

exang vs target
Chi2 = 50.9425597633616
p-value = 9.510884265909016e-13

slope vs target
Chi2 = 43.47317755212573
p-value = 3.630107106911135e-10

thal vs target
Chi2 = 82.46014428007756
p-value = 1.2416728386228762e-18

===== ODDS RATIO (exemplo: sex vs target) =====
Odds Ratio = 3.573932584269663

===== REGRESSÃO LOGÍSTICA =====
Optimization terminated successfully.
Current function value: 0.344594
Iterations 7
Logit Regression Results
==============================================================================
Dep. Variable: target No. Observations: 297
Model: Logit Df Residuals: 283
Method: MLE Df Model: 13
Date: Sat, 18 Apr 2026 Pseudo R-squ.: 0.5007
Time: 15:59:27 Log-Likelihood: -102.34
converged: True LL-Null: -204.97
Covariance Type: nonrobust LLR p-value: 1.136e-36
==============================================================================
coef std err z P>|z| [0.025 0.975]

---

const -7.3720 2.879 -2.560 0.010 -13.016 -1.728
age -0.0142 0.024 -0.591 0.555 -0.061 0.033
sex 1.3121 0.488 2.686 0.007 0.355 2.269
cp 0.5759 0.191 3.012 0.003 0.201 0.951
trestbps 0.0240 0.011 2.241 0.025 0.003 0.045
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
==============================================================================
coef std err z P>|z| [0.025 0.975]

---

const -7.3720 2.879 -2.560 0.010 -13.016 -1.728
age -0.0142 0.024 -0.591 0.555 -0.061 0.033
sex 1.3121 0.488 2.686 0.007 0.355 2.269
cp 0.5759 0.191 3.012 0.003 0.201 0.951
trestbps 0.0240 0.011 2.241 0.025 0.003 0.045
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
coef std err z P>|z| [0.025 0.975]

---

const -7.3720 2.879 -2.560 0.010 -13.016 -1.728
age -0.0142 0.024 -0.591 0.555 -0.061 0.033
sex 1.3121 0.488 2.686 0.007 0.355 2.269
cp 0.5759 0.191 3.012 0.003 0.201 0.951
trestbps 0.0240 0.011 2.241 0.025 0.003 0.045
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
const -7.3720 2.879 -2.560 0.010 -13.016 -1.728
age -0.0142 0.024 -0.591 0.555 -0.061 0.033
sex 1.3121 0.488 2.686 0.007 0.355 2.269
cp 0.5759 0.191 3.012 0.003 0.201 0.951
trestbps 0.0240 0.011 2.241 0.025 0.003 0.045
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
sex 1.3121 0.488 2.686 0.007 0.355 2.269
cp 0.5759 0.191 3.012 0.003 0.201 0.951
trestbps 0.0240 0.011 2.241 0.025 0.003 0.045
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
trestbps 0.0240 0.011 2.241 0.025 0.003 0.045
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
chol 0.0050 0.004 1.324 0.186 -0.002 0.012
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
fbs -1.0219 0.555 -1.840 0.066 -2.110 0.067
restecg 0.2452 0.185 1.325 0.185 -0.117 0.608
thalach -0.0207 0.010 -2.021 0.043 -0.041 -0.001
restecg 0.2452 0.185 1.325 0.185 -0.117 0.608
thalach -0.0207 0.010 -2.021 0.043 -0.041 -0.001
thalach -0.0207 0.010 -2.021 0.043 -0.041 -0.001
exang 0.9261 0.413 2.241 0.025 0.116 1.736
exang 0.9261 0.413 2.241 0.025 0.116 1.736
oldpeak 0.2474 0.212 1.168 0.243 -0.168 0.663
slope 0.5700 0.363 1.570 0.116 -0.142 1.282
ca 1.2677 0.265 4.777 0.000 0.748 1.788
thal 0.3439 0.100 3.427 0.001 0.147 0.541
==============================================================================

AUC = 0.9246350364963504
Brier score (modelo logístico) = 0.106857
Brier score (referência: probabilidade constante = prevalência 0.4613) = 0.248501
(Quanto menor o Brier, melhor a calibragem combinada com o erro quadrático das probabilidades.)
